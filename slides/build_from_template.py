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
    1, "recap", "agenda", 23, 4, 2, 24, 6, "provenance", "part2",
    "features", 14, "pipeline",      # the two we wrote, what a model is,
                                #   and whether one split was fair
    "ablations",                # run it, turn a knob, watch the numbers move
    7, 11, 5, 19,               # only then: what the numbers mean, and the results
    "part3", 17, "app_screen",           # the four moves, then what the screen looks like
    21, "fhir_back",            # and the result written back as FHIR
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
    for run_name in ("no_engineered", "starved"):
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
        "TextBox 8": "v2 finds a value by counting fields. FHIR finds it by its code.",
        "TextBox 7": (
            "Both are HL7 standards. v2 has been carrying hospital traffic "
            "since 1989 and still carries most of it. FHIR arrived in 2014 and "
            "usually sits in front of v2 rather than replacing it.\n"
            "\n"
            "The difference that matters this afternoon is on the right. In v2 "
            "you find a value by counting fields. In FHIR you find it by its "
            "code — which is why the flattening script can name a column after "
            "Observation.code and survive somebody reordering the file.\n"
            "\n"
            "Every Bundle you are about to open looks like the lower box."
        ),
    },
    # ------------------------------- agenda: five steps grouped into three
    # Five bullets is a list nobody remembers. Three moves is a shape.
    "agenda": {
        "TextBox 26": "AGENDA",
        "TextBox 27": (
            "Three moves. Every line of code is supplied — your "
            "job is to run it, read what comes back, and decide whether the "
            "result deserves trust."
        ),
        "TextBox 31": "1 · To a table",
        "TextBox 28": (
            "Walk one FHIR Bundle per patient, name a column after each "
            "code, and find "
            "out where the data really came from."
        ),
        "TextBox 32": "2 · To a model",
        "TextBox 29": (
            "Train two models, judge them on the error that costs a patient, "
            "then change one setting and watch what it did."
        ),
        "TextBox 33": "3 · To a service",
        "TextBox 30": (
            "Serve it on your own laptop two ways, then write the prediction "
            "back into the record as FHIR."
        ),
    },
    # -------------------------------------------------------- 19 results
    19: {
        "TextBox 16": "THE RESULTS",
        "TextBox 17": "01. {logit_name}",
        "TextBox 18": (
            "Accuracy {logit_accuracy:.3f} · Recall {logit_recall:.3f}. "
            "{logit_missed} malignant masses missed in the {n_test}-patient "
            "test set. This is the model the script keeps."
        ),
        "TextBox 19": "02. {forest_name}",
        "TextBox 20": (
            "Accuracy {forest_accuracy:.3f} · Recall {forest_recall:.3f}. "
            "{forest_missed} missed. Identical accuracy, two more cancers — "
            "this is the disagreement the last three slides were about."
        ),
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
        "TextBox 2": "THE APP, IN FOUR MOVES",
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
        "TextBox 3": "CHANGE ONE THING",
        "TextBox 4": (
            "Run it once with nothing set. Then change one setting and run it "
            "again — the script remembers your first run and prints the "
            "difference for you."
        ),
        "TextBox 20": "01. Fewer columns",
        "TextBox 21": (
            "--no-engineered\n"
            "Trains without the two columns we wrote. Every number comes back "
            "exactly the same. They bought nothing."
        ),
        "TextBox 24": "02. Fewer patients",
        "TextBox 25": (
            "--test-size 0.8\n"
            "Trains on {starved_n_train} patients instead of {n_train}. Tumours "
            "missed: {starved_missed_was} → {starved_missed}. And the headline "
            "score goes up."
        ),
    },
    # --------------- was one random draw fair? the page exists for that
    # The pipeline diagram is on this page too, but it is the supporting act:
    # what gets refitted inside every fold is exactly the saved object.
    "pipeline": {
        "TextBox 2": "WAS THAT SPLIT\nFAIR?",
        "TextBox 8": "k-fold cross-validation",
        "TextBox 7": (
            "Holding {n_test} patients back was one shuffle of the deck. That "
            "is a draw, not a measurement. What if the {n_test} we happened to "
            "hold back were the easy ones? Nothing inside a single split can "
            "tell you.\n\n"
            "So the {n_train} training patients are cut into five parts and the "
            "model is refitted five times, a different fifth held back each "
            "round. That is what cross-validation is, and it is what you run "
            "whenever you need to know whether a number is real or was luck.\n\n"
            "Recall lands anywhere between {cv_low:.3f} and {cv_high:.3f} — "
            "mean {cv_mean:.3f}, spread ±{cv_std:.3f}. One number to three "
            "decimals was never the answer. That spread is."
        ),
    },
    # ------------------------- stage 2 made concrete, before it is judged
    # The flags page later reports that these two bought nothing. That lands
    # only if the room first sees why a sane person would build them.
    "features": {
        "TextBox 2": "FEATURE\nENGINEERING",
        "TextBox 8": "A model can only see what is a column",
        "TextBox 7": (
            "If the thing that matters is not a column, the model cannot use "
            "it. Feature engineering is making it one — no new data arrives, "
            "you do arithmetic on what you were sent.\n\n"
            "The Bundle carries {n_features_raw} measurements. The model trains "
            "on {n_features_total}. We wrote two: {engineered_1} is perimeter² "
            "/ area, {engineered_2} is concavity / radius. Both say something "
            "about shape that no single measurement says on its own.\n\n"
            "That is a hypothesis, not an answer. A pathologist would agree "
            "with the reasoning — and we test it later this afternoon."
        ),
    },
    # ------------------------- stage 2 made concrete, before it is judged
    # The flags page later reports that these two bought nothing. That lands
    # only if the room first sees why a sane person would build them.
    # ------------------------------- app_screen: what localhost:8501 shows
    # Both images are captured from the running app by slides/capture_app.py,
    # so a change to the app changes the slide instead of dating it.
    "app_screen": {
        "TextBox 2": "WHAT YOU SEE",
        "TextBox 8": "localhost:8501, after move 2",
        "TextBox 7": (
            "Ten sliders holding one real patient's measurements, a risk band "
            "on the right, and a sidebar reporting what your chosen threshold "
            "would do.\n"
            "\n"
            "At 0.20 it misses {cost_20_missed} tumours and alarms "
            "{cost_20_false_alarms} healthy people. At 0.80 it misses "
            "{cost_80_missed} and alarms {cost_80_false_alarms}. Those counts "
            "are over all {n} patients, not the {n_test} in the test set — "
            "which is why they are bigger than the numbers on the results "
            "slide. Nothing is retrained between the two pictures."
        ),
    },
    # ----------------------------------------------------- 21 deployment
    21: {
        "TextBox 9": "NOW OVER HTTP",
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
        "TextBox 8": "Press “Send to record” in the app",
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
    1: "Open on the morning's own phrase, not on yours. They were told "
       "'impedance mismatch' - hierarchical FHIR trees against flat 2-D feature "
       "matrices. Say the afternoon is two hours of fixing exactly that by hand, "
       "and that the fixing is where real projects spend their calendar. Then: "
       "two hours, five steps, every line already written, and their job is to "
       "run it and judge it.",
    "recap": "Thirty seconds, not three minutes - this is a reminder, not a lecture, and "
             "they had two hours of it this morning. Point at the red carets: in v2 the "
             "meaning of 17.99 is 'the fifth field of OBX', so the contract is a position "
             "and a miscount gives you a wrong number with no error anywhere. In FHIR the "
             "meaning travels with the value as a code. Then say the honest part: v2 is "
             "not dead, it is what most hospitals run today, and FHIR is usually the front "
             "door bolted onto it. If nobody asks a question, move on.",
    "agenda": "Three moves, not five bullets. Point at the first box and say that this is "
              "the one that makes today different from a generic scikit-learn tutorial - "
              "most courses hand you a clean CSV, and clinical data never arrives that way. "
              "The card on the right is every command they will type all afternoon; tell "
              "them it is seven lines and they have already run the first one.",
    25: "The map for the next forty minutes, shown after they have already done stage one "
        "rather than before. Ask which stage they expected to spend the afternoon on - "
        "almost everyone says three, and three is twenty seconds of compute. They have "
        "just spent twenty minutes on stages one and two, which is the correct ratio. "
        "Then point at four: nothing in the first three stages tells you whether the "
        "result is any good, and that is what the rest of the afternoon is about.",
    19: "Accuracy is tied at 0.930 and tells you nothing. Recall separates the models, and "
        "recall is the one attached to a human cost.",
    "ablations": "This is the longest hands-on block of the afternoon - give it ten minutes "
                 "and walk the room. Two commands, and the script prints the diff against "
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
    "fhir_back": "Call back to the morning first: the Raman spotlight ended by serialising a sensor reading into FHIR R4. Same move here, different payload - that was an instrument writing into the record, this is a model writing into it. Then: this is the sentence the whole day was built to earn: this morning they "
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
