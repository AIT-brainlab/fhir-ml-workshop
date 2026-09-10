"""
The return journey: a prediction, written back as FHIR.

Part 1 went FHIR Bundle -> table. This goes the other way: model output ->
a FHIR resource a hospital system could actually file against the patient.

The resource is a **RiskAssessment**, not a Condition, and that distinction is
the whole point of this file:

    RiskAssessment  a score, produced by a Device (software)   <- we write this
    Condition       a diagnosis, asserted by a Practitioner    <- we never write this

An AI adds information to the record. It does not acquire the authority to
diagnose. FHIR encodes that separation in the data model itself, through
`performer` pointing at a Device rather than a Practitioner - so anyone reading
the record later can always tell which lines a machine wrote.
"""

from datetime import datetime, timezone

from common import RAW_FEATURES

# Where a real deployment would POST this. Fictional host on purpose.
FHIR_BASE = "https://hospital.example.org/fhir"
MODEL_DEVICE_ID = "tumour-risk-model"

# Our three bands mapped onto the code system FHIR expects here.
# http://terminology.hl7.org/CodeSystem/risk-probability
QUALITATIVE = {"LOW": "low", "MEDIUM": "moderate", "HIGH": "high"}

# SNOMED CT concept for the thing being predicted.
OUTCOME = {
    "system": "http://snomed.info/sct",
    "code": "254837009",
    "display": "Malignant neoplasm of breast",
}


def observation_refs(patient_id: str) -> list[dict]:
    """The ten Observations the score was derived from.

    In a real deployment these are the resource ids the server handed you.
    Recording them is what makes the score auditable: a year from now somebody
    can ask which numbers produced this and actually find out.
    """
    return [
        {"reference": f"Observation/{patient_id}-{feature}"}
        for feature in RAW_FEATURES
    ]


def _device(model_name: str, version: str) -> dict:
    """The software, described as a Device so it can be the performer."""
    return {
        "resourceType": "Device",
        "id": MODEL_DEVICE_ID,
        "status": "active",
        "manufacturer": "Health AI workshop",
        "deviceName": [{"name": f"Tumour Risk Assistant ({model_name})",
                        "type": "model-name"}],
        "version": [{"value": version}],
        "note": [{"text": "Teaching prototype. Not a medical device, not "
                          "clinically validated, must not be used to make "
                          "decisions about a real patient."}],
    }


def risk_assessment(
    result: dict,
    patient_id: str = "P0001",
    *,
    when: str | None = None,
    model_version: str = "0.1.0",
) -> dict:
    """Build the RiskAssessment for one prediction from `common.predict_one`.

    `when` defaults to now; pass a fixed value when the output has to be
    reproducible (the slide figures do).

    Key order is deliberate: the fields worth reading come first and the
    contained Device goes last, so anyone scrolling the JSON on a projector
    sees the answer before the boilerplate. FHIR does not care about order.
    """
    occurrence = when or datetime.now(timezone.utc).isoformat(timespec="seconds")
    probability = float(result["probability_malignant"])
    threshold = float(result["threshold"])

    return {
        "resourceType": "RiskAssessment",
        "status": "final",
        "subject": {"reference": f"Patient/{patient_id}"},
        "occurrenceDateTime": occurrence,
        # performer is a Device, not a Practitioner. This single line is what
        # tells every later reader that a machine wrote this, not a clinician.
        "performer": {"reference": f"#{MODEL_DEVICE_ID}"},
        "prediction": [
            {
                "outcome": {"coding": [OUTCOME], "text": OUTCOME["display"]},
                "probabilityDecimal": round(probability, 4),
                "qualitativeRisk": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/"
                                      "risk-probability",
                            "code": QUALITATIVE[result["risk_band"]],
                            "display": result["risk_band"].title(),
                        }
                    ]
                },
                "rationale": (
                    f"Reported as {result['prediction']} at a decision threshold "
                    f"of {threshold:.2f}. The threshold is a clinical setting, "
                    f"not a property of the model."
                ),
            }
        ],
        # the ten Observations this score came from, so it can be audited later
        "basis": observation_refs(patient_id),
        "method": {
            "text": f"{result['model']} on 10 FNA morphometry measurements "
                    f"plus 2 derived shape ratios"
        },
        "note": [
            {
                "text": "Decision support only. The diagnosis of record remains "
                        "the Condition asserted by the responsible clinician; "
                        "this resource does not create or amend one."
            }
        ],
        "contained": [_device(result["model"], model_version)],
    }


def submission(result: dict, patient_id: str = "P0001", **kwargs) -> dict:
    """What the app would actually send, request line included.

    Returned as a plain dict so the Streamlit app and the API can both show the
    same thing, and so students can see that "filing a result" is one ordinary
    HTTP request - the same shape as the GET that fetched the data this morning.
    """
    return {
        "request": {
            "method": "POST",
            "url": f"{FHIR_BASE}/RiskAssessment",
            "headers": {"Content-Type": "application/fhir+json"},
        },
        "body": risk_assessment(result, patient_id, **kwargs),
    }
