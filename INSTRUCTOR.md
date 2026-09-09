# Instructor notes

Not part of the student handout. Delete this file before sharing if you prefer.

> **Teaching from the front?** `TEACHING_SCRIPT.md` is the minute-by-minute
> version of this file, with the sentences written out. This file is the
> reference: timings, expected numbers, failure modes, scope gaps.

## The spine of the afternoon

The morning is a lecture on health data ecosystems, HL7 v2, FHIR and
AI-readiness. The afternoon has to *land* that, not run beside it. Step 1 is the
join: students start from FHIR Bundles and end at the table scikit-learn wants.

```
morning lecture          afternoon code
-----------------        --------------------------------
FHIR Resources     ->    Step 1  data/fhir/*.json
Bundle / reference ->    Step 1  walk entry[], join on subject
coded vocabularies ->    Step 1  Observation.code names the column
AI-readiness       ->    Step 2  missingness, class balance, leakage
                         Step 3  pipeline, metrics
                         Step 5  the model becomes callable over HTTP
```

If you only make one point all afternoon, make it this: **the FHIR-to-table step
is the job.** Everything downstream is a library call.

## Before the session

1. Run the whole flow once on the room's network:
   ```bash
   uv sync
   uv run python scripts/01_fhir_to_table.py
   uv run python scripts/02_explore_data.py
   uv run python scripts/03_train_model.py
   uv run python scripts/04_cluster_patients.py
   uv run streamlit run app/streamlit_app.py
   uv run uvicorn app.api:app --reload
   ```
2. **Send students the repo link and https://github.com/astral-sh/uv the night before**, with
   instructions to install uv and run `uv sync` at their accommodation. Ask for
   a screenshot of `uv run python -c "import sklearn; print(sklearn.__version__)"`
   as proof. This is the single highest-value thing you can do.
3. `uv sync` pulls about **580 MB per laptop** (66 packages). Thirty laptops is
   roughly 17 GB through the room's wifi — it will not finish in fifteen
   minutes. Bring two or three USB sticks carrying a pre-populated
   `~/.cache/uv` (`uv cache dir` prints the path) so stragglers can run
   `uv sync --offline`.
4. Have the **Download ZIP** link ready — Windows laptops frequently have no
   git: https://github.com/AIT-brainlab/fhir-ml-workshop/archive/refs/heads/main.zip
5. `data/patients.csv`, `data/fhir/` and `uv.lock` are committed, so nothing
   else downloads during class.
6. `models/model.joblib` is intentionally **not** committed — students must run
   Step 3 to produce it. If your room's laptops are slow, commit it as a
   fallback so Step 5 still works.

## Running to time (120 minutes)

| Minutes | What | Slides |
|---|---|---|
| 0–12 | Recap of v2 vs FHIR, what learning means, why not an LLM | 1–6 |
| 12–22 | `uv sync`, fix the two or three laptops that fail | 7 |
| 22–40 | Step 1 — FHIR to table; open `data/fhir/P0001.json` on the projector | 8–10 |
| 40–52 | Break the feed on purpose | 11 |
| 52–60 | Step 2 — read the output, majority-class baseline | 12, 13 |
| 60–70 | What a model is, how it is judged, what gets saved | 14–16 |
| 70–80 | Step 3 — the two models, and which error costs more | 17, 18 |
| 80–94 | Four flags — the longest hands-on block | 19, 20 |
| 94–100 | Step 4 — clustering, short | 21 |
| 100–114 | Step 5 — the app, the API, then the result back as FHIR | 22–25 |
| 114–120 | Limitations + the "why is this not safe" question | 26 |

Slide 2 recaps v2 versus FHIR in thirty seconds — after lunch, half the room
has lost it. Slide 5 defines what learning is at all; slides 14–16 and 19–20 carry the rest
of the machine-learning explanation. The morning
lecture is FHIR and AI-readiness, so this afternoon is the first time the room
hears what a model, a hold-out set or a recall figure actually is. Skipping
them means opening on a results table nobody can read.

If you are behind schedule, **cut Step 4 first** — slide 21 can be shown and
talked over in thirty seconds. Then trim slide 19 from four commands to two and
run them from the front. Never cut Step 1 (it is the link to the morning),
never cut slides 5, 14–15, never cut slides 22–23 (the guided app walkthrough and
the reference screen), and never cut the last 10 minutes.

## Everything is a flag now

Students never edit a file to run an experiment. Each script takes arguments and
answers `--help`. The ones worth demonstrating from the front:

| Command | What the room actually sees |
|---|---|
| `01_fhir_to_table.py --drop area` | a column vanishes, nothing errors |
| `01_fhir_to_table.py --rename radius:tumor_rad` | a renamed code silently breaks the join |
| `03_train_model.py --threshold 0.3` | missed 3 → 1, false alarms 5 → 7, accuracy unmoved |
| `03_train_model.py --no-engineered` | recall, precision and accuracy **identical** |
| `03_train_model.py --missing 0.3` | no error at all, and 2 more tumours missed |
| `03_train_model.py --test-size 0.8` | missed 3 → 21 while **accuracy rises** to 0.941 |
| `04_cluster_patients.py --clusters 5` | five groups appear because you asked |

Two of those are worth knowing in advance because they defeat the obvious
expectation, which is exactly why they teach well:

- **`--no-engineered` changes nothing.** The two hand-built shape ratios
  (`compactness_ratio`, `concavity_per_radius`) were added for sound clinical
  reasons and buy no measurable accuracy, recall or precision — only ROC-AUC
  moves, by 0.003. Say so. A student who learns to report that is worth more
  than one who learns to tune.
- **`--test-size 0.8` makes accuracy go up.** Training on 113 patients instead
  of 455 raises accuracy from 0.930 to 0.941 and takes missed tumours from 3 to
  21. It is the cleanest demonstration in the whole afternoon that a single
  headline metric decides nothing. Mention too that the two runs are scored on
  different test sets (456 patients versus 114), so strictly the accuracies are
  not comparable at all — which is the deeper version of the same lesson.

`03_train_model.py` records the first default run in `reports/baseline.json` and
prints a signed diff against it on every later run. **Run it once with no flags
before the session**, or the first student to change a flag gets no comparison.

### The single best two minutes of the afternoon

Open the API and hit these in order on the projector:

```
/sample/P0216?threshold=0.5   ->  "benign"
/sample/P0216?threshold=0.2   ->  "malignant"
```

P0216 is a real malignant tumour. Same patient, same model, same probability
(0.216). Ask the room who is responsible for the difference between those two
answers. Nobody in the room will say "the model".

Then open the Streamlit sidebar slider, which prints the cost across all 569
patients as they move it: 0.20 misses 7 tumours and alarms 39 healthy patients;
0.50 misses 20 and alarms 10; 0.80 misses 34 and alarms 1.

## The points worth making out loud

- **One patient is not one record.** Open `data/fhir/P0001.json` on screen. Ask
  the room how many resources describe this one person. Twelve.
- **The column name comes from the code, not the position.** That is what coded
  vocabularies buy you, and it is why a pipe-delimited HL7 v2 message is harder
  to work with than a FHIR Bundle.
- **P0010 is missing a measurement on purpose.** It produces a silent `NaN`. Ask
  the room how they would have noticed if the script had not printed it. Most
  real pipelines do not print it.
- **No LOINC codes here.** These are research morphometry values from an image,
  so they sit under a local CodeSystem. Real integration projects lose weeks to
  exactly this. We did not invent LOINC codes to make the demo look tidier —
  point that out.
- **No demographics at all.** `Patient` has an identifier and nothing else,
  because the source dataset has nothing else. So you cannot audit this model
  for bias across age or ethnicity. That is a blocker, not a footnote.
- **Majority-class baseline.** 62.7% accuracy for a model that detects nothing.
  Say this before you show any metric.
- **False negative vs false positive.** Ask which error they would rather make,
  and why the answer changes between screening and confirmation.
- **The pipeline is the deployable unit.** Scaling learned on training data must
  be reapplied identically at prediction time. `common.add_features` exists so
  training and serving cannot drift apart — that drift is a real and common
  patient-safety bug.
- **Clustering finds structure, not meaning.** K-Means recovers the diagnosis
  boundary (ARI ≈ 0.65) without ever seeing a label, but cannot say which
  cluster is dangerous.
- **Close the loop at Step 5c.** They read a FHIR resource this morning and
  produce one this afternoon: the app's "Send to record" button builds a real
  `RiskAssessment`. Make the distinction out loud — a RiskAssessment is a
  score performed by a `Device`; a `Condition` is a diagnosis asserted by a
  `Practitioner`, and the app never writes one. That separation is in the data
  model, not in a policy document.

## Expected numbers

Logistic Regression wins on recall and is the model that gets saved.

| Metric (test set, n=114) | Logistic Regression | Random Forest |
|---|---|---|
| accuracy | 0.930 | 0.930 |
| precision | 0.886 | 0.925 |
| recall | **0.929** | 0.881 |
| ROC-AUC | 0.987 | 0.984 |

Random Forest misses 5 malignant tumours, Logistic Regression misses 3 — a
concrete, teachable reason to pick the simpler model.

Step 1: 20 bundles, 19 complete rows, `texture` missing for P0010, comparison
against `patients.csv` returns `True`.

Clustering: silhouette 0.395, ARI vs. true diagnosis 0.646 (k=2);
ARI 0.483 at k=3 and 0.324 at k=5.

Cross-validation, 5 folds on the 455 training patients, recall: mean 0.900,
spread ±0.040, lowest fold 0.853, highest 0.941. Slide 16 uses this to make
the point that one split is not evidence.

Numbers are fixed by `random_state=42`, so they will be identical on every
laptop. If a student sees different figures, they edited something.

Every figure quoted in the deck is generated, not typed:
`slides/collect_results.py` runs the real pipeline with the pinned seed and
writes `slides/results.json`; `build_from_template.py`, `apply_results.py` and
`make_figures.py` all read from it. If you change the code or the data, run:

```bash
uv run python slides/collect_results.py
uv run python slides/apply_results.py
```

Slide 21 is a photograph of the running app, also generated rather than pasted:

```bash
uv run --with playwright playwright install chromium   # once
uv run --with playwright python slides/capture_app.py
```

It starts the app, makes the four moves slide 20 asks for, and writes
`slides/figures/app_full.png` and `app_threshold.png`. Re-run it if you change
the app's layout, or the slide will show a screen that no longer exists.

## Known scope gaps

Worth knowing in case anyone compares the code against the programme blurb.

- The blurb says **"patient outcome prediction"**. This is diagnosis, not
  prognosis — the dataset is a single time point with no follow-up. Say so
  during Step 2 and use it to explain the difference; it takes two minutes and
  is a better lesson than pretending otherwise.
- The blurb says **"public health datasets"**. Everything here is clinical.
  There is no population-level or epidemiological component.

## Common failures in the room

| Symptom | Cause |
|---|---|
| `uv: command not found` | uv not installed yet, or terminal not restarted |
| `No \`pyproject.toml\` found` | They ran `uv sync` outside the cloned folder |
| `ModuleNotFoundError: common` | Ran `python scripts/...` instead of `uv run python scripts/...`, or from the wrong directory |
| Streamlit shows the model-missing error | Step 3 not run yet |
| Port already in use | Another student's server, or a previous run not stopped |
| Corporate laptop blocks the installer | Fall back to `pip install uv` |

## Regenerating the data

Only needed if you change which columns are exported or which patients get
FHIR Bundles:

```bash
uv run python scripts/00_build_dataset.py
```

This rewrites both `data/patients.csv` and `data/fhir/`.
