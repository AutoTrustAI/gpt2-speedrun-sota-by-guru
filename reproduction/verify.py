"""Portable source/input/result checks; no training code is modified."""
import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text())


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def base_dir():
    return Path(os.environ.get('NANOCHAT_BASE_DIR', str(Path.home() / '.cache/nanochat'))).expanduser().absolute()


def sources():
    manifest = read(ROOT / 'reproduction/source-manifest.json')
    for name, expected in manifest['files'].items():
        p = ROOT / name
        require(p.is_file() and p.stat().st_size == expected['bytes'] and sha(p) == expected['sha256'], 'Frozen source differs: ' + name)
    return {'verified_source_files': len(manifest['files']), 'source_commit': manifest['frozen_training_source_commit']}


def inputs():
    base = base_dir()
    manifest = read(ROOT / 'reproduction/input-manifest.json')
    expected = {r['path']: r['bytes'] for r in manifest['parquet_inventory']}
    actual = {p.relative_to(base).as_posix(): p.stat().st_size for p in (base / 'base_data_climbmix').glob('*.parquet')}
    require(actual == expected, 'Expected exactly170 train shards plus the fixed heldout shard, with recorded sizes')
    require({p.relative_to(base).as_posix() for p in (base / 'eval_bundle').rglob('*') if p.is_file()} == {r['path'] for r in manifest['evaluation_files']}, 'Canonical evaluation bundle inventory differs')
    for row in manifest['hashed_inputs'] + manifest['evaluation_files']:
        p = base / row['path']
        require(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Input identity differs: ' + row['path'])
    return {'parquet_files': len(expected), 'hashed_inputs': len(manifest['hashed_inputs']), 'evaluation_files': len(manifest['evaluation_files'])}


def environment():
    expected = read(ROOT / 'reproduction/environment.json')['required_packages']
    actual = {name: importlib.metadata.version(name) for name in expected}
    require(actual == expected, 'Required package versions differ from the recorded environment')
    import torch
    require(torch.cuda.device_count() == 8, 'The fixed recipe requires exactly8 visible GPUs')
    require(all('H100' in torch.cuda.get_device_name(i) for i in range(8)), 'The recorded hardware is8xH100')
    from nanochat.flash_attention import USE_FA3
    require(USE_FA3, 'Original Flash Attention3 did not load')
    return {'packages': actual, 'gpus': [torch.cuda.get_device_name(i) for i in range(8)], 'flash_attention3': True}


def result(steps):
    recipe = read(ROOT / 'reproduction/recipes.json')['recipes'][str(steps)]
    base = base_dir(); tag = recipe['model_tag']; run = base / 'benchmark_results' / tag
    checkpoint = base / 'base_checkpoints' / tag
    names = {f'meta_{steps:06d}.json', f'model_{steps:06d}.pt'} | {f'optim_{steps:06d}_rank{r}.pt' for r in range(8)}
    require({p.name for p in checkpoint.iterdir()} == names, 'Expected complete10-file native checkpoint')
    require(all((checkpoint / n).is_file() and (checkpoint / n).stat().st_size > 0 for n in names), 'Empty checkpoint file')
    meta = read(checkpoint / f'meta_{steps:06d}.json')
    require(meta['step'] == steps and meta['model_config'] == recipe['model_config'] and meta['user_config'] == recipe['user_config'], 'Checkpoint does not match the fresh fixed recipe')
    require((meta['device_batch_size'], meta['max_seq_len'], meta['total_batch_size']) == (32, 2048, 524288), 'Checkpoint batch geometry changed')
    require(meta['step'] * meta['total_batch_size'] == recipe['actual_training_tokens'], 'Training token count changed')
    ansi = re.compile(r'\x1b\[[0-9;]*m')
    training = ansi.sub('', (run / 'train.log').read_text())
    require(f'Using user-provided number of iterations: {steps:,}' in training and 'Resuming optimization from step' not in training, 'Fresh explicit-iteration training marker missing')
    records = re.findall(r'^step (\d+)/(\d+) .*? \| dt: (\S+)ms \|', training, re.M)
    require([(int(s), int(n)) for s,n,dt in records] == [(s, steps) for s in range(steps)], 'Incomplete native training log')
    dt = [float(v) / 1000 for _,_,v in records[11:]]
    seconds = meta['loop_state']['total_training_time']
    require(len(dt) == recipe['timed_steps'] and math.isfinite(seconds) and seconds > 0 and abs(sum(dt) - seconds) <= len(dt) * .000005 + .00001, 'Native timer/log mismatch')
    with (run / 'core.csv').open() as f:
        rows = [{k.strip(): v.strip() for k,v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    require([r['Task'] for r in rows] == recipe['core_labels'] + ['CORE'], 'Expected the complete ordered22-task CORE evaluation')
    scores = [float(r['Centered']) for r in rows[:-1]]; core = float(rows[-1]['Centered'])
    require(all(math.isfinite(v) for v in scores + [core]) and abs(sum(scores) / 22 - core) <= .000001001, 'CORE aggregation mismatch')
    evaluation = ansi.sub('', (run / 'eval.log').read_text())
    require(f'Evaluating model: base_model (step {steps})' in evaluation and 'Eval modes: bpb, core' in evaluation, 'Independent evaluation identity differs')
    require(re.findall(r'^Evaluating: (.+?) \(', evaluation, re.M) == recipe['core_labels'], 'Incomplete evaluation log')
    bpb = {}
    for split in ('train', 'val'):
        values = re.findall(rf'^{split} bpb: (\S+)$', evaluation, re.M)
        require(len(values) == 1 and math.isfinite(float(values[0])) and float(values[0]) > 0, 'Missing independent BPB')
        bpb[split] = float(values[0])
    report = {'steps': steps, 'timed_steps': len(dt), 'native_training_seconds': seconds, 'native_training_minutes': seconds / 60, 'seed': 42, 'CORE': core, 'passes_CORE': core > recipe['core_threshold'], 'independent_bpb': bpb, 'full_core_tasks': 22, 'canonical_bpb_tokens_per_split': recipe['canonical_bpb_tokens_per_split']}
    (run / 'result.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('check', choices=['source', 'inputs', 'environment', 'result'])
    parser.add_argument('--steps', type=int, choices=[9841,9777])
    args = parser.parse_args()
    if args.check == 'result':
        parser.error('--steps is required for result') if args.steps is None else None
        report = result(args.steps)
    else:
        report = {'source': sources, 'inputs': inputs, 'environment': environment}[args.check]()
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == '__main__':
    # Environment check imports the unchanged repo package from any invocation cwd.
    sys.path.insert(0, str(ROOT))
    main()
