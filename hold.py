import csv
import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Get a dictionary of all CSS4 colors
css_colors_dict = mcolors.CSS4_COLORS

# Extract just the color names as a list
color_names = list(css_colors_dict.keys())


fx = lambda Vout, Iload: (0.37834+0.02285*Iload)*Vout/0.65

Iload = np.arange(0.5,4.0+0.5,0.5)
Vout = np.arange(0.65,0.95+0.1,0.1)

CSV_PATH = "/Users/nislam/Desktop/Katie_Website/XFly6S_thickgate_powerstage_efficiency.csv"


def load_efficiency(path):
    """Parse the swapSweep CSV into {Vout: (Iload array, efficiency array)}.

    Columns come in X/Y pairs, one pair per Vout, e.g.
    'swapSweep(eff_power "Iload") (Vout=0.65) X' / '... Y'
    """
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader if any(c.strip() for c in r)]

    data = {}
    for i in range(0, len(header), 2):
        vout = float(re.search(r"Vout=([\d.]+)", header[i]).group(1))
        x = np.array([float(r[i]) for r in rows])
        y = np.array([float(r[i + 1]) for r in rows])
        data[vout] = (x, y)
    return data


eff = load_efficiency(CSV_PATH)

colors = [f"tab:{c}" for c in ["red", "blue", "green", "purple"]]

# Two stacked panels sharing the Iload axis
fig, (ax_duty, ax_eff) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

for i, vout in enumerate(Vout):
    ax_duty.plot(Iload, [fx(vout, iload) for iload in Iload],
                 color=colors[i], label=f"Vout={vout:.2f}V")

for i, vout in enumerate(sorted(eff)):
    x, y = eff[vout]
    ax_eff.plot(x, y, color=colors[i], linestyle="--",
                marker="o", markersize=4, label=f"Vout={vout:.2f}V")

ax_duty.set_ylabel("Duty Cycle")
ax_eff.set_ylabel("Efficiency (%)")
ax_eff.set_xlabel("Iload (A)")

for ax in (ax_duty, ax_eff):
    ax.grid(True, alpha=0.3)

ax_duty.legend(title="Duty Cycle", loc="best", fontsize=8)
ax_eff.legend(title="Efficiency", loc="best", fontsize=8)

fig.tight_layout()
plt.show()
