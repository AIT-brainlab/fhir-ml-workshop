"""
STEP 2 - EXPLORE THE DATASET
Look at the data before you model it.

    uv run python scripts/02_explore_data.py

Prints a profile of the dataset and saves two figures into reports/.

Look at a different measurement without editing anything:

    --feature area        plot 'area' instead of the strongest feature
    --bins 12             coarser histogram
"""

import argparse
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
    p.add_argument("--feature", default=None,
                   help="which measurement to plot (default: the strongest one)")
    p.add_argument("--bins", type=int, default=30, help="histogram bins")
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
    print(f"\nStrongest signal: '{corr.index[0]}'")

    # ---- figure 1: class balance -------------------------------------------
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.bar(["benign", "malignant"], [counts.get(0, 0), counts.get(1, 0)],
           color=["#4C9F70", "#C64B4B"])
    ax.set_title("Class balance")
    ax.set_ylabel("patients")
    fig.tight_layout()
    fig.savefig(REPORTS / "01_class_balance.png", dpi=150)
    plt.close(fig)

    # ---- figure 2: distribution of one feature ------------------------------
    top = args.feature or corr.index[0]
    if top not in features:
        raise SystemExit(f"No such feature '{top}'. Choose from: {', '.join(features)}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df.loc[df[TARGET] == 0, top], bins=args.bins, alpha=0.7, label="benign", color="#4C9F70")
    ax.hist(df.loc[df[TARGET] == 1, top], bins=args.bins, alpha=0.7, label="malignant", color="#C64B4B")
    ax.set_xlabel(top)
    ax.set_ylabel("patients")
    ax.set_title(f"'{top}' by diagnosis")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "01_top_feature.png", dpi=150)
    plt.close(fig)

    rule("DONE")
    print("Figures saved to reports/01_class_balance.png and reports/01_top_feature.png")
    print("\nDiscuss with your group:")
    print("  - Which feature would a clinician actually be able to measure?")
    print("  - If a column recorded the treatment given, could we use it? (No - leakage.)")
    print("\nPlot a different measurement:")
    print("  uv run python scripts/02_explore_data.py --feature area")
    print("\nNext:  uv run python scripts/03_train_model.py")


if __name__ == "__main__":
    main()
