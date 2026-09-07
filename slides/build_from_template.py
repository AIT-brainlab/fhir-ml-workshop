"""
Build the workshop deck on top of the AIT Canva template.

Input : ait-template.pptx  (29 pages exported from Canva)
Output: fhir-ml-workshop/slides/from-fhir-to-a-table.pptx

Keeps every AIT design element - photos, logo, colours, shapes - and only
swaps the placeholder text. Slides carrying rasterised dummy charts (16, 18)
are deliberately excluded: their numbers are baked into a PNG and cannot be
corrected, so putting our results next to them would be misleading.

Replacement strings are kept close to the original length so nothing overflows
the boxes the template designer sized.
"""

import copy
import json
from pathlib import Path

from pptx import Presentation
from pptx.text.text import _Paragraph

HERE = Path(__file__).resolve().parent
SRC = HERE / "ait-template.pptx"          # re-exported from Canva, not committed
DST = HERE / "from-fhir-to-a-table.pptx"

# new order -> original 1-indexed slide number
# Deck page -> where that page's text lives in TEXT below.
#
# An integer is a page of the original Canva export. A string is a page written
# after the export, by copying a layout already in the deck (slides/clone_page.py)
# and rewriting it. main() can only rebuild the integers; apply_results.py
# refreshes both, and is what you want in almost every case.
ORDER = [
    1, "recap", 3, 25, 23, 4, 2, 24, 6, 10, 20, 11,
    14, 7, "pipeline",          # what a model is, how it is judged, what is saved
    19, 5,
    "ablations", "starved",     # change one setting, then read what it cost
    8,
    17, "app_screen",           # the four moves, then what the screen looks like
    21, "fhir_back",            # and the result written back as FHIR
    22,
]

RESULTS = Path(__file__).resolve().parent / "results.json"


def load_results() -> dict:
    """Flatten slides/results.json into the names the templates below use.

    Produced by slides/collect_results.py from an actual run with a pinned
    seed. Nothing in this file should contain a hand-typed figure.
    """
    if not RESULTS.exists():
        raise SystemExit(
            "slides/results.json is missing.\n"
            "Run:  uv run python slides/collect_results.py"
        )
    r = json.loads(RESULTS.read_text())
    flat = {
        **r["fhir"], **r["cohort"], **r["env"],
        "inc_patient": r["fhir"]["incomplete"]["patient"],
        "inc_missing": r["fhir"]["incomplete"]["missing"],
    }
    for key in ("logit", "forest"):
        for k, v in r["models"][key].items():
            if not isinstance(v, dict):
                flat[f"{key}_{k}"] = v
    flat["flip_patient"] = r["flip_case"]["patient"]
    flat["flip_probability"] = r["flip_case"]["probability"]
    flat["flip_low"] = f'{r["flip_case"]["low"]:.2f}'
    flat["flip_high"] = f'{r["flip_case"]["high"]:.2f}'
    for k, v in r["clustering"].items():
        flat[f"ari_{k}"] = v["ari"]

    flat["n_train"] = r["cohort"]["n"] - r["cohort"]["n_test"]
    for t, v in r["threshold_cohort"].items():
        tag = round(float(t) * 100)
        for k, n in v.items():
            flat[f"cost_{tag}_{k}"] = n
    for k, v in r["cv"][r["selected"]].items():
        flat[f"cv_{k}"] = v

    # every flag the room is asked to turn, and what it really did
    abl = r["ablations"]
    flat["engineered_1"], flat["engineered_2"] = abl["engineered_names"]
    flat["starved_n_train"] = abl["starved_n_train"]
    flat["starved_n_test"] = abl["starved_n_test"]
    flat["missing_pct"] = int(abl["missing30_fraction"] * 100)
    flat["missing_column"] = abl["missing30_column"]
    for run_name in ("threshold30", "no_engineered", "missing30", "starved"):
        for metric, d in abl[run_name].items():
            if isinstance(d, dict):
                flat[f"{run_name}_{metric}"] = d["now"]
                flat[f"{run_name}_{metric}_was"] = d["baseline"]
    return flat

TEXT = {
    # ------------------------------------------------------------- 1 cover
    1: {
        "TextBox 22": "FROM FHIR\nTO A TABLE",
    },
    # ------------------------------ recap: what the morning actually said
    "recap": {
        "TextBox 2": "THIS MORNING",
        "TextBox 8": "Two standards, one measurement, thirty seconds",
        "TextBox 7": (
            "Both are HL7 standards. v2 has been carrying hospital traffic "
            "since 1989 and still carries most of it. FHIR arrived in 2014 and "
            "usually sits in front of v2 rather than replacing it.\n"
            "\n"
            "The difference that matters this afternoon is on the right. In v2 "
            "you find a value by counting fields. In FHIR you find it by its "
            "code — which is why Step 1 can name a column after "
            "Observation.code and survive somebody reordering the file.\n"
            "\n"
            "Every Bundle you are about to open looks like the lower box."
        ),
    },
    # ----------------------------------------------------------- 3 outline
    3: {
        "TextBox 5": "Outline",
        "TextBox 6": "FIVE STEPS, ONE MODEL",
        "TextBox 7": (
            "1.  Read FHIR Bundles into a table\n"
            "2.  Profile the data before modelling it\n"
            "3.  Train and compare two models\n"
            "4.  Cluster the patients without labels\n"
            "5.  Serve the model on your own laptop\n\n"
            "Every line of code is supplied. Your job is to run it, read the\n"
            "output, and decide whether the result deserves trust."
        ),
    },
    # ------------------------------------------- 25 anatomy, four stages
    25: {
        "TextBox 3": "FOUR STAGES",
        "TextBox 4": "Only stage three is machine learning. Projects fail at stages two and four.",
        "TextBox 18": "01. Source",
        "TextBox 19": "EHR and lab systems. Speaks FHIR, not pandas.",
        "TextBox 20": "02. Feature table",
        "TextBox 21": "One row per patient. Written by hand, every time.",
        "TextBox 22": "03. Model",
        "TextBox 23": "Fit, evaluate, select. Library work, once the table exists.",
        "TextBox 24": "04. Point of care",
        "TextBox 25": "An endpoint a clinician can act on, or nothing changes.",
    },
    # ------------------------------------------------ 23 why not an LLM
    23: {
        "TextBox 14": "Why not an LLM?",
        "TextBox 11": "TEN NUMBERS",
        "TextBox 13": "What this task needs",
        "TextBox 12": (
            "A probability you can move a threshold through, the same answer "
            "every single time it runs, and twelve coefficients a clinician can read."
        ),
        "TextBox 16": "Where LLMs belong",
        "TextBox 15": (
            "Upstream, at stage two: turning a free-text pathology report into these "
            "numbers, and mapping a local code onto LOINC. That job is still open."
        ),
    },
    # ---------------------------------------------------------- 2 divider
    2: {
        "TextBox 21": "STEP 1 — FROM BUNDLES TO A TABLE",
    },
    # -------------------------------------------------- 4 step 0, uv setup
    4: {
        "TextBox 2": "Step 0 · Before anything else",
        "TextBox 3": "INSTALL UV FIRST",
        "TextBox 4": (
            "1.  Install uv  —  github.com/astral-sh/uv\n"
            "      macOS / Linux    curl -LsSf https://astral.sh/uv/install.sh | sh\n"
            "      Windows          irm https://astral.sh/uv/install.ps1 | iex\n"
            "\n"
            "2.  Close and reopen your terminal, then check:   uv --version\n"
            "\n"
            "3.  git clone <repo>     cd fhir-ml-workshop\n"
            "\n"
            "4.  uv sync\n"
            "\n"
            "uv installs the right Python for you. You do not need Python first,\n"
            "and you do not need pip."
        ),
    },
    # -------------------------------------------- 24 one patient, twelve
    24: {
        "TextBox 16": "Step 1 · The data as given",
        "TextBox 14": "ONE PATIENT",
        "TextBox 15": "Patient",
        "TextBox 19": "1 — identity",
        "TextBox 17": "Observation",
        "TextBox 20": "{n_observation} — the features",
        "TextBox 18": "Condition",
        "TextBox 21": "1 — the biopsy result we predict",
        "TextBox 22": "Resources",
        "TextBox 23": "{resources_in_example}",
        "TextBox 24": "per patient",
        "TextBox 25": "{example_id}.json",
    },
    # ------------------------------------------------------ 6 step 1 flatten
    6: {
        "TextBox 4": "FLATTENING",
        "TextBox 5": "STEP 1     uv run python scripts/01_fhir_to_table.py",
        "TextBox 6": "Walk the Bundle",
        "TextBox 8": (
            "Take the Patient identifier, name a column after each "
            "Observation code, read the Condition as the label. Nothing in "
            "scikit-learn can read FHIR."
        ),
        "TextBox 7": "Then prove it matches",
        "TextBox 9": (
            "The script asserts its output is identical to patients.csv. One "
            "patient, P0010, returns a silent NaN because an Observation is "
            "missing from the Bundle."
        ),
    },
    # ------------------------------------------- 10 failure modes, three
    10: {
        "TextBox 26": "WHAT BREAKS ONCE THE FEED IS REAL",
        "TextBox 27": (
            "STEP 1     uv run python scripts/01_fhir_to_table.py --drop area\n"
            "\n"
            "The flattening works perfectly on the {n_bundles} Bundles we supplied.\n"
            "None of the following raises an error. Each one quietly changes\n"
            "the population your model is trained on."
        ),
        "TextBox 31": "Missing",
        "TextBox 28": "{inc_patient} carries no {inc_missing} Observation. The pivot returns NaN, silently.",
        "TextBox 32": "Uncoded",
        "TextBox 29": "No LOINC concept covers image morphometry, so a local code is used.",
        "TextBox 33": "Duplicated",
        "TextBox 30": "One patient, two departmental identifiers. Cross-validation then leaks.",
    },
    # ------------------------------------------------- 20 AI-readiness
    20: {
        "TextBox 4": "FIT TO MODEL?",
        "TextBox 5": (
            "STEP 2     uv run python scripts/02_explore_data.py\n"
            "\n"
            "Assessed and written down before a single model was fitted. Complete, "
            "labelled, leakage-free, and workably balanced at {pct_malignant}% malignant."
        ),
        "TextBox 10": (
            "BLOCKER — no demographics at all, so the subgroup fairness analysis "
            "a regulator would require cannot be performed."
        ),
        "TextBox 11": (
            "BLOCKER — a single time point with no follow-up. This is diagnosis, not "
            "prognosis. We proceed anyway, and you should be able to say why that is "
            "a compromise."
        ),
    },
    # --------------------------------------------------- 11 baseline stat
    11: {
        "TextBox 4": "{pct_benign}% ACCURACY, DETECTING NOTHING",
        "TextBox 5": (
            "{n_benign} of the {n} patients are benign. A classifier that answers "
            "“benign” every time scores {pct_benign}% while missing every tumour in the "
            "dataset. That is the number to beat, and the reason we report recall, "
            "precision and ROC-AUC instead."
        ),
    },
    # ------------------------------------------------- 14 what a model is
    # The morning was FHIR, not machine learning. These three pages are the
    # only introduction the room gets, so they come before any result.
    14: {
        "TextBox 13": "TWO MODELS",
        "TextBox 15": "Model A",
        "TextBox 18": "{logit_name}",
        "TextBox 14": (
            "Draws one straight boundary through the measurements. Every "
            "feature gets a weight you can print out and read to a doctor."
        ),
        "TextBox 16": "Model B",
        "TextBox 19": "{forest_name}",
        "TextBox 17": (
            "Grows 300 decision trees on random slices of the data and lets "
            "them vote. It bends around shapes a straight line cannot. "
            "Nobody reads 300 trees."
        ),
    },
    # -------------------------------------------------- 7 how we measure
    7: {
        "TextBox 2": "HOW WE MEASURE",
        "TextBox 8": "Before you believe any number",
        "TextBox 7": (
            "Hold out {n_test} patients. Train on the other {n_train}. Score "
            "only the held-out ones — a model marking its own homework always "
            "looks brilliant.\n"
            "\n"
            "Accuracy counts every mistake the same. Recall asks how many of "
            "the tumours we caught. Precision asks how many of our alarms "
            "were real."
        ),
    },
    # ------------------------------------------ pipeline: what gets saved
    "pipeline": {
        "TextBox 2": "ONE OBJECT",
        "TextBox 8": "Impute, scale, classify — fitted together, saved together",
        "TextBox 7": (
            "The median that fills a gap and the mean that centres a column "
            "are learned from the {n_train} training patients only, then "
            "reapplied unchanged to everybody else. Ship those two steps "
            "separately from the model and the app slowly drifts away from "
            "what was tested.\n"
            "\n"
            "Before the test set is opened at all, the training half is cut "
            "{cv_folds} ways and the model refitted {cv_folds} times. Recall "
            "lands between {cv_low:.3f} and {cv_high:.3f}. One split is not evidence."
        ),
    },
    # -------------------------------------------------------- 19 results
    19: {
        "TextBox 16": "THE TWO MODELS",
        "TextBox 17": "01. {logit_name}",
        "TextBox 18": (
            "Accuracy {logit_accuracy:.3f} · Recall {logit_recall:.3f} · ROC-AUC {logit_roc_auc:.3f}. "
            "{logit_missed} malignant masses missed in the {n_test}-patient test set. "
            "This is the model the script keeps."
        ),
        "TextBox 19": "02. {forest_name}",
        "TextBox 20": (
            "Accuracy {forest_accuracy:.3f} · Recall {forest_recall:.3f} · ROC-AUC {forest_roc_auc:.3f}. "
            "{forest_missed} malignant masses missed. More complexity, more cancers, "
            "no gain in accuracy."
        ),
        "TextBox 21": "Step 3 · Run it yourself",
        "TextBox 22": "uv run python\nscripts/03_train_model.py",
    },
    # ------------------------------------------------- 8 step 4, clustering
    8: {
        "TextBox 5": "GROUPS",
        "TextBox 7": "Step 4 · No labels used",
        "TextBox 6": (
            "uv run python\nscripts/04_cluster_patients.py\n"
            "\n"
            "K-Means never saw a diagnosis. Its two groups still line up with "
            "one: ARI {ari_2}.\n"
            "\n"
            "Ask for three groups and you get three, ARI {ari_3}. Ask for five "
            "and you get five, {ari_5}. It always answers."
        ),
    },
    # ------------------------------------------- 17 step 5, the app, guided
    17: {
        "TextBox 2": "STEP 5 · THE APP",
        "TextBox 11": "1 · Start it",
        "TextBox 21": (
            "uv run streamlit run app/streamlit_app.py\n"
            "Your browser opens at localhost:8501. If it does not, type that "
            "address in yourself. Ctrl+C in the terminal stops it."
        ),
        "TextBox 7": "2 · Load a real patient",
        "TextBox 23": (
            "In the sidebar click “Patient with a malignant tumour”. All ten "
            "sliders jump to that patient's actual measurements, and a risk "
            "band appears."
        ),
        "TextBox 15": "3 · Move a slider",
        "TextBox 20": (
            "Drag “Concave points”. Watch the probability and the RISK BAND "
            "move as you go. Nothing is retrained — you are re-scoring one "
            "patient."
        ),
        "TextBox 19": "4 · Move the threshold",
        "TextBox 22": (
            "Drag “Decision threshold” to {flip_low}, then 0.80. Read the three "
            "lines beneath it: how many tumours missed, how many healthy "
            "patients alarmed."
        ),
    },
    # ----------------------------------------------------- 5 error cost
    5: {
        "TextBox 5": "WHICH ERROR?",
        "TextBox 9": "False negative",
        "TextBox 13": (
            "A malignant mass reported benign and sent home. Detected in months, "
            "if ever. Frequently irreversible."
        ),
        "TextBox 10": "False positive",
        "TextBox 14": (
            "A healthy patient sent for an unnecessary biopsy. Detected in days. "
            "Frightening and costly, but recoverable."
        ),
        "TextBox 15": "Optimise recall",
        "TextBox 16": "Accept these",
    },
    # ------------------------------------- ablations: turn one knob, re-run
    # Every figure below was read out of the script's own diff table by
    # collect_results.py, so the slide says what the room's terminal says.
    "ablations": {
        "TextBox 3": "FOUR FLAGS",
        "TextBox 4": (
            "Step 3 · Change one setting, run it again. The script remembers "
            "your first run and prints the difference."
        ),
        "TextBox 18": "01. Move the line",
        "TextBox 19": (
            "--threshold 0.30\n"
            "Missed {threshold30_missed_was} → {threshold30_missed}. "
            "False alarms {threshold30_false_alarms_was} → "
            "{threshold30_false_alarms}. Accuracy does not move at all."
        ),
        "TextBox 20": "02. Drop features",
        "TextBox 21": (
            "--no-engineered\n"
            "Removes {engineered_1} and {engineered_2}. Recall, precision and "
            "accuracy all identical. Two features we were proud of bought "
            "nothing."
        ),
        "TextBox 22": "03. Punch holes",
        "TextBox 23": (
            "--missing 0.30\n"
            "Deletes {missing_column} for {missing_pct}% of patients. No error "
            "is raised. Recall {missing30_recall_was:.3f} → {missing30_recall:.3f}, "
            "{missing30_missed} missed."
        ),
        "TextBox 24": "04. Starve it",
        "TextBox 25": (
            "--test-size 0.8\n"
            "Trains on {starved_n_train} patients, not {n_train}. Missed "
            "{starved_missed_was} → {starved_missed} — and accuracy goes up."
        ),
    },
    # ------------------------------- starved: the headline number lying
    "starved": {
        "TextBox 4": "ACCURACY ROSE. THE MODEL GOT WORSE.",
        "TextBox 5": (
            "Training on {starved_n_train} patients instead of {n_train} moved "
            "accuracy from {starved_accuracy_was:.3f} to {starved_accuracy:.3f}, and "
            "missed tumours from {starved_missed_was} to {starved_missed}. "
            "The two runs are not even scored on the same patients. No single "
            "headline number settles anything — recall is the one with a "
            "person attached to it."
        ),
    },
    # ------------------------------- app_screen: what localhost:8501 shows
    # Both images are captured from the running app by slides/capture_app.py,
    # so a change to the app changes the slide instead of dating it.
    "app_screen": {
        "TextBox 2": "WHAT YOU SEE",
        "TextBox 8": "localhost:8501, after move 2",
        "TextBox 7": (
            "Ten sliders holding one real patient's measurements, a risk band "
            "on the right, and a sidebar reporting what your chosen threshold "
            "would do to all {n} patients at once.\n"
            "\n"
            "At 0.20 it misses {cost_20_missed} tumours and alarms "
            "{cost_20_false_alarms} healthy people. At 0.80 it misses "
            "{cost_80_missed} and alarms {cost_80_false_alarms}. Nothing is "
            "retrained between those two pictures — the weights are identical."
        ),
    },
    # ----------------------------------------------------- 21 deployment
    21: {
        "TextBox 9": "STEP 5 · NOW OVER HTTP",
        "TextBox 10": (
            "The same model, served the way the hospital served us data this "
            "morning: JSON in, JSON out. That symmetry is the reason FHIR made "
            "clinical AI integrable at all."
        ),
        "TextBox 13": "5 · Start the API",
        "TextBox 11": (
            "uv run uvicorn app.api:app --reload\n"
            "Open 127.0.0.1:8000/docs, expand POST /predict, click Try it out, "
            "then Execute."
        ),
        "TextBox 14": "6 · Ask {flip_patient} twice",
        "TextBox 12": (
            "/sample/{flip_patient}?threshold={flip_high} says benign.\n"
            "/sample/{flip_patient}?threshold={flip_low} says malignant.\n"
            "{flip_patient} has a real tumour. Same probability both times."
        ),
    },
    # ----------------------------- fhir_back: the result written back as FHIR
    "fhir_back": {
        "TextBox 2": "FULL CIRCLE",
        "TextBox 8": "Step 5c · press “Send to record” in the app",
        "TextBox 7": (
            "The app builds the request a hospital system would accept: one "
            "POST carrying a FHIR RiskAssessment. Nothing is sent — the "
            "hostname is fictional.\n"
            "\n"
            "Read three fields. It is a RiskAssessment, not a Condition — a "
            "score, not a diagnosis. Its performer is a Device, so the chart "
            "always shows that software wrote this line. Its basis lists the "
            "{n_features_raw} Observations the score came from, so somebody "
            "can audit it a year from now."
        ),
    },
    # ---------------------------------------------------- 22 limitations
    22: {
        "TextBox 16": "LIMITATIONS",
        "TextBox 18": "Never seen a patient from here",
        "TextBox 17": (
            "Fitted on one American hospital's cases from the 1990s. Transfer to "
            "this region is an assumption with no evidence."
        ),
        "TextBox 20": "Cannot be audited for bias",
        "TextBox 19": (
            "No age, sex, ethnicity or comorbidity recorded, so the subgroup "
            "analysis a regulator demands is impossible."
        ),
        "TextBox 22": "Predicts a label, not a disease",
        "TextBox 21": (
            "The target is what a pathologist wrote, errors included. The model "
            "repeats them with confidence."
        ),
    },
}

NOTES = {
    1: "Two hours, five steps, every line already written. Their job is to run it and judge it.",
    "recap": "Thirty seconds, not three minutes - this is a reminder, not a lecture, and "
             "they had two hours of it this morning. Point at the red carets: in v2 the "
             "meaning of 17.99 is 'the fifth field of OBX', so the contract is a position "
             "and a miscount gives you a wrong number with no error anywhere. In FHIR the "
             "meaning travels with the value as a code. Then say the honest part: v2 is "
             "not dead, it is what most hospitals run today, and FHIR is usually the front "
             "door bolted onto it. If nobody asks a question, move on.",
    3: "Point at step 1. It is what separates this from a generic scikit-learn tutorial.",
    25: "Ask which stage they expected to spend the afternoon on. Almost everyone says three. "
        "Stage two is the one that consumes the calendar in real projects.",
    23: "Asked every time: why not an LLM? Answer honestly. This input is already ten "
        "numbers - an LLM's advantage is unstructured text, and there is none here. We "
        "need a calibrated probability to put a threshold through, the same answer on "
        "every run for a regulator, and coefficients somebody can inspect. Twenty "
        "seconds of training, offline, no data leaving the building. Then give the LLM "
        "its due: the job it would actually be good at is the one we did by hand in "
        "Step 1 - reading a free-text report into structured fields, and mapping a "
        "local code onto LOINC. That is stage two, and it is still unsolved.",
    2: "Section break. From here on everything is the morning's material executed as code.",
    4: "uv sync is the only step needing the internet and the only one likely to fail in the "
       "room. Get everyone through it before moving on.",
    24: "Open data/fhir/P0001.json on the projector. Twelve resources describe one person, "
        "and none of that structure is what a model consumes.",
    6: "Run the script live. Point at P0010 in the output - no error, no warning, just NaN.",
    10: "Ask how they would have noticed the missing value if the script had not printed it. "
        "Most production pipelines do not print it.",
    20: "The honest slide. Without demographics the fairness audit cannot be run at all - that "
        "is a property of the dataset, not an oversight in the code.",
    11: "Say this number out loud before showing them any model result.",
    14: "Define the words before you use them. A model here is a function from ten numbers "
        "to one probability, fitted by showing it patients whose diagnosis we already know "
        "- that is what supervised means. Both pictures are the real fitted models, "
        "projected onto two dimensions. Logistic regression can only draw the straight "
        "line. The forest carves out pockets. More flexible is not automatically better, "
        "which is what the next three pages are about.",
    7: "Four cells and two fractions, and nothing else all afternoon. Walk the confusion "
       "matrix cell by cell before you say a single metric name - the false negative is "
       "bottom left, and it is the one with a patient attached to it. Then read the two "
       "fractions straight off the picture: recall uses the bottom row, precision uses the "
       "right-hand column.",
    "pipeline": "Two ideas, both about trust rather than accuracy. First: the median and the "
                "mean are learned quantities, so they belong inside the saved object. If the "
                "app recomputes them from whatever data it has to hand, the app is running a "
                "different model from the one that was tested, and nothing will tell you. "
                "common.py exists to make that impossible. Second: the five folds are fitted "
                "and scored before the test set is opened. Point at the spread - the same "
                "model on the same data scores differently depending on which patients it "
                "sees, so one number from one split was never evidence.",
    19: "Accuracy is tied at 0.930 and tells you nothing. Recall separates the models, and "
        "recall is the one attached to a human cost.",
    "ablations": "This is the longest hands-on block of the afternoon - give it ten minutes "
                 "and walk the room. Four commands, and the script prints the diff against "
                 "their first run, so nobody has to remember what the numbers were. Ask them "
                 "to predict the sign of the change before pressing enter, then read what "
                 "actually happened. Card two is the honest one: we engineered two features "
                 "for good clinical reasons and they bought nothing measurable. Report that. "
                 "Card three is the quiet one: 30% of a column deleted, no error, no warning, "
                 "two more women sent home.",
    "starved": "Stay on this one. Accuracy went UP while the model got materially worse, and "
               "if accuracy were the number on the dashboard nobody would have looked twice. "
               "Then be honest about the second problem: the two runs are scored on different "
               "test sets, so strictly the accuracies are not comparable at all - which is "
               "itself the lesson. Ask what number they would put on a dashboard for a "
               "screening tool, and make them defend it.",
    5: "Ask the room to commit to an answer, then ask whether it changes for a confirmatory "
       "test rather than a screening programme.",
    "app_screen": "Leave this one up while you walk the room. It is the reference screen — "
                  "anyone whose laptop does not look like this is stuck, and they will not "
                  "say so. Then use the two sidebars on the right: the model is byte for "
                  "byte the same in both, and one of them sends thirty-four women home. "
                  "Ask who in a hospital is allowed to choose that number. It is not the "
                  "person who wrote the code.",
    21: "They consumed JSON over HTTP this morning and they produce JSON over HTTP now. That "
        "sentence is the whole day.",
    8: "Short block. Structure exists in the measurements before anybody labels "
       "anything - useful when labels are expensive. Then the trap: --clusters 5 "
       "returns five groups whether or not five exist. Cut this block first if late.",
    17: "Walk them through it in order and do not move on until every screen shows a "
        "risk band. Number four is the one that matters: the curve in the middle is "
        "what they are dragging along, and the model is identical at every point on it.",
    "fhir_back": "This is the sentence the whole day was built to earn: this morning they "
                 "consumed a FHIR resource, and just now they produced one. Press the "
                 "button live and let the JSON fill the screen. Then slow down on three "
                 "words. RiskAssessment, not Condition - the model contributes a number, "
                 "it does not acquire the authority to diagnose, and FHIR encodes that in "
                 "the data model rather than in a policy document. performer is a Device, "
                 "so nobody reading the chart in five years can mistake a machine's line "
                 "for a clinician's. basis lists the ten Observations, which is the only "
                 "reason the score can ever be audited. If someone asks what is still "
                 "missing before this is real: authentication, a Provenance resource, a "
                 "validated model, and a regulator.",
    22: "Do not rush this. Stating the limits of your own model is the difference between an "
        "engineer and someone who should not be given patient data.",
}


def set_text(shape, text: str) -> None:
    """Replace a text box's content, keeping the first run's formatting."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    if not p0.runs:
        return

    lines = text.split("\n")
    p0.runs[0].text = lines[0]
    for r in p0.runs[1:]:
        r._r.getparent().remove(r._r)
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)

    for line in lines[1:]:
        new_p = copy.deepcopy(p0._p)
        p0._p.getparent().append(new_p)
        para = _Paragraph(new_p, tf)
        para.runs[0].text = line
        for r in para.runs[1:]:
            r._r.getparent().remove(r._r)


def main() -> None:
    prs = Presentation(SRC)
    facts = load_results()

    named = [o for o in ORDER if not isinstance(o, int)]
    if named:
        print("  ! pages written after the Canva export cannot be rebuilt from it:")
        print("    " + ", ".join(named))
        print("    re-add them with slides/clone_page.py, then run apply_results.py")

    for orig, mapping in TEXT.items():
        if not isinstance(orig, int):
            continue
        mapping = {k: v.format(**facts) for k, v in mapping.items()}
        slide = prs.slides[orig - 1]
        by_name = {sh.name: sh for sh in slide.shapes}
        for name, new in mapping.items():
            sh = by_name.get(name)
            if sh is None:
                print(f"  ! slide {orig}: no shape named {name}")
                continue
            set_text(sh, new)
        if orig in NOTES:
            slide.notes_slide.notes_text_frame.text = NOTES[orig]

    sldIdLst = prs.slides._sldIdLst
    ids = list(sldIdLst)
    keep_idx = {n - 1 for n in ORDER if isinstance(n, int)}

    for i, sid in enumerate(ids):
        if i not in keep_idx:
            rId = sid.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            )
            prs.part.drop_rel(rId)
            sldIdLst.remove(sid)

    remaining = {i + 1: sid for i, sid in enumerate(ids) if i in keep_idx}
    for sid in list(sldIdLst):
        sldIdLst.remove(sid)
    for orig in ORDER:
        if isinstance(orig, int):
            sldIdLst.append(remaining[orig])

    DST.parent.mkdir(parents=True, exist_ok=True)
    prs.save(DST)
    print(f"wrote {DST}  ({len(Presentation(DST).slides._sldIdLst)} slides)")


if __name__ == "__main__":
    main()
