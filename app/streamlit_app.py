"""
STEP 5a - DEPLOY LOCALLY (browser app)

    uv run streamlit run app/streamlit_app.py

Opens http://localhost:8501 - move the sliders, get a prediction.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from common import (
    DEFAULT_THRESHOLD,
    LABELS,
    RAW_FEATURES,
    TARGET,
    add_features,
    feature_ranges,
    load_dataset,
    load_model,
    predict_one,
)
from fhir_out import submission

st.set_page_config(page_title="Tumour Risk Assistant", page_icon="+", layout="wide")

BAND_COLOR = {"HIGH": "#C64B4B", "MEDIUM": "#D9A03C", "LOW": "#4C9F70"}


@st.cache_resource
def get_model():
    return load_model()


@st.cache_data
def get_ranges():
    return feature_ranges()


@st.cache_data
def get_examples():
    """One real malignant and one real benign patient, for the preset buttons."""
    df = load_dataset()
    return {
        "malignant": df[df[TARGET] == 1].iloc[0][RAW_FEATURES].to_dict(),
        "benign": df[df[TARGET] == 0].iloc[0][RAW_FEATURES].to_dict(),
    }


@st.cache_data
def cohort_probabilities(_feature_names):
    """Score all 569 patients once, so the threshold slider can show its cost."""
    df = load_dataset()
    scored = add_features(df)[list(_feature_names)]
    proba = get_model()["pipeline"].predict_proba(scored)[:, 1]
    return proba, df[TARGET].to_numpy()


st.title("Tumour Risk Assistant")

try:
    bundle = get_model()
except FileNotFoundError as err:
    st.error(str(err))
    st.stop()

ranges = get_ranges()
examples = get_examples()

# Slider values live in session_state so the preset buttons can change them.
for _f in RAW_FEATURES:
    st.session_state.setdefault(_f, float(ranges[_f]["median"]))

# ---------------------------------------------------------------- presets
st.sidebar.header("Load a real patient")
st.sidebar.write("Start from an actual record in the dataset, then adjust.")
if st.sidebar.button("Patient with a malignant tumour"):
    st.session_state.update({k: float(v) for k, v in examples["malignant"].items()})
if st.sidebar.button("Patient with a benign tumour"):
    st.session_state.update({k: float(v) for k, v in examples["benign"].items()})
if st.sidebar.button("Reset to dataset median"):
    st.session_state.update({f: float(ranges[f]["median"]) for f in RAW_FEATURES})

st.sidebar.divider()
st.sidebar.subheader("Decision threshold")
threshold = st.sidebar.slider(
    "Call it malignant above this probability",
    min_value=0.05, max_value=0.95,
    value=float(bundle.get("threshold", DEFAULT_THRESHOLD)),
    step=0.05,
    key="decision_threshold",
)

proba_all, y_all = cohort_probabilities(tuple(bundle["feature_names"]))
flagged = int((proba_all >= threshold).sum())
missed = int(((proba_all < threshold) & (y_all == 1)).sum())
alarms = int(((proba_all >= threshold) & (y_all == 0)).sum())

st.sidebar.write(
    f"Across all **{len(y_all)}** patients in the dataset, this threshold would:"
)
def _plural(n: int, one: str, many: str) -> str:
    # at threshold 0.80 this drops to a single patient, and "1 patients" on a
    # projector is the kind of detail a room notices instead of the number
    return one if n == 1 else many


st.sidebar.write(f"- flag **{flagged}** for biopsy")
st.sidebar.write(f"- miss **{missed}** {_plural(missed, 'tumour', 'tumours')}")
st.sidebar.write(
    f"- falsely alarm **{alarms}** healthy "
    f"{_plural(alarms, 'patient', 'patients')}"
)
st.sidebar.caption(
    "Move the slider. The model never changes — only the line you draw through it. "
    "Patient P0216 has a real tumour the model misses at 0.50 and catches at 0.20."
)

st.sidebar.divider()
st.sidebar.subheader("Model in use")
st.sidebar.write(f"**{bundle['model_name']}**")
for metric, value in bundle["metrics"].items():
    if isinstance(value, float):
        st.sidebar.write(f"{metric}: `{value:.3f}`")
    else:
        st.sidebar.write(f"{metric}: `{value}`")

# ---------------------------------------------------------------- sliders
left, right = st.columns([3, 2], gap="large")

with left:
    st.subheader("Measurements from the cell sample")
    measurements = {}
    cols = st.columns(2)
    for i, feature in enumerate(RAW_FEATURES):
        info = ranges[feature]
        step = (info["max"] - info["min"]) / 200
        measurements[feature] = cols[i % 2].slider(
            LABELS[feature],
            min_value=float(info["min"]),
            max_value=float(info["max"]),
            step=float(step),
            key=feature,
        )

# ------------------------------------------------------------- prediction
with right:
    st.subheader("Model output")
    result = predict_one(bundle, measurements, threshold=threshold)
    probability = result["probability_malignant"]
    band = result["risk_band"]

    st.markdown(
        f"<div style='padding:18px;border-radius:10px;"
        f"background:{BAND_COLOR[band]};color:white;text-align:center'>"
        f"<div style='font-size:15px;opacity:.85'>RISK BAND</div>"
        f"<div style='font-size:38px;font-weight:700'>{band}</div></div>",
        unsafe_allow_html=True,
    )
    st.metric("Probability of malignancy", f"{probability:.1%}")
    st.progress(probability)
    st.write(
        f"Classified as **{result['prediction']}** "
        f"because {probability:.1%} "
        f"{'≥' if probability >= threshold else '<'} the {threshold:.0%} threshold."
    )

    st.divider()
    st.markdown(
        "**Read this before you trust the number**\n\n"
        "- The model was trained on 569 patients from one hospital in the 1990s.\n"
        "- It has never seen a patient from this country or this decade.\n"
        "- It predicts a *label in a dataset*, not a *diagnosis*.\n"
        "- A clinician remains responsible for the decision."
    )

with st.expander("What the model actually received (after feature engineering)"):
    from common import add_features

    st.dataframe(
        add_features(pd.DataFrame([measurements]))[bundle["feature_names"]].T.rename(
            columns={0: "value"}
        )
    )

# --------------------------------------------------- back into the record
# This is the return half of the morning. Step 1 read FHIR in; this writes
# FHIR out, so the room can see that "the AI result goes into the chart" is
# one ordinary HTTP request carrying one ordinary resource.
st.divider()
st.subheader("Send this result back to the hospital record")

col_btn, col_note = st.columns([1, 3])
with col_btn:
    submit = st.button("Send to record", type="primary")
with col_note:
    st.caption(
        "Nothing leaves your laptop — the request below is built and shown, "
        "not sent. hospital.example.org does not exist."
    )

if submit:
    payload = submission(result, patient_id="P0001")
    req = payload["request"]
    st.code(
        f"{req['method']} {req['url']}\n"
        f"Content-Type: {req['headers']['Content-Type']}",
        language="http",
    )
    st.json(payload["body"])

    st.markdown(
        "**Read the resource, not just the number**\n\n"
        "- `RiskAssessment`, not `Condition`. A score, not a diagnosis.\n"
        "- `performer` points at a **Device**, so the record always shows that "
        "software produced this line, never a clinician.\n"
        "- `basis` lists the ten `Observation` ids the score came from, so a "
        "year from now somebody can audit which numbers produced it.\n"
        "- `rationale` records the threshold, because the same probability "
        "gives a different verdict at a different setting."
    )
    st.warning(
        "The diagnosis of record is still a `Condition` written by the "
        "responsible clinician. This app never creates one, and it must not."
    )
