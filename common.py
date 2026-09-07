"""
Shared code used by the training scripts AND by both apps.

Keeping feature engineering in ONE place is the whole point of this file:
if training and serving compute features differently, the model silently
gets worse in production. In health care that is a patient-safety bug.
"""

import warnings
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.exceptions import InconsistentVersionWarning

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "patients.csv"
MODEL_PATH = ROOT / "models" / "model.joblib"

TARGET = "malignant"

# The probability above which a patient is called malignant.
# 0.5 is a default, not a law. Lowering it catches more tumours and raises
# more false alarms. Every script and app below lets you change it at run time.
DEFAULT_THRESHOLD = 0.5

# The 10 measurements a technician actually records from the slide.
RAW_FEATURES = [
    "radius",
    "texture",
    "perimeter",
    "area",
    "smoothness",
    "compactness",
    "concavity",
    "concave_points",
    "symmetry",
    "fractal_dimension",
]

# Shown in the app so the sliders read like a lab form.
LABELS = {
    "radius": "Radius (mean distance centre to edge)",
    "texture": "Texture (variation in grey-scale)",
    "perimeter": "Perimeter",
    "area": "Area",
    "smoothness": "Smoothness (local variation in radius)",
    "compactness": "Compactness",
    "concavity": "Concavity (severity of concave portions)",
    "concave_points": "Concave points (number of concave portions)",
    "symmetry": "Symmetry",
    "fractal_dimension": "Fractal dimension (coastline approximation)",
}


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Feature engineering: two clinically motivated shape ratios.

    Both describe SHAPE independently of SIZE - a small but very irregular
    mass is still worrying, and raw size alone would hide that.
    """
    out = df.copy()
    out["compactness_ratio"] = out["perimeter"] ** 2 / out["area"]
    out["concavity_per_radius"] = out["concavity"] / out["radius"]
    return out


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA)


def load_model() -> dict:
    """Returns the bundle saved by scripts/03_train_model.py."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "models/model.joblib not found.\n"
            "Run this first:  uv run python scripts/03_train_model.py"
        )
    with warnings.catch_warnings():
        # A .joblib written by a different scikit-learn build unpickles with a
        # warning and then fails later, deep inside predict, with something
        # unreadable. Turn that into an error here, where we can say what to do.
        warnings.simplefilter("error", InconsistentVersionWarning)
        try:
            return joblib.load(MODEL_PATH)
        except InconsistentVersionWarning as exc:
            raise RuntimeError(
                f"models/model.joblib was written by a different scikit-learn "
                f"({exc.original_sklearn_version}, you have "
                f"{sklearn.__version__}). It will not predict correctly.\n"
                "Delete it and retrain — it takes about 20 seconds:\n"
                "  rm models/model.joblib\n"
                "  uv run python scripts/03_train_model.py"
            ) from None


def predict_one(
    bundle: dict, measurements: dict, threshold: float = DEFAULT_THRESHOLD
) -> dict:
    """Score a single patient from the 10 raw measurements.

    `threshold` is the probability at which we call a tumour malignant.
    Move it and the same model gives a different answer for the same patient.
    """
    row = pd.DataFrame([{k: float(measurements[k]) for k in RAW_FEATURES}])
    row = add_features(row)[bundle["feature_names"]]

    probability = float(bundle["pipeline"].predict_proba(row)[0, 1])

    # bands sit either side of whatever threshold is in force
    high = threshold + (1 - threshold) * 0.4
    low = threshold * 0.6
    if probability >= high:
        band = "HIGH"
    elif probability >= low:
        band = "MEDIUM"
    else:
        band = "LOW"

    return {
        "prediction": "malignant" if probability >= threshold else "benign",
        "probability_malignant": round(probability, 4),
        "risk_band": band,
        "threshold": round(float(threshold), 3),
        "model": bundle["model_name"],
    }


def feature_ranges() -> dict:
    """Min / max / median of each measurement, used to build the sliders."""
    df = load_dataset()
    return {
        f: {
            "min": float(df[f].min()),
            "max": float(df[f].max()),
            "median": float(df[f].median()),
        }
        for f in RAW_FEATURES
    }
