"""Render six nanochat leaderboard runs and selected Time-to-GPT-2 results."""
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
MUTED = '#6C7C73'
HISTORY = '#8B9F85'

def date(value):
    return datetime.fromisoformat(value)

def callout(ax, point, text, xytext, *, strong=False, align='left'):
    ax.annotate(text, xy=(date(point['date']), point['minutes']),
        xytext=xytext, textcoords='axes fraction', ha=align, va='center',
        fontsize=12 if not strong else 15, color=ACCENT if strong else INK,
        weight='bold' if strong else 'normal', linespacing=1.4,
        bbox=dict(boxstyle='round,pad=.5,rounding_size=.2', facecolor=CARD,
                  edgecolor=ACCENT if strong else '#D2DACF', linewidth=1.1),
        arrowprops=dict(arrowstyle='-', color=ACCENT if strong else '#A9B8A7',
                        lw=1.1, shrinkA=6, shrinkB=8), zorder=8)

data = json.loads((ASSETS / 'speedrun-history-data.json').read_text())
points = data['points']
official = [p for p in points if p['series'] == 'nanochat']
others = [p for p in points if p['series'] == 'comparison']
ours = next(p for p in points if p['series'] == 'scienceguru')
best = json.loads((ROOT / 'results/nc033/metrics.json').read_text())
public = json.loads((ROOT / 'results/public-baselines.json').read_text())
assert len(official) == 6
assert ours['minutes'] == best['training_minutes'] and ours['core'] == best['core']
for point in others:
    original = next(b for b in public['baselines'] if b['id'] == point['id'])
    assert (point['minutes'], point['core'], point['runs']) == (original['minutes'], original['core'], original['runs'])
for p in official:
    assert abs(p['minutes'] - p['reported_hours'] * 60) < 1e-9
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'svg.fonttype': 'none', 'svg.hashsalt': 'gpt2-history-v1'})
fig = plt.figure(figsize=(20, 9.8), facecolor=BACKGROUND)
ax = fig.add_axes((.08, .20, .87, .54), facecolor='none')
fig.text(.052, .945, 'AutoTrust', fontsize=18, color=INK, weight='bold')
fig.text(.052, .885, 'ScienceGuru · Guru Turbo 1.2', fontsize=30, color=INK, weight='bold')
fig.text(.052, .835, 'Time-to-GPT-2 · 8× H100 · Complete CORE target > 0.256525', fontsize=15, color=MUTED)
fig.text(.955, .943, f"{ours['minutes']:.4f} min", fontsize=32, ha='right', color=ACCENT, weight='bold')
fig.text(.955, .887, '≈1.37× faster than official SOTA', fontsize=16, ha='right', color=INK)
fig.text(.955, .843, '≈27.03% less training time · CORE 0.259212', fontsize=12.5, ha='right', color=MUTED)
ax.set_xlim(date('2026-01-20'), date('2026-10-20'))
ax.set_ylim(52, 205)
ax.set_yticks([60, 90, 120, 150, 180])
ax.set_ylabel('Reported training time (minutes)', color=INK, labelpad=15, fontsize=13)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b 2026'))
ax.tick_params(axis='both', length=0, pad=10, colors=MUTED)
ax.grid(axis='y', color='#D6DDD1', lw=.9)
ax.grid(axis='x', color='#E1E5D9', lw=.7)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_color('#D2DACF')
ax.step([date(p['date']) for p in official], [p['minutes'] for p in official],
        where='post', color=HISTORY, linewidth=2.3, zorder=3)
ax.scatter([date(p['date']) for p in official], [p['minutes'] for p in official],
           color='#D2DCCB', edgecolor=HISTORY, s=65, linewidth=1.2, zorder=4)
for p in others:
    ax.scatter(date(p['date']), p['minutes'], marker='D', s=85,
               facecolor=CARD, edgecolor='#6B8B7B', linewidth=1.6, zorder=6)
ax.scatter(date(ours['date']), ours['minutes'], marker='*', s=550, color=ACCENT, zorder=10)
last = official[-1]
ax.annotate('', xy=(date(ours['date']), ours['minutes']), xytext=(date(last['date']), last['minutes']),
            arrowprops=dict(arrowstyle='-', linestyle=(0, (4, 4)), color=ACCENT,
                            connectionstyle='arc3,rad=0', linewidth=1.5, alpha=.55, shrinkA=8, shrinkB=12))
lookup = {p['id']: p for p in points}
callout(ax, lookup['run1'], 'Run 1 · d24 baseline\n≈182.4 min', (.13, .93))
callout(ax, lookup['run2'], 'Run 2 · FP8\n≈174.6 min', (.015, .60))
callout(ax, lookup['run3'], 'Run 3 · Larger batch\n≈165.6 min', (.25, .73))
callout(ax, lookup['run4'], 'Run 4 · ClimbMix\n≈121.2 min', (.30, .51))
callout(ax, lookup['run5'], 'Run 5 · Autoresearch round 1\n≈108 min', (.06, .12))
callout(ax, lookup['run6'], 'Run 6 · Autoresearch round 2\n≈99 min · official SOTA', (.35, .13))
callout(ax, lookup['pr830_main'], 'Giovanni · ClimbMix\n81.835 min', (.57, .53))
callout(ax, lookup['pr830_mixed'], 'Giovanni · Mixed data\n73.917 min', (.60, .12))
callout(ax, lookup['pr854_hostram'], 'Oriole Networks · n-grams\n91.74 min', (.78, .48))
callout(ax, ours, 'ScienceGuru\n72.2419 min', (.995, .29), strong=True, align='right')
legend = [Line2D([0], [0], color=HISTORY, marker='o', markerfacecolor='#D2DCCB', lw=2, label='nanochat leaderboard · 6 runs'),
          Line2D([0], [0], color='#6B8B7B', marker='D', markerfacecolor=CARD, lw=0, label='Selected comparisons'),
          Line2D([0], [0], color=ACCENT, marker='*', markersize=14, lw=0, label='ScienceGuru · seed 42')]
fig.legend(handles=legend, loc='lower left', bbox_to_anchor=(.06, .079), ncol=3,
           frameon=False, labelcolor=INK, fontsize=12, columnspacing=3)
fig.text(.065, .045, 'Dates: official leaderboard, submission opening, or repository publication · Sources and exact values: docs/SPEEDRUN_CHART.md', fontsize=10.5, color=MUTED)
fig.text(.065, .016, 'Official times are converted from rounded leaderboard hours. All plotted results use the 8× H100 Time-to-GPT-2 protocol.', fontsize=10.5, color=MUTED)
for suffix in ('svg', 'png'):
    fig.savefig(ASSETS / f'speedrun-history.{suffix}', dpi=160, facecolor=BACKGROUND, metadata={'Date': None} if suffix == 'svg' else None)
plt.close(fig)
ns = 'http://www.w3.org/2000/svg'
ET.register_namespace('', ns)
path = ASSETS / 'speedrun-history.svg'; tree = ET.parse(path); svg = tree.getroot()
svg.set('role', 'img'); svg.set('aria-labelledby', 'chart-title chart-description')
def described_time(point):
    if point.get('time_is_approximate'):
        return f"approximately {point['minutes']:g}"
    return f"{point['minutes']:.4f}" if point['series'] == 'scienceguru' else f"{point['minutes']:g}"

for tag, ident, text in [('title', 'chart-title', 'ScienceGuru Time-to-GPT-2 training-time history'),
    ('desc', 'chart-description', '; '.join(f"{p['date']} {p['label']}: {described_time(p)} minutes" for p in points))]:
    element = ET.Element(f'{{{ns}}}{tag}', {'id': ident}); element.text = text; svg.insert(0, element)
tree.write(path, encoding='utf-8', xml_declaration=True)
print('Rendered six official runs, three public comparisons, and ScienceGuru as SVG and PNG.')
