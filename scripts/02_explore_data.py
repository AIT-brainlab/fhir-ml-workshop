"""
EXPLORE THE DATASET
Look at the data before you model it.

    uv run python scripts/02_explore_data.py

Seven sections of profiling and two figures in reports/. Three of the sections
are checks rather than descriptions: a leakage tripwire, a look at how alike
the measurements are to each other, and the gap between the two groups. Those
are the ones that would change what you do next.
"""

import argparse
import itertools
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save figures to file instead of opening a window
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "patients.csv"
REPORTS = ROOT / "reports"

TARGET = "malignant"


def rule(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Profile the patient table.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    REPORTS.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    features = [c for c in df.columns if c not in ("patient_id", TARGET)]

    rule("1. WHAT IS IN THE FILE?")
    print(f"Rows (patients) : {len(df)}")
    print(f"Columns         : {len(df.columns)}")
    print(f"Features        : {len(features)}")
    print(f"Target          : '{TARGET}'  (1 = malignant, 0 = benign)")
    print("\nFirst 5 patients:")
    print(df.head().to_string(index=False))

    rule("2. IS ANYTHING MISSING?")
    missing = df.isna().sum()
    if missing.sum() == 0:
        print("No missing values.")
        print("Real clinical data is never this clean - our pipeline still")
        print("contains an imputer so it survives contact with real data.")
    else:
        print(missing[missing > 0].to_string())

    rule("3. IS THE DATASET BALANCED?")
    counts = df[TARGET].value_counts().sort_index()
    for label, n in counts.items():
        name = "malignant" if label == 1 else "benign"
        print(f"  {name:<10} {n:>4}  ({n / len(df):.1%})")
    majority = counts.max() / len(df)
    print(f"\nA model that always predicts the majority class gets {majority:.1%} accuracy.")
    print("This is why accuracy alone is a bad metric in health care.")

    rule("4. HOW DO THE FEATURES BEHAVE?")
    print(df[features].describe().T[["mean", "std", "min", "max"]].round(3).to_string())
    print("\nNote the scales: 'area' is in the hundreds, 'smoothness' is ~0.1.")
    print("Models that use distance need these scaled - that is what StandardScaler does.")

    rule("5. WHICH FEATURES SEPARATE THE TWO GROUPS?")
    corr = df[features + [TARGET]].corr()[TARGET].drop(TARGET).sort_values(ascending=False)
    print(corr.round(3).to_string())
    print(f"\nStrongest signal: '{corr.index[0]}' at {corr.iloc[0]:.3f}")

    LEAK = 0.95
    suspects = corr[corr.abs() > LEAK]
    if suspects.empty:
        print(f"\nLeakage check: nothing correlates with the answer above {LEAK:.2f}.")
        print("That is what you want to see. A column at 0.99 is not a good")
        print("feature - it is usually the answer itself, arriving early: a")
        print("treatment code, a billing code, a follow-up date. Run this check")
        print("on every dataset before you are pleased with a result.")
    else:
        print(f"\nLEAKAGE WARNING: {', '.join(suspects.index)} sit above {LEAK:.2f}.")
        print("Find out where each one comes from before training anything.")

    rule("6. HOW FAR APART ARE THE TWO GROUPS?")
    grp = df.groupby(TARGET)[features].mean().T
    grp.columns = ["benign", "malignant"]
    grp["x"] = (grp["malignant"] / grp["benign"]).round(2)
    grp = grp.sort_values("x", ascending=False)
    print(grp.round(3).to_string())
    print("\nRead the right-hand column: malignant nuclei are about")
    print(f"{grp['x'].iloc[0]:.1f}x the {grp.index[0]} of benign ones. A clinician can")
    print("argue with a number like that. They cannot argue with a correlation")
    print("coefficient, which is why this table is the one to show them.")

    rule("7. HOW ALIKE ARE THE MEASUREMENTS?")
    cm = df[features].corr().abs()
    top = sorted(
        ((a, b, cm.loc[a, b]) for a, b in itertools.combinations(features, 2)),
        key=lambda t: t[2], reverse=True)[:5]
    for a, b, r in top:
        print(f"  {a:<20} {b:<20} r = {r:.3f}")
    print("\nThe top pairs are not three measurements. They are one measurement")
    print("written three ways - a bigger nucleus has a bigger radius, a bigger")
    print("perimeter and a bigger area, necessarily.")
    print("\nKeep this in mind when 03 lets you drop the two engineered columns")
    print("and nothing changes. compactness_ratio is perimeter squared over area:")
    print("built out of two columns the model already had, and already knew were")
    print("telling it the same thing.")

    # ---- figure 1: class balance -------------------------------------------
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.bar(["benign", "malignant"], [counts.get(0, 0), counts.get(1, 0)],
           color=["#4C9F70", "#C64B4B"])
    ax.set_title("Class balance")
    ax.set_ylabel("patients")
    fig.tight_layout()
    fig.savefig(REPORTS / "explore_class_balance.png", dpi=150)
    plt.close(fig)

    # ---- figure 2: how alike the measurements are ---------------------------
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm.values, cmap="Greens", vmin=0, vmax=1)
    ax.set_xticks(range(len(features)), features, rotation=90, fontsize=8)
    ax.set_yticks(range(len(features)), features, fontsize=8)
    for i in range(len(features)):
        for j in range(len(features)):
            v = cm.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6,
                    color="white" if v > 0.6 else "#333333")
    ax.set_title("How alike are the measurements?  (|correlation|)", fontsize=11)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(REPORTS / "explore_correlations.png", dpi=150)
    plt.close(fig)

    rule("DONE")
    print("Figures  -> reports/explore_class_balance.png")
    print("         -> reports/explore_correlations.png")
    print("\nDiscuss with your group:")
    print("  - Which feature would a clinician actually be able to measure?")
    print("  - If a column recorded the treatment given, could we use it? (No - leakage.)")
    print("\nNext:  uv run python scripts/03_train_model.py")


if __name__ == "__main__":
    main()
