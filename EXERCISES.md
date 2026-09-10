# Turn the knobs

You do not have to write any code. Every experiment below is a flag on a
command you have already run. Run it, read what changed, and try to explain it
to the person next to you before moving on.

Every script also has `--help`:

```bash
uv run python scripts/03_train_model.py --help
```

---

## A. The decision threshold

The model outputs a probability. Somebody has to decide how high that
probability must be before a patient is sent for a biopsy. That decision is not
in the model.

### A1. One patient, two answers

Start the API:

```bash
uv run uvicorn app.api:app --reload
```

Then open these two URLs:

```
http://127.0.0.1:8000/sample/P0216?threshold=0.5
http://127.0.0.1:8000/sample/P0216?threshold=0.2
```

P0216 has a **real, biopsy-confirmed malignant tumour**.

- What does the model call it at 0.5?
- What does it call it at 0.2?
- The probability is identical in both responses. What actually changed?

### A2. Watch the cost of the choice

```bash
uv run streamlit run app/streamlit_app.py
```

Move the **Decision threshold** slider in the sidebar. It reports, live, what
that threshold would do across all 569 patients.

Fill this in:

| threshold | tumours missed | healthy patients alarmed |
|---|---|---|
| 0.20 | | |
| 0.50 | | |
| 0.80 | | |

- At which threshold would you deploy a **screening** programme?
- Would your answer change for a **confirmatory** test after a suspicious scan?
- Who in a hospital should own this number: the data scientist, the radiologist,
  the hospital board, or the regulator?

### A3. The same table, printed by the trainer

```bash
uv run python scripts/03_train_model.py
```

Section 5 prints the same trade-off for seven thresholds. Nothing is retrained
between those rows. Convince yourself of that.

---

## B. Break the data feed

The Bundles on disk are never modified — the damage is applied in memory as
they are read.

### B1. A hospital stops sending a measurement

*(These two used to have a slide of their own. They are here now — run them
in a gap, or when you finish a section early.)*

```bash
uv run python scripts/01_fhir_to_table.py --drop area
```

- How many columns come out now?
- Did anything raise an error?
- What would happen if you fed this table to a model trained with `area`?

### B2. A hospital renames a code

```bash
uv run python scripts/01_fhir_to_table.py --rename radius:tumor_rad
```

- Look at the column list. Where did `radius` go?
- The proof section still passes. Why is that *worse* than failing?

---

## C. Make the model worse on purpose

### C1. Starve it of training data

```bash
uv run python scripts/03_train_model.py --test-size 0.8
```

Only 20% of patients are used for training.

- Read section 6 carefully. One of those metrics goes **up**. Which one, and
  would you have caught the problem if that were the only number you watched?
- Missed tumours go from 3 to 21. Say in one sentence why accuracy did not
  notice.
- The two runs are not even scored on the same patients — the second tests on
  456, the first on 114. Does that make the comparison better or worse?

### C2. A different random split

```bash
uv run python scripts/03_train_model.py --seed 7
uv run python scripts/03_train_model.py --seed 123
```

- How much do the numbers move between seeds?
- If two papers report recall 0.929 and 0.905, is either one better?

### C3. Cripple the forest

```bash
uv run python scripts/03_train_model.py --forest-trees 3
```

### C4. Remove the engineered features

```bash
uv run python scripts/03_train_model.py --no-engineered
```

- Were `compactness_ratio` and `concavity_per_radius` earning their place?
- Recall, precision and accuracy do not move at all. Only ROC-AUC does, by
  0.003. If you had spent a week building those two features, what would you
  write in the report?

### C5. Combine two changes

```bash
uv run python scripts/03_train_model.py --test-size 0.6 --seed 7
```

- Can you predict the direction of the change before you press enter?
- Run it again with `--seed 11`. How much of what you just saw was the change,
  and how much was the shuffle?

---

## D. Clustering without labels

### D1. Ask for more groups

```bash
uv run python scripts/04_cluster_patients.py --clusters 3
uv run python scripts/04_cluster_patients.py --clusters 5
```

- Does the Adjusted Rand Index go up or down?
- Can you give each of the five groups a clinical name?
- If you cannot, what does that tell you about the five groups?

### D2. A different starting point

```bash
uv run python scripts/04_cluster_patients.py --clusters 3 --seed 99
```

- Are the same patients grouped together as before?

---

## E. Look at the data differently

```bash
uv run python scripts/02_explore_data.py --feature area
uv run python scripts/02_explore_data.py --feature fractal_dimension --bins 15
```

Open `reports/01_top_feature.png` after each run.

- Which measurement separates the two groups most cleanly?
- Which one barely separates them at all? Should it stay in the model?

---

## If you still have time

Now you may edit code. Add a third model to the `candidates` dictionary in
`scripts/03_train_model.py`:

```python
from sklearn.ensemble import GradientBoostingClassifier
"Gradient Boosting": GradientBoostingClassifier(random_state=args.seed),
```

Does the extra complexity buy anything you would be willing to defend to a
clinician?

---

## F. Put the answer back where it came from

### F1. Read the resource, not the number

Press **Send to record** at the bottom of the Streamlit app.

- Find `performer`. Why does it point at a `Device` and not a `Practitioner`?
- Find `basis`. What could you do a year from now that you could not do if it
  were missing?
- The resource says `RiskAssessment`. What would change, legally and
  clinically, if the app wrote a `Condition` instead?

### F2. The threshold, in FHIR terms

```
http://127.0.0.1:8000/sample/P0216/fhir?threshold=0.5
http://127.0.0.1:8000/sample/P0216/fhir?threshold=0.2
```

- `probabilityDecimal` is identical in both. `qualitativeRisk` is not.
- Which of those two fields would you put in front of a clinician, and why?

### F3. What is still missing

The request in the app would be rejected by a real hospital for at least four
reasons. Name them. (Hint: one is in the URL, one is a header that is not
there, one is a resource this app never creates, and one is not technical at
all.)
