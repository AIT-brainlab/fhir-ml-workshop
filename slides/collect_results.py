"""
Run the workshop for real and record every number the deck quotes.

    uv run python slides/collect_results.py

Writes slides/results.json. Nothing in the deck should contain a hand-typed
figure — build_from_template.py and make_figures.py both read this file, so a
change in the code shows up in the slides instead of quietly contradicting them.

Every seed is pinned (SEED below, matching the scripts' defaults), so this
produces byte-identical numbers on every machine, every time.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    adjusted_rand_score,
    confusion_matrix,
    precision_score,
    recall_score,
    silhouette_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from common import DEFAULT_THRESHOLD, RAW_FEATURES, TARGET, add_features, load_dataset

SEED = 42
TEST_SIZE = 0.2
OUT = ROOT / "slides" / "results.json"

# The patient used for the threshold demonstration. Chosen because the model
# is genuinely uncertain about them, so the verdict flips with the threshold.
DEMO_LOW, DEMO_HIGH = 0.20, 0.50


def run(*args: str) -> str:
    """Run one of the workshop scripts and return its stdout."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / args[0]), *args[1:]],
        capture_output=True, text=True, cwd=ROOT, check=True,
    )
    return proc.stdout


def main() -> None:
    r: dict = {"seed": SEED, "test_size": TEST_SIZE, "threshold": DEFAULT_THRESHOLD}

    # -------------------------------------------------- 1. the FHIR bundles
    fhir_dir = ROOT / "data" / "fhir"
    bundles = sorted(fhir_dir.glob("*.json"))
    first = json.loads(bundles[0].read_text())
    kinds = [e["resource"]["resourceType"] for e in first["entry"]]
    r["fhir"] = {
        "n_bundles": len(bundles),
        "example_id": bundles[0].stem,
        "resources_in_example": len(kinds),
        "n_patient": kinds.count("Patient"),
        "n_observation": kinds.count("Observation"),
        "n_condition": kinds.count("Condition"),
    }

    # find the bundle that is deliberately short of an Observation
    incomplete = {}
    for f in bundles:
        b = json.loads(f.read_text())
        codes = [
            e["resource"]["code"]["coding"][0]["code"]
            for e in b["entry"]
            if e["resource"]["resourceType"] == "Observation"
        ]
        missing = [c for c in RAW_FEATURES if c not in codes]
        if missing:
            incomplete = {"patient": f.stem, "missing": missing[0]}
    r["fhir"]["incomplete"] = incomplete

    # ------------------------------------------------------- 2. the cohort
    df = load_dataset()
    n = len(df)
    n_mal = int(df[TARGET].sum())
    n_ben = n - n_mal
    r["cohort"] = {
        "n": n,
        "n_malignant": n_mal,
        "n_benign": n_ben,
        "pct_malignant": round(100 * n_mal / n, 1),
        "pct_benign": round(100 * n_ben / n, 1),
        "n_features_raw": len(RAW_FEATURES),
    }

    # ------------------------------------------------------- 3. the models
    d = add_features(df)
    feature_names = [c for c in d.columns if c not in ("patient_id", TARGET)]
    X, y = d[feature_names], d[TARGET]
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED
    )
    r["cohort"]["n_features_total"] = len(feature_names)
    r["cohort"]["n_test"] = len(X_te)

    # a stale baseline from an older version of the code would make every
    # ablation diff below meaningless, so start from nothing
    (ROOT / "reports" / "baseline.json").unlink(missing_ok=True)
    run("03_train_model.py")                      # fits and saves models/model.joblib
    bundle = joblib.load(ROOT / "models" / "model.joblib")

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    def fit(model):
        p = Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler()), ("model", model)])
        return p.fit(X_tr, y_tr)

    models = {
        "logit": fit(LogisticRegression(max_iter=2000, random_state=SEED)),
        "forest": fit(RandomForestClassifier(n_estimators=300, random_state=SEED,
                                             n_jobs=-1)),
    }
    names = {"logit": "Logistic Regression", "forest": "Random Forest"}

    r["models"] = {}
    for key, pipe in models.items():
        proba = pipe.predict_proba(X_te)[:, 1]
        pred = (proba >= DEFAULT_THRESHOLD).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_te, pred, labels=[0, 1]).ravel()
        from sklearn.metrics import accuracy_score, roc_auc_score
        r["models"][key] = {
            "name": names[key],
            "accuracy": round(float(accuracy_score(y_te, pred)), 3),
            "precision": round(float(precision_score(y_te, pred, zero_division=0)), 3),
            "recall": round(float(recall_score(y_te, pred, zero_division=0)), 3),
            "roc_auc": round(float(roc_auc_score(y_te, proba)), 3),
            "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
            "missed": int(fn),
            "false_alarms": int(fp),
            "detected": int(tp),
        }

    r["selected"] = max(r["models"], key=lambda k: r["models"][k]["recall"])

    # ---------------------------------------- 4. thresholds across the cohort
    proba_all = bundle["pipeline"].predict_proba(add_features(df)[bundle["feature_names"]])[:, 1]
    y_all = df[TARGET].to_numpy()
    r["threshold_cohort"] = {}
    for t in (0.20, 0.50, 0.80):
        flagged = int((proba_all >= t).sum())
        r["threshold_cohort"][f"{t:.2f}"] = {
            "flagged": flagged,
            "missed": int(((proba_all < t) & (y_all == 1)).sum()),
            "false_alarms": int(((proba_all >= t) & (y_all == 0)).sum()),
        }

    # ----------------------------- 5. the patient whose verdict flips, if any
    flip = None
    for i in np.argsort(proba_all):
        p = float(proba_all[i])
        if DEMO_LOW <= p < DEMO_HIGH and y_all[i] == 1:
            flip = {
                "patient": str(df["patient_id"].iloc[i]),
                "probability": round(p, 4),
                "actual": "malignant",
                "low": DEMO_LOW,
                "high": DEMO_HIGH,
            }
            break
    r["flip_case"] = flip

    # ---------------------------------------------------------- 6. clustering
    feats = [c for c in df.columns if c not in ("patient_id", TARGET)]
    Xs = StandardScaler().fit_transform(df[feats])
    r["clustering"] = {}
    for k in (2, 3, 5):
        cl = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(Xs)
        r["clustering"][str(k)] = {
            "ari": round(float(adjusted_rand_score(y_all, cl)), 3),
            "silhouette": round(float(silhouette_score(Xs, cl)), 3),
        }

    # -------------------------------------- 7. cross-validation on the train half
    # 03_train_model.py cross-validates before it touches the test set. The deck
    # quotes the spread, because one number from one split is not evidence.
    from sklearn.model_selection import cross_val_score
    r["cv"] = {}
    for key, model in (("logit", LogisticRegression(max_iter=2000, random_state=SEED)),
                       ("forest", RandomForestClassifier(n_estimators=300,
                                                         random_state=SEED, n_jobs=-1))):
        pipe = Pipeline([("impute", SimpleImputer(strategy="median")),
                         ("scale", StandardScaler()), ("model", model)])
        s = cross_val_score(pipe, X_tr, y_tr, cv=5, scoring="recall")
        r["cv"][key] = {"folds": 5, "mean": round(float(s.mean()), 3),
                        "std": round(float(s.std()), 3),
                        "low": round(float(s.min()), 3),
                        "high": round(float(s.max()), 3)}

    # ------------------------------------- 8. ablations the room runs as flags
    # These are read back out of the script's OWN section-6 diff table, not
    # re-implemented here. If the deck quoted a private re-fit it could disagree
    # with the terminal the students are looking at, which is the one number a
    # slide is never allowed to get wrong.
    r["ablations"] = {"model": names[r["selected"]],
                      "engineered_names": [c for c in feature_names
                                           if c not in RAW_FEATURES]}

    def ablate(key: str, *flags: str) -> None:
        out = run("03_train_model.py", *flags)
        table = out.split("WHAT YOUR SETTINGS DID")[1]
        got = {}
        for line in table.splitlines():
            parts = line.split()
            if len(parts) >= 4 and parts[0] in (
                "recall", "precision", "accuracy", "roc_auc", "missed",
                "false_alarms",
            ):
                base, now = parts[1], parts[2]
                cast = int if parts[0] in ("missed", "false_alarms") else float
                got[parts[0]] = {"baseline": cast(base), "now": cast(now),
                                 "delta": round(cast(now) - cast(base), 3)}
        if not got:
            raise RuntimeError(f"could not parse the diff table for {key}")
        r["ablations"][key] = got

    ablate("no_engineered", "--no-engineered")
    ablate("starved", "--test-size", "0.8")
    r["ablations"]["starved_test_size"] = 0.8
    starved_tr, starved_te = train_test_split(
        X, y, test_size=0.8, stratify=y, random_state=SEED)[:2]
    r["ablations"]["starved_n_train"] = len(starved_tr)
    r["ablations"]["starved_n_test"] = len(starved_te)

    run("03_train_model.py")   # leave models/model.joblib as the default fit

    # ------------------------------------------------------- 9. environment
    lock = (ROOT / "uv.lock").read_text()
    r["env"] = {
        "n_packages": lock.count("\n[[package]]"),
        "python": (ROOT / ".python-version").read_text().strip(),
    }

    OUT.write_text(json.dumps(r, indent=2) + "\n")
    print(json.dumps(r, indent=2))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
