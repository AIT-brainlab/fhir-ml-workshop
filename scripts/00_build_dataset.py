"""
00 - Build the workshop data  (INSTRUCTOR ONLY - students do NOT run this)

Produces two things from the Breast Cancer Wisconsin (Diagnostic) dataset
that ships inside scikit-learn, so the workshop needs no internet access:

  data/patients.csv   the flat table used for modelling (all 569 patients)
  data/fhir/*.json    one FHIR R4 Bundle per patient - the shape the data
                      would arrive in from a real hospital system

Every patient is exported, so scripts/01_fhir_to_table.py rebuilds the whole
of patients.csv from the Bundles. Nothing in the workshop trains on rows the
students did not flatten themselves.

Run once before the class:
    uv run python scripts/00_build_dataset.py
"""

import json
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "patients.csv"
FHIR_DIR = ROOT / "data" / "fhir"

BASE = "http://fhir-ml-workshop.example.org/fhir"
CODE_SYSTEM = f"{BASE}/CodeSystem/fna-morphometry"
DX_SYSTEM = f"{BASE}/CodeSystem/breast-mass-diagnosis"
MRN_SYSTEM = f"{BASE}/sid/workshop-mrn"
EFFECTIVE = "1995-06-15"   # synthetic; see data/DATA_CARD.md

# One patient is deliberately shipped with a missing Observation, so students
# see a NaN appear when they flatten it. Real FHIR extracts always have gaps.
INCOMPLETE_PATIENT = "P0010"
INCOMPLETE_DROPS = ["texture"]

RENAME = {
    "mean radius": "radius",
    "mean texture": "texture",
    "mean perimeter": "perimeter",
    "mean area": "area",
    "mean smoothness": "smoothness",
    "mean compactness": "compactness",
    "mean concavity": "concavity",
    "mean concave points": "concave_points",
    "mean symmetry": "symmetry",
    "mean fractal dimension": "fractal_dimension",
}

# display text and unit for each measurement.
# NOTE: these are research morphometry measurements taken from a digitised
# image, not standard lab tests, so no LOINC code exists for them. We publish
# them under a local CodeSystem rather than inventing LOINC codes, and the
# pixel-based ones carry a plain unit string rather than a fake UCUM code.
MEASUREMENTS = {
    "radius": ("Nucleus radius (mean)", "pixel", None),
    "texture": ("Nucleus texture, SD of grey-scale (mean)", "1", "1"),
    "perimeter": ("Nucleus perimeter (mean)", "pixel", None),
    "area": ("Nucleus area (mean)", "pixel2", None),
    "smoothness": ("Nucleus smoothness (mean)", "1", "1"),
    "compactness": ("Nucleus compactness (mean)", "1", "1"),
    "concavity": ("Nucleus concavity (mean)", "1", "1"),
    "concave_points": ("Nucleus concave points (mean)", "1", "1"),
    "symmetry": ("Nucleus symmetry (mean)", "1", "1"),
    "fractal_dimension": ("Nucleus fractal dimension (mean)", "1", "1"),
}


def build_csv() -> pd.DataFrame:
    frame = load_breast_cancer(as_frame=True).frame
    df = frame[list(RENAME)].rename(columns=RENAME).round(5)

    # scikit-learn encodes 0 = malignant, 1 = benign.
    # We flip it so that 1 = malignant = the condition we want to DETECT.
    df.insert(0, "patient_id", [f"P{i:04d}" for i in range(1, len(df) + 1)])
    df["malignant"] = 1 - frame["target"]

    CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV, index=False)
    print(f"Wrote {CSV.relative_to(ROOT)}  ({len(df)} rows, {df['malignant'].sum()} malignant)")
    return df


def observation(pid: str, feature: str, value: float) -> dict:
    display, unit, ucum = MEASUREMENTS[feature]
    quantity = {"value": float(value), "unit": unit}
    if ucum:  # only attach a UCUM code where a real one exists
        quantity["system"] = "http://unitsofmeasure.org"
        quantity["code"] = ucum

    return {
        "fullUrl": f"{BASE}/Observation/{pid}-{feature}",
        "resource": {
            "resourceType": "Observation",
            "id": f"{pid}-{feature}",
            "status": "final",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "imaging",
                            "display": "Imaging",
                        }
                    ]
                }
            ],
            "code": {
                "coding": [{"system": CODE_SYSTEM, "code": feature, "display": display}],
                "text": display,
            },
            "subject": {"reference": f"Patient/{pid}"},
            "effectiveDateTime": EFFECTIVE,
            "valueQuantity": quantity,
        },
    }


def bundle_for(row: pd.Series) -> dict:
    pid = row["patient_id"]
    malignant = int(row["malignant"]) == 1

    entries = [
        {
            "fullUrl": f"{BASE}/Patient/{pid}",
            "resource": {
                "resourceType": "Patient",
                "id": pid,
                # No name, gender or birthDate: the source dataset carries no
                # demographics at all. That absence is itself a finding - you
                # cannot audit this model for bias.
                "identifier": [{"system": MRN_SYSTEM, "value": pid}],
            },
        }
    ]

    dropped = INCOMPLETE_DROPS if pid == INCOMPLETE_PATIENT else []
    for feature in MEASUREMENTS:
        if feature in dropped:
            continue
        entries.append(observation(pid, feature, row[feature]))

    entries.append(
        {
            "fullUrl": f"{BASE}/Condition/{pid}-dx",
            "resource": {
                "resourceType": "Condition",
                "id": f"{pid}-dx",
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                        }
                    ]
                },
                "verificationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                            "code": "confirmed",
                        }
                    ]
                },
                # In production this would be SNOMED CT. Mapping a local
                # pathology vocabulary onto SNOMED is a project in itself.
                "code": {
                    "coding": [
                        {
                            "system": DX_SYSTEM,
                            "code": "malignant" if malignant else "benign",
                            "display": (
                                "Malignant breast mass (biopsy confirmed)"
                                if malignant
                                else "Benign breast mass (biopsy confirmed)"
                            ),
                        }
                    ]
                },
                "subject": {"reference": f"Patient/{pid}"},
                "recordedDate": EFFECTIVE,
            },
        }
    )

    return {
        "resourceType": "Bundle",
        "id": f"bundle-{pid}",
        "type": "collection",
        "timestamp": f"{EFFECTIVE}T14:00:00+07:00",
        "entry": entries,
    }


def build_fhir(df: pd.DataFrame) -> None:
    # Every patient, so Step 1 reconstructs patients.csv exactly.
    sample = df.sort_values("patient_id")

    FHIR_DIR.mkdir(parents=True, exist_ok=True)
    for old in FHIR_DIR.glob("*.json"):
        old.unlink()

    for _, row in sample.iterrows():
        path = FHIR_DIR / f"{row['patient_id']}.json"
        path.write_text(json.dumps(bundle_for(row), indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(sample)} bundles to {FHIR_DIR.relative_to(ROOT)}/")
    print(f"  {INCOMPLETE_PATIENT} is missing {INCOMPLETE_DROPS} on purpose.")


def main() -> None:
    df = build_csv()
    build_fhir(df)


if __name__ == "__main__":
    main()
