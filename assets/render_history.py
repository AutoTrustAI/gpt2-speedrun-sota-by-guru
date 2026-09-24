"""Render the Time-to-GPT-2 history in the NanoGPT blog figure style."""
import json
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
BACKGROUND = '#FAF6EC'
CARD = '#FFFDF7'
ACCENT = '#1F4B41'
INK = '#1C2A25'
MUTED = '#64736A'
HISTORY = '#B78962'
GRID = '#E4DFD1'


def date(value):
    return datetime.fromisoformat(value)


def described_time(point):
    if point.get('time_is_approximate'):
        return f"approximately {point['minutes']:g}"
    return f"{point['minutes']:.4f}" if point['series'] == 'scienceguru' else f"{point['minutes']:g}"


def callout(ax, point, label, value, xytext, *, strong=False, align='left', detail=None):
    """Place a labelled result without moving its true date or value."""
    text = f'{label}\n' + r'$\bf{' + value.replace(' ', r'\ ') + '}$'
    if detail:
        text += f'\n{detail}'
    ax.annotate(text, xy=(date(point['date']), point['minutes']),
        xytext=xytext, textcoords='axes fraction', ha=align, va='center',
        fontsize=13.1 if not strong else 15, color=INK,
        linespacing=1.4,
        bbox=dict(boxstyle='round,pad=.62,rounding_size=.4', facecolor=CARD,
                  edgecolor=ACCENT if strong else '#CFC8B7', linewidth=1.9 if strong else 1.1),
        arrowprops=dict(arrowstyle='-', color=ACCENT if strong else '#C6BFAA',
                        lw=1.3, shrinkA=5, shrinkB=9), zorder=8)


data = json.loads((ASSETS / 'speedrun-history-data.json').read_text())
points = data['points']
official = [p for p in points if p['series'] == 'nanochat']
others = [p for p in points if p['series'] == 'comparison']
ours = next(p for p in points if p['series'] == 'scienceguru')
best = json.loads((ROOT / 'results/nc033/metrics.json').read_text())
public = json.loads((ROOT / 'results/public-baselines.json').read_text())
assert len(official) == 6 and len(others) == 2
assert ours['minutes'] == best['training_minutes'] and ours['core'] == best['core']
for point in others:
    original = next(b for b in public['baselines'] if b['id'] == point['id'])
    assert (point['minutes'], point['core'], point['runs']) == (original['minutes'], original['core'], original['runs'])
for point in official:
    assert abs(point['minutes'] - point['reported_hours'] * 60) < 1e-9

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 13,
    'mathtext.fontset': 'dejavusans', 'svg.fonttype': 'none',
    'svg.hashsalt': 'gpt2-history-blog-v2',
})
fig = plt.figure(figsize=(20, 11.25), facecolor=BACKGROUND)
ax = fig.add_axes((.10, .215, .835, .565), facecolor='none')
fig.text(.045, .918, 'GPT-2 Speedrun: training time to the CORE target',
         fontsize=29, color=INK, weight='bold')
fig.text(.045, .871, 'Time-to-GPT-2 · 8× H100 · complete CORE > 0.256525 · latest official record ≈99 min',
         fontsize=16, color=MUTED)
fig.text(.955, .932, 'AutoTrust AI', fontsize=22, color=ACCENT, weight='bold', ha='right')
fig.text(.955, .902, 'SCIENCEGURU', fontsize=12, color=MUTED, weight='bold', ha='right')

ax.set_xlim(date('2026-01-23'), date('2026-10-07'))
ax.set_ylim(55, 195)
ax.set_yticks([60, 80, 100, 120, 140, 160, 180])
ax.set_ylabel('Training time (minutes)', color=MUTED, labelpad=16, fontsize=14)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.tick_params(axis='both', length=0, pad=12, colors=MUTED, labelsize=13)
ax.grid(color=GRID, lw=1)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_color('#CFC8B7')
ax.spines['bottom'].set_linewidth(1)

# The horizontal continuation is the standing record, not an additional result.
ax.step([date(point['date']) for point in official], [point['minutes'] for point in official],
        where='post', color=HISTORY, linewidth=2.5, zorder=3)
ax.plot([date(official[-1]['date']), date(ours['date'])], [official[-1]['minutes']] * 2,
        color=HISTORY, linewidth=2.1, alpha=.45, zorder=2)
ax.scatter([date(point['date']) for point in official], [point['minutes'] for point in official],
           color=HISTORY, edgecolor=BACKGROUND, s=110, linewidth=2, zorder=4)
for point in others:
    ax.scatter(date(point['date']), point['minutes'], marker='o', s=170,
               facecolor=BACKGROUND, edgecolor=HISTORY, linewidth=2.8, zorder=6)
ax.plot([date(ours['date'])] * 2, [official[-1]['minutes'], ours['minutes']],
        color=ACCENT, linestyle=(0, (4, 4)), linewidth=2, zorder=5)
ax.scatter(date(ours['date']), ours['minutes'], marker='*', s=670,
           color=ACCENT, edgecolor=BACKGROUND, linewidth=1.2, zorder=10)

lookup = {point['id']: point for point in points}
callout(ax, lookup['run1'], 'Run 1 · d24 baseline', '≈182.4 min', (.09, .99))
callout(ax, lookup['run2'], 'Run 2 · FP8 training', '≈174.6 min', (.008, .635))
callout(ax, lookup['run3'], 'Run 3 · Larger global batch', '≈165.6 min', (.205, .82))
callout(ax, lookup['run4'], 'Run 4 · ClimbMix data', '≈121.2 min', (.28, .555))
callout(ax, lookup['run5'], 'Run 5 · Autoresearch round 1', '≈108 min', (.01, .225))
callout(ax, lookup['run6'], 'Run 6 · Autoresearch round 2', '≈99 min · official record', (.315, .235))
callout(ax, lookup['pr830_main'], 'Giovanni · ClimbMix', '81.835 min', (.60, .455))
callout(ax, lookup['pr854_hostram'], 'Oriole Networks · n-grams', '91.74 min', (.765, .67))
callout(ax, ours, 'ScienceGuru · Guru Turbo 1.2',
        f"{ours['minutes']:.2f} min", (.50, .12), strong=True,
        detail=f"{official[-1]['minutes'] / ours['minutes']:.2f}× faster than official record")

legend = [
    Line2D([0], [0], color=HISTORY, marker='o', markerfacecolor=HISTORY,
           markersize=8, lw=0, label='Official record'),
    Line2D([0], [0], color=HISTORY, marker='o', markerfacecolor=BACKGROUND,
           markeredgewidth=2, markersize=10, lw=0, label='Public comparison'),
    Line2D([0], [0], color=ACCENT, marker='*', markersize=14, lw=0,
           label='ScienceGuru'),
]
fig.legend(handles=legend, loc='lower left', bbox_to_anchor=(.091, .115), ncol=3,
           frameon=False, labelcolor=MUTED, fontsize=13, columnspacing=2.5, handletextpad=.5)
fig.text(.935, .134, '2026', color=MUTED, fontsize=12, ha='right')
fig.add_artist(Line2D([.045, .955], [.088, .088], transform=fig.transFigure, color=GRID, lw=1))
fig.text(.045, .057,
         'Community records: github.com/karpathy/nanochat · Official times converted from rounded hours. All points use 8× H100.',
         fontsize=11.5, color=MUTED)
fig.text(.045, .030,
         'Dates: leaderboard, submission opening, or repository publication · ScienceGuru: CORE 0.259212 · Sources: docs/SPEEDRUN_CHART.md',
         fontsize=11.5, color=MUTED)

for suffix in ('svg', 'png'):
    fig.savefig(ASSETS / f'speedrun-history.{suffix}', dpi=120, facecolor=BACKGROUND,
                metadata={'Date': None} if suffix == 'svg' else None)
plt.close(fig)

ns = 'http://www.w3.org/2000/svg'
ET.register_namespace('', ns)
path = ASSETS / 'speedrun-history.svg'
tree = ET.parse(path)
svg = tree.getroot()
svg.set('role', 'img')
svg.set('aria-labelledby', 'chart-title chart-description')
for tag, ident, text in [
    ('title', 'chart-title', 'ScienceGuru Time-to-GPT-2 training-time history'),
    ('desc', 'chart-description', 'Linear scale in minutes. ' + '; '.join(
        f"{point['date']} {point['label']}: {described_time(point)} minutes" for point in points)),
]:
    element = ET.Element(f'{{{ns}}}{tag}', {'id': ident})
    element.text = text
    svg.insert(0, element)
tree.write(path, encoding='utf-8', xml_declaration=True)
path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
print(f'Rendered {len(official)} official runs, {len(others)} public comparisons, and ScienceGuru as SVG and 2400×1350 PNG.')
