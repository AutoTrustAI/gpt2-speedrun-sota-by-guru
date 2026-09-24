"""Render the GPT-2 comparison. Run with Python and Matplotlib installed."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
BACKGROUND = '#FAF6EC'
ACCENT = '#1F4B41'
INK = '#1C2A25'
MUTED = '#6C7C73'
GRID = '#E1E5D9'

best = json.loads((ROOT / 'results/nc033/metrics.json').read_text())
public = json.loads((ROOT / 'results/public-baselines.json').read_text())
data = json.loads((ASSETS / 'comparison-data.json').read_text())
rows = data['points']
assert rows[0]['minutes'] == best['training_minutes']
assert rows[0]['core'] == best['core']
for row in rows[1:]:
    original = next(b for b in public['baselines'] if b['id'] == row['id'])
    assert (row['minutes'], row['core'], row['runs']) == (original['minutes'], original['core'], original['runs'])
assert [r['minutes'] for r in rows] == sorted(r['minutes'] for r in rows)

labels = {
    'scienceguru_nc033': ('ScienceGuru', 'AutoTrust · Guru Turbo 1.2'),
    'pr830_main': ('ClimbMix recipe', 'Giovanni Zinzi · 6 runs'),
    'pr854_hostram': ('Host-RAM n-grams', 'Oriole Networks · 3 runs'),
    'official_run6': ('Official SOTA · Run 6', 'Andrej Karpathy · 5 runs'),
}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'svg.fonttype': 'none', 'svg.hashsalt': 'gpt2-comparison-v2'})
fig = plt.figure(figsize=(16, 7.5), facecolor=BACKGROUND)
ax = fig.add_axes((.32, .21, .63, .55), facecolor='none')
ax.set_xlim(0, 115)
ax.set_ylim(len(rows) - .35, -.65)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_yticks([])
ax.tick_params(axis='x', length=0, pad=10, colors=MUTED)
ax.set_axisbelow(True)
ax.grid(axis='x', color=GRID, linewidth=.9)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xlabel('Reported training time (minutes) · lower is better', labelpad=15, color=MUTED)
fig.text(.035, .945, 'AutoTrust · ScienceGuru · Guru Turbo 1.2', color=ACCENT, fontsize=16, weight='bold')
fig.text(.035, .878, 'GPT-2 training-time comparison', color=INK, fontsize=28, weight='bold')
fig.text(.035, .823, '8× H100  ·  Complete CORE target > 0.256525', color=MUTED, fontsize=14)
for i, row in enumerate(rows):
    ours = i == 0
    y = fig.transFigure.inverted().transform(ax.transData.transform((0, i)))[1]
    if ours:
        fig.add_artist(FancyBboxPatch((.022, y - .043), .955, .086,
            boxstyle='round,pad=.008,rounding_size=.012', linewidth=0,
            facecolor='#E4EEE7', transform=fig.transFigure, zorder=-1))
    ax.barh(i, row['minutes'], height=.43, color=ACCENT if ours else '#B3C3B8', zorder=3)
    title, subtitle = labels[row['id']]
    fig.text(.035, y + .012, title, color=ACCENT if ours else INK, fontsize=16, weight='bold', va='center')
    fig.text(.035, y - .021, subtitle, color=MUTED, fontsize=11, va='center')
    value = f"{row['minutes']:.4f}" if ours else ('≈99' if row.get('time_is_approximate') else f"{row['minutes']:g}")
    ax.text(row['minutes'] + 1.8, i - .08, value + ' min', color=ACCENT if ours else INK,
            weight='bold', fontsize=14, va='center')
    ax.text(row['minutes'] + 1.8, i + .19, f"CORE {row['core']:.6f}", color=MUTED, fontsize=9.5, va='center')
fig.text(.035, .07, 'ScienceGuru: 9,841 updates · seed 42 · CORE 0.259212', fontsize=12, color=INK)
fig.text(.035, .033, 'Sources and run counts: README comparison and docs/BENCHMARK.md · checked 2026-09-24 UTC', fontsize=10, color=MUTED)
for suffix in ('svg', 'png'):
    fig.savefig(ASSETS / f'gpt2-comparison.{suffix}', dpi=160, facecolor=BACKGROUND, metadata={'Date': None} if suffix == 'svg' else None)
plt.close(fig)
ns = 'http://www.w3.org/2000/svg'
ET.register_namespace('', ns)
path = ASSETS / 'gpt2-comparison.svg'
tree = ET.parse(path)
svg = tree.getroot(); svg.set('role', 'img'); svg.set('aria-labelledby', 'chart-title chart-description')
def described_time(row):
    if row.get('time_is_approximate'):
        return f"approximately {row['minutes']:g}"
    return f"{row['minutes']:.4f}" if row['id'] == 'scienceguru_nc033' else f"{row['minutes']:g}"

for tag, ident, text in [('title', 'chart-title', 'ScienceGuru GPT-2 training-time comparison'),
    ('desc', 'chart-description', '; '.join(f"{labels[r['id']][0]}: {described_time(r)} minutes, CORE {r['core']:.6f}" for r in rows))]:
    element = ET.Element(f'{{{ns}}}{tag}', {'id': ident}); element.text = text; svg.insert(0, element)
tree.write(path, encoding='utf-8', xml_declaration=True)
print(f'Rendered {len(rows)} GPT-2 comparison rows as SVG and PNG.')
