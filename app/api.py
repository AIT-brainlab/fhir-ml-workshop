"""
STEP 5b - DEPLOY LOCALLY (REST API)

    uv run uvicorn app.api:app --reload

Then open http://127.0.0.1:8000/docs and press "Try it out" on /predict.

Every endpoint takes an optional ?threshold= between 0 and 1. Patient P0216
has a real, biopsy-confirmed malignant tumour. Ask for it twice:

    /sample/P0216?threshold=0.5   -> "benign"     the model misses it
    /sample/P0216?threshold=0.2   -> "malignant"  the model catches it

Add /fhir to either endpoint and the same answer comes back as a FHIR R4
RiskAssessment, which is what a hospital could actually file:

    /sample/P0216/fhir?threshold=0.2

Same patient, same model, same numbers. Only the line moved.

This is the shape a hospital IT team would actually integrate with:
JSON in, JSON out, over HTTP - exactly like a FHIR server.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from common import DEFAULT_THRESHOLD, RAW_FEATURES, load_dataset, load_model, predict_one
from fhir_out import risk_assessment

_bundle: dict | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Load the model once, when the server starts - not on every request."""
    global _bundle
    try:
        _bundle = load_model()
        print(f"[startup] Model loaded: {_bundle['model_name']}")
    except FileNotFoundError as err:
        print(f"\n[startup] {err}\n")
    yield


app = FastAPI(
    title="Breast Mass Risk API",
    description="Teaching prototype. Not a medical device.",
    version="0.1.0",
    lifespan=lifespan,
)


class Patient(BaseModel):
    """One cell-sample measurement set. Defaults are a real malignant case."""

    radius: float = Field(17.99, gt=0)
    texture: float = Field(10.38, gt=0)
    perimeter: float = Field(122.8, gt=0)
    area: float = Field(1001.0, gt=0)
    smoothness: float = Field(0.1184, gt=0)
    compactness: float = Field(0.2776, ge=0)
    concavity: float = Field(0.3001, ge=0)
    concave_points: float = Field(0.1471, ge=0)
    symmetry: float = Field(0.2419, gt=0)
    fractal_dimension: float = Field(0.07871, gt=0)


@app.get("/")
def root() -> dict:
    return {
        "service": "Breast Mass Risk API",
        "status": "model loaded" if _bundle else "MODEL MISSING - run scripts/03_train_model.py",
        "try_this": "open /docs in your browser",
        "tip": "add ?threshold=0.2 to /predict or /sample/{id} and compare",
        "expects": RAW_FEATURES,
    }


@app.get("/health")
def health() -> dict:
    if _bundle is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    return {"ok": True, "model": _bundle["model_name"], "metrics": _bundle["metrics"]}


@app.post("/predict")
def predict(patient: Patient, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Score one patient. Change ?threshold= and the same numbers get a
    different verdict — the model is not retrained, only the line moves."""
    if _bundle is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run: uv run python scripts/03_train_model.py",
        )
    if not 0.0 < threshold < 1.0:
        raise HTTPException(status_code=422, detail="threshold must be between 0 and 1")
    return predict_one(_bundle, patient.model_dump(), threshold=threshold)


@app.get("/sample/{patient_id}")
def sample(patient_id: str, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Score a patient that already exists in the dataset, e.g. /sample/P0001."""
    if _bundle is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    if not 0.0 < threshold < 1.0:
        raise HTTPException(status_code=422, detail="threshold must be between 0 and 1")
    df = load_dataset()
    match = df[df["patient_id"] == patient_id.upper()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"No patient '{patient_id}'.")

    row = match.iloc[0]
    result = predict_one(_bundle, row[RAW_FEATURES].to_dict(), threshold=threshold)
    result["actual_diagnosis"] = "malignant" if row["malignant"] == 1 else "benign"
    result["patient_id"] = row["patient_id"]
    return result


# ------------------------------------------------ the same answer, as FHIR
# Everything above returns whatever JSON we felt like inventing. A hospital
# cannot file that. These two return a real RiskAssessment instead — the
# return half of the morning: FHIR in at Part 1, FHIR out here.


@app.post("/predict/fhir")
def predict_fhir(patient: Patient, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """The same prediction as /predict, as a FHIR R4 RiskAssessment.

    Compare the two responses side by side. The numbers are identical; only
    one of them can be filed against a patient.
    """
    if _bundle is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    if not 0.0 < threshold < 1.0:
        raise HTTPException(status_code=422, detail="threshold must be between 0 and 1")
    result = predict_one(_bundle, patient.model_dump(), threshold=threshold)
    return risk_assessment(result, patient_id="P0001")


@app.get("/sample/{patient_id}/fhir")
def sample_fhir(patient_id: str, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """A dataset patient, scored and returned as a FHIR RiskAssessment.

    Try /sample/P0216/fhir?threshold=0.5 then ?threshold=0.2 and read
    prediction[0].qualitativeRisk — the probability does not move, the risk
    band does, because a human chose a different line.
    """
    result = sample(patient_id, threshold)
    return risk_assessment(result, patient_id=result["patient_id"])
