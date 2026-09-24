"""Render the GPT-2 research workflow and measured experiments from saved metrics.

Run with Python and Matplotlib installed. No benchmark results are estimated.
"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BACKGROUND = "#FAF6EC"
GREEN = "#1F4B41"
INK = "#1C2A25"
MUTED = "#65756C"
GRID = "#E4DFD0"
CARD = "#FFFDF7"

names = ("nc027", "nc029", "nc033")
rows = [json.loads((ROOT / f"results/{name}/metrics.json").read_text()) for name in names]
for name, row in zip(names, rows):
    assert row["experiment"] == name
    assert row["seed"] == 42
    assert row["core"] > 0.256525
    assert abs(row["training_minutes"] * 60 - row["training_seconds"]) < 1e-8
assert [r["mlp_width"] for r in rows] == [5120, 5120, 4864]
assert [r["steps"] for r in rows] == [9873, 9841, 9841]
config = json.loads((ROOT / "results/nc033/configuration.json").read_text())
assert config["step"] == rows[-1]["steps"]
saved_seconds = rows[1]["training_seconds"] - rows[2]["training_seconds"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "svg.fonttype": "none", "svg.hashsalt": "gpt2-research-loop-v1",
})
fig = plt.figure(figsize=(16, 9), facecolor=BACKGROUND)

def label(x, y, value, size=12, color=INK, weight="normal", **kwargs):
    return fig.text(x, y, value, fontsize=size, color=color, weight=weight,
                    transform=fig.transFigure, **kwargs)

label(.043, .94, "A U T O T R U S T  A I  ·  S C I E N C E G U R U  R E S E A R C H  L O O P",
      12.4, GREEN, "bold", va="center")
label(.957, .94, "AutoTrust AI", 23, GREEN, "bold", ha="right", va="center")
label(.957, .904, "GURU TURBO 1.2", 12.5, MUTED, "bold", ha="right")
label(.043, .87, "Tune capacity and schedule, then verify the result", 27, INK, "bold")

cards = [
    ("Survey", "Study the public\nrecipes and the\nbenchmark target"),
    ("Size", "Narrow the MLP:\n5,120 → 4,864\nKeep depth at 22"),
    ("Schedule", "Train for 9,841\nupdates with the\nrecorded schedule"),
    ("Execute", "Retain FP8,\nFlashAttention 3\nand Liger kernels"),
    ("Verify", "Evaluate all 22\nCORE tasks and\nheld-out BPB"),
]
for i, (heading, body) in enumerate(cards):
    x = .043 + i * .188
    fig.add_artist(FancyBboxPatch((x, .66), .162, .163,
        boxstyle="round,pad=0,rounding_size=.012", edgecolor=GRID,
        facecolor=CARD, linewidth=1.1, transform=fig.transFigure))
    label(x + .021, .789, str(i + 1), 12.2, CARD, "bold", ha="center", va="center",
          bbox=dict(boxstyle="circle,pad=.39", facecolor=GREEN, edgecolor="none"))
    label(x + .040, .797, heading, 15, INK, "bold", va="center")
    label(x + .040, .770, body, 12.2, MUTED, va="top", linespacing=1.43)
    if i < len(cards) - 1:
        label(x + .176, .739, "→", 20, GREEN, "bold", ha="center", va="center")

fig.add_artist(plt.Line2D([.043, .957], [.632, .632], transform=fig.transFigure,
                         color=GRID, linewidth=1))
label(.5, .632, "Recorded experiments make the speed–quality tradeoff inspectable", 13.2,
      GREEN, "bold", ha="center", va="center", backgroundcolor=BACKGROUND)

label(.043, .573, "Three completed experiments on 8×H100", 19, INK, "bold")
label(.043, .537, "Native training time · full 22-task CORE · lower time is better", 12.5, MUTED)
ax = fig.add_axes((.295, .262, .56, .248), facecolor="none")
ax.set_xlim(0, 80)
ax.set_ylim(2.6, -.6)
ax.set_xticks([0, 20, 40, 60, 80])
ax.set_xticklabels(["0", "20", "40", "60", "80 min"])
ax.set_yticks([])
ax.tick_params(axis="x", length=0, pad=9, labelsize=11, colors=MUTED)
ax.set_axisbelow(True)
ax.grid(axis="x", color=GRID, linewidth=.9)
for spine in ax.spines.values():
    spine.set_visible(False)
for i, row in enumerate(rows):
    color = GREEN if i == 2 else "#A9AEA1"
    ax.barh(i, row["training_minutes"], height=.38, color=color, zorder=3)
    y = fig.transFigure.inverted().transform(ax.transData.transform((0, i)))[1]
    label(.280, y + .011, f'{row["experiment"]} · MLP {row["mlp_width"]:,}', 14,
          GREEN if i == 2 else INK, "bold", ha="right", va="center")
    label(.280, y - .018, f'{row["steps"]:,} updates · CORE {row["core"]:.6f}',
          11.1, MUTED, ha="right", va="center")
    ax.text(row["training_minutes"] + 1.2, i, f'{row["training_minutes"]:.4f} min',
            fontsize=14, color=color if i == 2 else INK, weight="bold", va="center", clip_on=False)

fig.add_artist(FancyBboxPatch((.043, .123), .914, .082,
    boxstyle="round,pad=0,rounding_size=.009", linewidth=0, facecolor="#E8EEE2",
    transform=fig.transFigure))
label(.060, .176,
      f'At 9,841 updates, MLP 4,864 recorded {saved_seconds:.2f} s less training time than MLP 5,120.',
      13.5, GREEN, "bold", va="center")
label(.060, .146,
      f'CORE {rows[1]["core"]:.6f} → {rows[2]["core"]:.6f}; both exceed the 0.256525 target.',
      12.3, MUTED, va="center")

fig.add_artist(plt.Line2D([.043, .957], [.093, .093], transform=fig.transFigure,
                         color=GRID, linewidth=.9))
label(.043, .066, "Each row is one completed seed 42 run; these measurements are not repeated-run averages.",
      10.7, MUTED)
label(.043, .039, "Sources: results/nc027, nc029, nc033/metrics.json · docs/STRATEGY.md", 10.5, MUTED)
label(.957, .039, "github.com/AutoTrustAI/gpt2-speedrun-sota-by-guru", 10.5, GREEN, "bold", ha="right")

for suffix in ("svg", "png"):
    fig.savefig(ASSETS / f"gpt2-research-loop.{suffix}", dpi=150, facecolor=BACKGROUND,
                metadata={"Date": None} if suffix == "svg" else None)
plt.close(fig)

ns = "http://www.w3.org/2000/svg"
ET.register_namespace("", ns)
path = ASSETS / "gpt2-research-loop.svg"
tree = ET.parse(path)
svg = tree.getroot()
svg.set("role", "img")
svg.set("aria-labelledby", "chart-title chart-description")
descriptions = [
    ("title", "chart-title", "ScienceGuru GPT-2 research workflow and completed experiments"),
    ("desc", "chart-description",
     "Five workflow stages: survey, size the MLP, schedule training, execute, verify. "
     + "; ".join(f'{r["experiment"]}: MLP width {r["mlp_width"]}, {r["steps"]} updates, '
                  f'{r["training_minutes"]:.6f} minutes, CORE {r["core"]:.6f}' for r in rows)
     + f". Each is one seed 42 run. At 9841 updates, nc033 took {saved_seconds:.2f} seconds less than nc029; "
       "CORE decreased but stayed above the target. The training-time axis starts at zero."),
]
for tag, ident, value in reversed(descriptions):
    element = ET.Element(f"{{{ns}}}{tag}", {"id": ident})
    element.text = value
    svg.insert(0, element)
tree.write(path, encoding="utf-8", xml_declaration=True)
print("Rendered GPT-2 research workflow as 2400×1350 PNG and accessible SVG.")
