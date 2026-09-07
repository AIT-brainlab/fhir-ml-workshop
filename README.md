# Machine Learning for Health Data — Hands-on Workshop

A two-hour session. You start from FHIR Bundles, turn them into a table, train
a model on that table, serve it on your own laptop, and write the result back
out as FHIR.

You will run seven commands. All the code is already written — your job is to run
it, change a setting, run it again, and decide whether you would trust the result.

Nothing here requires editing a file. Every setting worth playing with is a
command-line flag, and every script answers `--help`.

```
FHIR Bundles  →  flat table  →  trained model  →  running service
   Step 1          Step 2          Step 3-4          Step 5
```

---

## Step 0a — Install uv  (do this first, ideally the night before)

Everything in this workshop runs through **uv**, the Python package manager.

> **https://github.com/astral-sh/uv**

Install it *before* you touch this repository. `uv sync` will not work until uv
exists, and it will not work outside the cloned folder.

**macOS / Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal, then check:

```bash
uv --version
```

You do **not** need Python installed first, and you do **not** need `pip`. The
installer is a standalone binary, and uv downloads the correct Python (3.12)
for you in the next step.

*No git on your machine?* Use the green **Code → Download ZIP** button on the
repository page instead of `git clone`, and unzip it.

---

## Step 0b — Get the code and build the environment

```bash
git clone <REPO-URL> health-ai-workshop
cd health-ai-workshop
uv sync
```

`uv sync` must run **from inside the folder** — it reads `pyproject.toml` and
`uv.lock` from the current directory. Running it anywhere else is the most
common first error.

It downloads about 580 MB the first time — 66 packages, pinned to exact
versions by `uv.lock` so every machine in the room ends up identical. That is
the whole reason we use it: "it works on my laptop" is not a result you can
publish. On conference wifi with thirty laptops it is also slow, which is why
this page says *the night before*.

Check it worked:

```bash
uv run python -c "import sklearn; print(sklearn.__version__)"
```

> You never need to activate a virtual environment. Just put `uv run` in front
> of any command and uv handles it.

---

## Step 1 — From FHIR to a table

```bash
uv run python scripts/01_fhir_to_table.py
```

This is the bridge from this morning. `data/fhir/` holds 20 real FHIR R4
Bundles — the format a hospital system would actually hand you. Each Bundle
contains one `Patient`, ten `Observation` resources, and one `Condition`
carrying the biopsy result.

The script walks each Bundle, pulls the coded values out, and produces one row
per patient. Nothing in scikit-learn can read FHIR. Someone has to write this
step, and in most health AI projects it is where the majority of the work goes.

**Look for:** one patient comes back with a missing measurement. No error, no
warning — just a silent `NaN`, because that `Observation` was not in the Bundle.
That is the normal condition of real health data.

**Now break the feed yourself** — the files on disk are never modified:

```bash
uv run python scripts/01_fhir_to_table.py --drop area
uv run python scripts/01_fhir_to_table.py --rename radius:tumor_rad
```

The script then proves the rows it produced are identical to `data/patients.csv`,
which is the same flattening run over all 569 patients.

---

## Step 2 — Explore the dataset

```bash
uv run python scripts/02_explore_data.py
```

Profiles the 569 patients: what the columns mean, whether anything is missing,
how imbalanced the classes are, and which measurements separate malignant from
benign tumours. Saves two figures into `reports/`.

**Look for:** the majority-class baseline it prints. If 63% of patients are
benign, a model that predicts "benign" every time is already 63% accurate — and
completely useless. This is why the next step does not report accuracy alone.

---

## Step 3 — Train model

```bash
uv run python scripts/03_train_model.py
```

Splits the data, engineers two shape features, builds a scikit-learn `Pipeline`
(impute → scale → classify), trains **Logistic Regression** and **Random
Forest**, cross-validates both, and evaluates them on data neither model has
seen. Saves the better model to `models/model.joblib` and a ROC curve to
`reports/`.

**Look for:** the confusion matrix, and section 5 — the same fitted model read
off at seven different thresholds. Nothing is retrained between those rows.

**Then change one thing and run it again.** The first default run is recorded as
a baseline, and every later run prints what your change did to it:

```bash
uv run python scripts/03_train_model.py --threshold 0.30   # catch more, alarm more
uv run python scripts/03_train_model.py --missing 0.30     # delete 30% of a column
uv run python scripts/03_train_model.py --test-size 0.8    # starve it of training data
uv run python scripts/03_train_model.py --seed 7           # a different random split
uv run python scripts/03_train_model.py --no-engineered    # drop the two shape features
```

---

## Step 4 — Find patient subgroups (unsupervised)

```bash
uv run python scripts/04_cluster_patients.py
```

Runs K-Means and PCA on the same patients with the diagnosis **hidden**. The
algorithm still recovers groups that line up closely with the real diagnosis.

**Look for:** the crosstab of cluster vs. actual diagnosis. Clustering can find
structure without labels — but it cannot tell you which group is the dangerous
one. Only labelled data does that.

```bash
uv run python scripts/04_cluster_patients.py --clusters 3
uv run python scripts/04_cluster_patients.py --clusters 5
```

Three groups will always appear if you ask for three. That is the trap.

---

## Step 5 — Deploy for local use

Two ways to serve the same model. Try both.

### 5a. Browser app (Streamlit)

```bash
uv run streamlit run app/streamlit_app.py
```

Opens <http://localhost:8501>. Load a real patient from the sidebar, move the
measurement sliders, and watch the risk band change.

Then move the **Decision threshold** slider. It reports live what that threshold
would do across all 569 patients — how many tumours it misses, how many healthy
people it sends for a biopsy. The model is never retrained. Only the line moves.

Press `Ctrl+C` in the terminal to stop.

### 5b. REST API (FastAPI)

```bash
uv run uvicorn app.api:app --reload
```

Open <http://127.0.0.1:8000/docs>, expand **POST /predict**, click *Try it out*,
then *Execute*. You just called your own model over HTTP — JSON in, JSON out,
the same interaction style as the FHIR server from this morning. This is how a
hospital system would consume your model.

Also try these two, one after the other:

```
http://127.0.0.1:8000/sample/P0216?threshold=0.5
http://127.0.0.1:8000/sample/P0216?threshold=0.2
```

P0216 has a real, biopsy-confirmed malignant tumour. At 0.5 the model calls it
benign. At 0.2 it catches it. The probability is identical in both responses —
only the threshold moved.

### 5c. Back into the record, as FHIR

Everything above returns JSON we invented. A hospital cannot file that. Scroll
to the bottom of the Streamlit app and press **Send to record**:

```
POST https://hospital.example.org/fhir/RiskAssessment
Content-Type: application/fhir+json
```

Nothing is sent — the hostname is fictional and the request is only built and
shown. The same resource is available from the API:

```
http://127.0.0.1:8000/sample/P0216/fhir?threshold=0.5
http://127.0.0.1:8000/sample/P0216/fhir?threshold=0.2
```

**Look for three fields.**

| field | why it matters |
|---|---|
| `resourceType` | `RiskAssessment`, not `Condition` — a score, not a diagnosis |
| `performer` | points at a **Device**, so the chart shows software wrote this |
| `basis` | the ten `Observation` ids the score came from, so it can be audited |

This morning you read a FHIR resource. Now you have produced one. Same
standard, opposite direction — that round trip is the point of the whole day.

The diagnosis of record is still a `Condition` written by a clinician. This app
never creates one, and it must not.

---

## Before you leave

Three things to be able to say out loud:

1. Show one live prediction, from the app or the API.
2. Your confusion matrix from Step 3, and which metric you would optimise.
3. **One reason this model is not safe to use on real patients.**

The third is the one that matters — and "we need more data" does not count.
Name something specific: a row in the AI-readiness table, a number you saw, a
column that is missing.

---

## Folder structure

```
health-ai-workshop/
├── README.md              <- you are here
├── EXERCISES.md           <- the knobs, and what to notice when you turn them
├── TEACHING_SCRIPT.md     <- instructor only: minute-by-minute running order
├── pyproject.toml         <- dependency list
├── uv.lock                <- exact versions, so everyone gets the same env
├── common.py              <- shared feature engineering + prediction logic
├── fhir_out.py            <- the return trip: prediction -> FHIR RiskAssessment
├── data/
│   ├── fhir/              <- 20 FHIR R4 Bundles (Step 1 input)
│   ├── patients.csv       <- the flat table, all 569 patients
│   └── DATA_CARD.md       <- where it came from, what each column means
├── scripts/
│   ├── 00_build_dataset.py     <- instructor only, already run for you
│   ├── 01_fhir_to_table.py     <- Step 1
│   ├── 02_explore_data.py      <- Step 2
│   ├── 03_train_model.py       <- Step 3
│   └── 04_cluster_patients.py  <- Step 4
├── app/
│   ├── streamlit_app.py   <- Step 5a and 5c
│   └── api.py             <- Step 5b, plus /fhir variants
├── slides/                <- the deck used in the session
├── models/                <- model.joblib appears here after Step 3
└── reports/               <- figures appear here after Steps 2 and 4
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv: command not found` | Close and reopen the terminal after installing uv |
| `models/model.joblib not found` | Run Step 3 first |
| `ModuleNotFoundError` | You forgot `uv run` in front of the command |
| Port 8501 or 8000 already in use | Add `--server.port 8502` (Streamlit) or `--port 8001` (uvicorn) |
| Nothing opens in the browser | Type the URL manually: `localhost:8501` |
| You want to start over | `rm -rf .venv && uv sync` |

---

## Data and safety notice

`data/patients.csv` is the **Breast Cancer Wisconsin (Diagnostic)** dataset,
distributed with scikit-learn and derived from digitised fine-needle-aspirate
images collected in the 1990s. It contains no identifiable patient information.
The Bundles in `data/fhir/` were generated from that same dataset to show its
shape as FHIR — they are a faithful re-encoding, not a separate source. See
`data/DATA_CARD.md` for details.

Everything in this repository is teaching material. It is not a medical device,
has not been clinically validated, and must never be used to make decisions
about a real patient.
