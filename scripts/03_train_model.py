"""
STEP 3 - TRAIN MODEL
Build a scikit-learn pipeline, train two models, compare them, keep the better one.

    uv run python scripts/03_train_model.py

Then change one thing and run it again. Every setting below is a command-line
flag, so you never have to edit the file:

    --threshold 0.30      call malignant above this probability   (default 0.50)
                          the Streamlit slider is the same setting, live
    --test-size 0.50      hold out half the patients instead of a fifth
    --seed 7              a different random split
    --forest-trees 20     cripple the Random Forest
    --no-engineered       drop the two engineered shape features
    --model logit         train only one model (logit | forest | both)

The first default run is remembered as the baseline. Every later run prints
what your change did to it.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from common import DEFAULT_THRESHOLD, RAW_FEATURES, TARGET, add_features, load_dataset

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"
REPORTS = ROOT / "reports"
BASELINE = REPORTS / "baseline.json"

DEFAULTS = dict(
    threshold=DEFAULT_THRESHOLD,
    test_size=0.2,
    seed=42,
    forest_trees=300,
    engineered=True,
    model="both",
)


def rule(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Train and compare two clinical prediction models.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--threshold", type=float, default=DEFAULTS["threshold"],
                   help="probability above which a tumour is called malignant")
    p.add_argument("--test-size", type=float, default=DEFAULTS["test_size"],
                   help="fraction of patients held out for testing")
    p.add_argument("--seed", type=int, default=DEFAULTS["seed"],
                   help="random seed for the split and the models")
    p.add_argument("--forest-trees", type=int, default=DEFAULTS["forest_trees"],
                   help="number of trees in the Random Forest")
    p.add_argument("--no-engineered", action="store_true",
                   help="train on the 10 measured features only")
    p.add_argument("--model", choices=["logit", "forest", "both"],
                   default=DEFAULTS["model"], help="which model(s) to train")
    return p.parse_args()


def changed(args) -> dict:
    """Which settings differ from the defaults?"""
    now = dict(
        threshold=args.threshold,
        test_size=args.test_size,
        seed=args.seed,
        forest_trees=args.forest_trees,
        engineered=not args.no_engineered,
        model=args.model,
    )
    return {k: (DEFAULTS[k], v) for k, v in now.items() if v != DEFAULTS[k]}


def build_pipeline(model) -> Pipeline:
    """Every step lives inside the pipeline, so it is applied identically
    to training data, test data, and to a new patient at prediction time."""
    return Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("model", model),
        ]
    )


def evaluate(name: str, pipe: Pipeline, X_test, y_test, threshold: float) -> dict:
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = (proba >= threshold).astype(int)

    scores = {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, proba),
    }
    print(f"\n--- {name} ---")
    for metric, value in scores.items():
        print(f"  {metric:<10} {value:.3f}")

    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    print(f"\n  Confusion matrix (test set, threshold {threshold:.2f})")
    print("                    predicted benign   predicted malignant")
    print(f"  actual benign     {tn:>16}   {fp:>19}")
    print(f"  actual malignant  {fn:>16}   {tp:>19}")
    print(f"\n  {fn} malignant tumour(s) were missed  <- false negatives")
    print(f"  {fp} healthy patient(s) falsely alarmed <- false positives")

    scores["missed"] = int(fn)
    scores["false_alarms"] = int(fp)
    return scores


def threshold_table(pipe, X_test, y_test) -> None:
    """The same fitted model, read off at several thresholds."""
    proba = pipe.predict_proba(X_test)[:, 1]
    print("\n  threshold   missed   false alarms   recall   precision")
    for t in (0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80):
        pred = (proba >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
        r = recall_score(y_test, pred, zero_division=0)
        p = precision_score(y_test, pred, zero_division=0)
        print(f"     {t:.2f}       {fn:>3}          {fp:>4}        {r:.3f}     {p:.3f}")
    print("\n  Nothing was retrained between those rows. One model, seven answers.")
    print("  Choosing the row is a clinical decision, not an engineering one.")


def compare_to_baseline(name: str, scores: dict, args) -> None:
    diffs = changed(args)
    if not diffs:
        BASELINE.write_text(json.dumps({"model": name, **scores}, indent=2))
        print("\nThis was a default run, so it is now the baseline other runs")
        print("are compared against  ->  reports/baseline.json")
        return

    print("\nYou changed:")
    for k, (was, now) in diffs.items():
        print(f"  {k:<14} {was}  ->  {now}")

    if not BASELINE.exists():
        print("\nNo baseline recorded yet. Run once with no flags to make one.")
        return

    base = json.loads(BASELINE.read_text())
    print(f"\nAgainst the baseline ({base['model']}):")
    print("  metric        baseline     now       change")
    for m in ("recall", "precision", "accuracy", "roc_auc"):
        d = scores[m] - base[m]
        arrow = "  " if abs(d) < 5e-4 else ("up" if d > 0 else "DOWN")
        print(f"  {m:<12} {base[m]:>8.3f} {scores[m]:>8.3f}   {d:+.3f} {arrow}")
    for m in ("missed", "false_alarms"):
        d = scores[m] - base[m]
        arrow = "  " if d == 0 else ("WORSE" if (m == "missed" and d > 0) else "")
        print(f"  {m:<12} {base[m]:>8} {scores[m]:>8}   {d:+d} {arrow}")


def main() -> None:
    args = parse_args()
    MODELS.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    # ---------------------------------------------------------------- data
    df = load_dataset()

    df = add_features(df)
    feature_names = [c for c in df.columns if c not in ("patient_id", TARGET)]
    if args.no_engineered:
        feature_names = list(RAW_FEATURES)
    X, y = df[feature_names], df[TARGET]

    rule("1. SPLIT THE DATA")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, stratify=y, random_state=args.seed
    )
    print(f"Training set : {len(X_train)} patients")
    print(f"Test set     : {len(X_test)} patients  (never seen during training)")
    print(f"Features     : {len(feature_names)}")
    print(f"Missing cells: {int(X.isna().sum().sum())}")
    print(f"Threshold    : {args.threshold:.2f}")
    print("\nstratify=y keeps the malignant rate the same in both halves.")

    # ------------------------------------------------------------- training
    rule("2. TRAIN")
    all_models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, random_state=args.seed),
        "Random Forest": RandomForestClassifier(
            n_estimators=args.forest_trees, random_state=args.seed, n_jobs=-1
        ),
    }
    wanted = {
        "logit": ["Logistic Regression"],
        "forest": ["Random Forest"],
        "both": list(all_models),
    }[args.model]
    candidates = {k: all_models[k] for k in wanted}

    fitted, results = {}, {}
    for name, model in candidates.items():
        pipe = build_pipeline(model)
        cv = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")
        pipe.fit(X_train, y_train)
        fitted[name] = pipe
        print(f"{name:<22} 5-fold CV ROC-AUC = {cv.mean():.3f} (+/- {cv.std():.3f})")

    # ----------------------------------------------------------- evaluation
    rule("3. EVALUATE ON THE HELD-OUT TEST SET")
    for name, pipe in fitted.items():
        results[name] = evaluate(name, pipe, X_test, y_test, args.threshold)

    rule("4. WHICH METRIC MATTERS HERE?")
    print("A false negative = a malignant tumour sent home untreated.")
    print("A false positive = an anxious patient and an unnecessary biopsy.")
    print("In screening we therefore optimise RECALL, not accuracy.")
    print("\nModel comparison by recall:")
    for name, s in results.items():
        print(f"  {name:<22} recall={s['recall']:.3f}  roc_auc={s['roc_auc']:.3f}"
              f"  missed={s['missed']}")

    best_name = max(results, key=lambda n: results[n]["recall"])
    best_pipe = fitted[best_name]
    print(f"\nSelected: {best_name}")

    rule("5. THE SAME MODEL AT DIFFERENT THRESHOLDS")
    threshold_table(best_pipe, X_test, y_test)

    rule("6. WHAT YOUR SETTINGS DID")
    compare_to_baseline(best_name, results[best_name], args)

    # ------------------------------------------------------------ roc curve
    fig, ax = plt.subplots(figsize=(5.5, 5))
    for name, pipe in fitted.items():
        fpr, tpr, _ = roc_curve(y_test, pipe.predict_proba(X_test)[:, 1])
        ax.plot(fpr, tpr, label=f"{name} (AUC={results[name]['roc_auc']:.3f})")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="random guessing")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate (recall)")
    ax.set_title("ROC curve - test set")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(REPORTS / "02_roc_curve.png", dpi=150)
    plt.close(fig)

    # ----------------------------------------------------------------- save
    joblib.dump(
        {
            "pipeline": best_pipe,
            "model_name": best_name,
            "feature_names": feature_names,
            "raw_features": RAW_FEATURES,
            "metrics": {k: v for k, v in results[best_name].items()},
            "threshold": args.threshold,
            "settings": vars(args),
        },
        MODELS / "model.joblib",
    )

    rule("DONE")
    print("Model saved  -> models/model.joblib")
    print("ROC curve    -> reports/02_roc_curve.png")
    print("\nTry one of these, then read section 6 again:")
    print("  uv run python scripts/03_train_model.py --no-engineered")
    print("  uv run python scripts/03_train_model.py --test-size 0.8")
    print("\nNext:  uv run streamlit run app/streamlit_app.py")


if __name__ == "__main__":
    main()
