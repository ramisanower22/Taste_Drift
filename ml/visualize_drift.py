import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"

timeline = pd.read_csv(
    PROCESSED / "taste_drift_timeline.csv"
)


# =========================
# CREATE LABELS
# =========================

timeline["transition"] = (
    "P" + timeline["from_period"].astype(str)
    + " → P"
    + timeline["to_period"].astype(str)
)


# =========================
# GRAPH
# =========================

plt.figure(figsize=(9, 5))

plt.plot(
    timeline["transition"],
    timeline["drift"],
    marker="o",
    linewidth=2
)

plt.title("Taste Drift Over Time")
plt.xlabel("Taste Period Transition")
plt.ylabel("Drift Score")

plt.grid(alpha=0.3)

plt.tight_layout()


# =========================
# SAVE
# =========================

output = PROCESSED / "taste_drift_graph.png"

plt.savefig(
    output,
    dpi=300
)

plt.show()

print("\n✅ TASTE DRIFT GRAPH CREATED")
print("Saved to:")
print(output)