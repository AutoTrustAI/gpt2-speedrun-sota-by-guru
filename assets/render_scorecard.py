"""Render the GPT-2 result card in the supplied NanoGPT blog's visual style."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
result = json.loads((ROOT / 'results/nc033/metrics.json').read_text())
comparison = json.loads((ASSETS / 'comparison-data.json').read_text())
public = json.loads((ROOT / 'results/public-baselines.json').read_text())
references = {row['id']: row for row in public['baselines']}
points = {row['id']: row for row in comparison['points']}
minutes = result['training_seconds'] / 60
assert abs(minutes - result['training_minutes']) < 1e-10
assert (points['scienceguru_nc033']['minutes'], points['scienceguru_nc033']['core']) == (minutes, result['core'])
assert result['core'] > comparison['core_target']
assert result['steps'] - result['timed_steps'] == 11
for key in ('official_run6', 'pr830_main'):
    assert points[key]['minutes'] == references[key]['minutes']
official = references['official_run6']['minutes']
climbmix = references['pr830_main']['minutes']
speedup = official / minutes
other_speedup = climbmix / minutes
reduction = 100 * (1 - minutes / official)
saved = official - minutes

GREEN = '#1F4B41'
CREAM = '#FAF6EC'
GOLD = '#E5C677'
MUTED = '#BED0C5'
CARD = '#2B5148'
EDGE = '#46695F'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none',
                     'svg.hashsalt': 'scienceguru-gpt2-scorecard-v1'})
fig = plt.figure(figsize=(20, 11.25), facecolor=GREEN)
texts = []


def text(x, y, value, size, color=CREAM, weight='normal', **kwargs):
    artist = fig.text(x, y, value, fontsize=size, color=color, weight=weight,
                      transform=fig.transFigure, **kwargs)
    texts.append(artist)
    return artist


text(.047, .915, 'AUTOTRUST AI  ·  SCIENCEGURU', 15, MUTED, 'bold')
fig.add_artist(FancyBboxPatch((.765, .892), .186, .05,
    boxstyle='round,pad=.007,rounding_size=.024', transform=fig.transFigure,
    facecolor='none', edgecolor='#749083', linewidth=1))
text(.858, .908, 'Time-to-GPT-2', 15, weight='bold', ha='center')
text(.047, .802, 'ScienceGuru × Guru Turbo 1.2', 50, weight='bold')
text(.047, .730, 'GPT language model trained past the GPT-2 quality target on 8×H100.', 19, MUTED)
text(.047, .690, 'Complete 22-task evaluation · CORE target > 0.256525.', 19, MUTED)

number = text(.040, .412, f'{minutes:.2f}', 155, GOLD, 'bold')
fig.canvas.draw()
number_right = number.get_window_extent(fig.canvas.get_renderer()).x1 / fig.bbox.width
text(number_right + .005, .414, 'min', 36, GOLD, 'bold')
text(.047, .333, 'Training time to the GPT-2 quality target', 21, weight='bold')
text(.047, .286, f"{result['steps']:,} updates · {result['timed_steps']:,} timed updates", 17, MUTED)

for x, y, height in ((.500, .425, .226), (.738, .425, .226),
                     (.500, .211, .190), (.738, .211, .190)):
    fig.add_artist(FancyBboxPatch((x, y), .213, height,
        boxstyle='round,pad=.007,rounding_size=.015', transform=fig.transFigure,
        facecolor=CARD, edgecolor=EDGE, linewidth=1))

text(.512, .579, f'≈{speedup:.2f}×', 42, weight='bold')
text(.512, .526, 'faster than official Run 6', 16, MUTED)
text(.512, .487, f'(≈{official:g} min)', 17, weight='bold')
text(.750, .579, f'{other_speedup:.2f}×', 42, weight='bold')
text(.750, .526, 'faster than the ClimbMix', 16, MUTED)
text(.750, .490, 'recipe by Giovanni Zinzi', 16, MUTED)
text(.750, .453, f'({climbmix:g} min)', 17, weight='bold')
text(.512, .326, f"{result['core']:.6f}", 35, weight='bold')
text(.512, .283, 'complete 22-task CORE', 16, MUTED)
text(.512, .247, f"above target {comparison['core_target']:.6f}", 15.5, MUTED)
text(.750, .326, f'≈{reduction:.2f}%', 37, weight='bold')
text(.750, .283, 'less training time vs Run 6', 15.5, MUTED)
text(.750, .247, f'≈{saved:.2f} minutes saved', 15.5, MUTED)

fig.add_artist(plt.Line2D([.047, .953], [.120, .120], transform=fig.transFigure,
                          color=EDGE, linewidth=1))
text(.047, .079, '8× H100 80GB · native training timer · one completed run', 13, MUTED)
text(.953, .079, 'github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru', 13, weight='bold', ha='right')
text(.047, .044, 'Sources: nc033 metrics and public baselines. Official Run 6 time is rounded; derived comparisons are approximate.', 11.5, MUTED)

fig.canvas.draw()
renderer = fig.canvas.get_renderer()
for artist in texts:
    bounds = artist.get_window_extent(renderer)
    assert bounds.x0 >= 0 and bounds.y0 >= 0 and bounds.x1 <= fig.bbox.width and bounds.y1 <= fig.bbox.height, artist.get_text()
for suffix in ('svg', 'png'):
    fig.savefig(ASSETS / f'gpt2-scorecard.{suffix}', dpi=120, facecolor=GREEN,
                metadata={'Date': None} if suffix == 'svg' else None)
plt.close(fig)

ns = 'http://www.w3.org/2000/svg'
ET.register_namespace('', ns)
path = ASSETS / 'gpt2-scorecard.svg'
tree = ET.parse(path)
svg = tree.getroot()
svg.set('role', 'img')
svg.set('aria-labelledby', 'chart-title chart-description')
description = (f"ScienceGuru with Guru Turbo 1.2: {minutes:.4f} minutes on 8 H100 GPUs; "
    f"complete 22-task CORE {result['core']:.6f}, above {comparison['core_target']:.6f}. "
    f"Approximately {speedup:.2f} times the training speed and {reduction:.2f}% less training time "
    f"than the rounded official Run 6 reference of {official:g} minutes; "
    f"{other_speedup:.2f} times the training speed of the {climbmix:g}-minute ClimbMix recipe. "
    f"One completed run; {result['steps']} updates, including {result['timed_steps']} timed updates.")
for tag, ident, value in [('title', 'chart-title', 'ScienceGuru Time-to-GPT-2 result scorecard'),
                          ('desc', 'chart-description', description)]:
    node = ET.Element(f'{{{ns}}}{tag}', {'id': ident})
    node.text = value
    svg.insert(0, node)
tree.write(path, encoding='utf-8', xml_declaration=True)
print('Rendered the verified GPT-2 scorecard as SVG and 2400×1350 PNG.')
