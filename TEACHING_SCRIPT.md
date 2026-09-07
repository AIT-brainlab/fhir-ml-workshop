# Teaching script — two hours, minute by minute

Minute by minute. Lines in **quotation marks** are things to say more or less
as written; everything else is direction. You will not use all of it — the
point is that you never have to invent a sentence while thirty people watch.

---

## Twenty-five slides, six steps

| | minutes |
|---|---|
| Students typing, running, reading their own output | ~68 |
| You talking | ~52 |
| Slides | 25 |

Slightly over 2 minutes of speaking per slide on average, but the average is
not the point: five pages are one-line punctuation you leave up for forty
seconds, and four are hands-on blocks you stand on for ten minutes each. The
terminal is the teaching material; the slides are punctuation.

**Every step is numbered on the slide it belongs to**, and every command they
have to type is on one. Page 3 lists all of them in one place, and the step
pages repeat the relevant one at the top. A student who only ever looks at the
projector still knows where they are and what to run.

| Step | What | Slides |
|---|---|---|
| — | Recap of HL7 v2 and FHIR | 2 |
| 0 | Install uv, build the environment | 6 |
| 1 | FHIR Bundles into a table | 7, 8, 9, 10 |
| 2 | Profile the data | 11, 12 |
| 3 | What a model is and how it is judged | 13, 14, 15 |
| 3 | Train, compare, choose an error | 16, 17 |
| 3 | Change one setting and re-read | 18, 19 |
| 4 | Cluster without labels | 20 |
| 5 | Serve it — app, API, then back as FHIR | 21, 22, 23, 24 |
| — | Limitations and close | 25 |

Pages 13–15 and 18–19 exist because the morning was FHIR, not machine
learning. Nobody in the room has been told what a model is, what a hold-out
set is for, or why anyone would report four numbers instead of one. Without
those five pages the afternoon opens on a results table, which teaches
nothing.

There is no hand-in slide. The three questions still get asked in the last ten
minutes, out loud — see the closing block — but putting them on a slide made
it read like an exam.

---

## Before anyone arrives

```bash
cd health-ai-workshop
uv sync
uv run python scripts/03_train_model.py     # records reports/baseline.json
uv run uvicorn app.api:app --reload         # leave running in a spare terminal
```

That third command matters: the first default run becomes the baseline every
student's later run is compared against. Skip it and the first person to try a
flag sees nothing to compare.

Have open on your machine, ready to alt-tab:

1. Terminal A — your repo, clean prompt
2. Terminal B — the API already running on :8000
3. Browser tab 1 — `data/fhir/P0001.json`
4. Browser tab 2 — `http://127.0.0.1:8000/docs`
5. The deck

Write on the whiteboard before they sit down:

```
1.  github.com/astral-sh/uv        <- install this FIRST
2.  git clone <URL>
3.  cd health-ai-workshop
4.  uv sync                        <- only works inside the folder
```

---

## 00:00 – 00:12 · Framing  (slides 1–5)

**Slide 1 — cover**

> "This morning you learned what FHIR is. For the next two hours you are going
> to use it. By four o'clock every one of you will have a model running on your
> own laptop that answers questions over HTTP, and you will be able to tell me
> why it should not be allowed near a patient."

> "The code is already written. Two hours is not enough to type it, so we are
> going to spend the time running it and looking hard at what comes back
> instead. If you want to change something, there are flags for that, and the
> last exercise does open the editor."

**Slide 2 — this morning**

Thirty seconds. They had two hours of this before lunch; this is a reminder,
not a second lecture.

> "Quick recap, because it is after lunch. Both boxes are HL7 standards. The
> top one is v2, from 1989, and it still carries most hospital traffic in the
> world today. The bottom one is FHIR, from 2014."

Point at the red carets.

> "Same measurement, same patient, both boxes. In v2, seventeen point nine nine
> means something because it is the fifth field of that line. Count wrong and
> you get the wrong number, and nothing anywhere tells you."

> "In FHIR the meaning travels *with* the value, as a code. That is the only
> reason Step 1 can name a column after Observation.code — and it is why
> everything you do this afternoon starts from the lower box."

The honest footnote if anyone asks: FHIR did not replace v2. It is usually
bolted onto the front of a hospital that is still running v2 underneath.

If nobody has a question, move straight on.

**Slide 3 — five steps, one model**

Walk the five lines. Then:

> "Step 1 is the unusual one. Most machine learning courses hand you a clean
> CSV on a plate. Clinical data never arrives that way, and the distance
> between what a hospital sends and what scikit-learn eats is where most health
> AI projects quietly fail. So we start there."

**Slide 4 — four stages**

> "Any clinical AI system has four stages. A source system that speaks FHIR.
> A feature table. A model. And something a clinician can actually act on."

Point at stage 3.

> "That box, and only that box, is machine learning. It is also the box that
> takes the least time in a real project, because it is library calls. Boxes two
> and four are where projects die. We are doing all four this afternoon."

**Slide 5 — ten numbers**

This gets asked every single time, so answer it before anybody raises it.

> "Fair question before we start. It is 2026 — why are we not using an LLM for
> this?"

Point at the left-hand card.

> "That is the model's entire input. Ten numbers. An LLM's advantage is
> unstructured text, and there is none here."

> "And look at what we need out of it. A calibrated probability, so we can put a
> threshold through it — that is the whole second half of this afternoon. The
> same answer every single time it runs, because a regulator will ask. Twelve
> coefficients a clinician can actually read. It trains in twenty seconds, on
> your laptop, offline, with no patient data leaving the building."

Then the lower card.

> "Now the honest half. There *is* a job here that a language model would be
> very good at, and it is the one we are about to do by hand in Step 1 — reading
> a free-text pathology report into structured fields, and mapping a local code
> onto LOINC. That is stage two from the last slide. It is still an open
> problem, and solving it is worth more than another percent of accuracy on
> stage three."

*Timing check: you should be starting slide 6 at 00:12.*

---

## 00:12 – 00:22 · Step 0, get everyone running  (slide 6)

**Slide 6 — install uv first**

**Do not let anyone type `uv sync` yet.** Two things have to be true first.

> "Everything today runs through a tool called uv. If you did not install it
> last night, install it now — the link is on the slide, and it is on the
> board."

Write on the board: **https://github.com/astral-sh/uv**

> "It is not a pip package. You do not need Python installed to get it, and you
> do not need pip. The installer is a standalone binary, and uv will download
> the right Python for you a minute from now."

> "Second thing: `uv sync` only works from *inside* the cloned folder, because
> it reads the lockfile in that directory. If you run it from your home folder
> it will tell you there is no pyproject.toml. That is the most common first
> error in this room, every time."

Only once people have `uv --version` printing something:

> "Now `uv sync`. It reads a lockfile that pins the exact version of all
> sixty-six packages, so every laptop in this room ends up identical. That is
> not housekeeping — it is the difference between a result and an anecdote. If
> your number cannot be reproduced on another machine, it is not a number."

Then stop talking and work the room.

**This is the block that eats your schedule if you let it.** Rules:

- Anyone still failing at 00:18 gets paired with a working neighbour. Do not
  debug one laptop while twenty-nine wait.
- `uv: command not found` → not installed, or terminal not restarted.
- `No pyproject.toml found` → they are not inside the cloned folder.
- No git on a Windows laptop → GitHub **Code → Download ZIP**.
- Corporate laptop blocking the installer script → `pip install uv` works as a
  fallback if they already have Python.
- Wifi crawling → USB stick with the pre-built `~/.cache/uv`, then
  `uv sync --offline`.

When most screens are green:

> "From now on, every command starts with `uv run`. You never activate
> anything. If you get ModuleNotFoundError, you forgot those two words."

---

## 00:22 – 00:40 · Step 1, Bundles become rows  (slides 7, 8, 9)

**Slide 7 — section divider**

> "Everything from here is this morning's material, executed."

**Slide 8 — one patient, twelve resources**

Switch to the browser tab with `P0001.json` open. Scroll it slowly.

> "This is one patient. Twelve resources describe them: one Patient, ten
> Observations, one Condition."

> "Notice three things. `code` says *what* was measured — the column name comes
> from the coded concept, not from a position in a file. `subject` points back
> at the patient; that is your join key. And the number you actually want,
> 17.99, is buried three levels deep inside `valueQuantity`."

> "Notice also what is *not* here. No name. No age. No sex. Hold that thought —
> we come back to it at the end and it turns out to be the most important thing
> on the slide."

**Slide 9 — flattening**

> "Fifty lines of Python turn that into one row per patient. There is no
> library call for this. Somebody writes it, by hand, for every source system
> they integrate. Run it."

```bash
uv run python scripts/01_fhir_to_table.py
```

Give them 90 seconds to read their own output, then drive from the front.

> "Section three. Look at patient P0010."

> "The `texture` measurement is missing. Not zero. Not an error. The Observation
> simply was not in the Bundle, so pandas gave you NaN and moved on. Nothing
> raised. Nothing logged."

> "This script printed a warning. Most production pipelines do not. So ask
> yourself how you would ever have found out — and the honest answer is that
> you would not, until somebody noticed the model had quietly got worse."

> "Section four proves the twenty rows you just built are identical to the
> 569-row CSV we shipped. Same procedure, run over everybody."

---

## 00:40 – 00:52 · Break the feed on purpose  (slide 10)

**Slide 10 — what breaks once the feed is real**

> "Everything works perfectly on the twenty Bundles I prepared for you. Let's
> stop that. Type this."

```bash
uv run python scripts/01_fhir_to_table.py --drop area
```

> "A hospital upgraded their LIS and stopped sending one measurement. Look at
> your column count. Eleven instead of twelve. Did anything go wrong on your
> screen? No. Would your model notice? It would produce numbers for every
> patient, all of them wrong, and never complain."

Then:

```bash
uv run python scripts/01_fhir_to_table.py --rename radius:tumor_rad
```

> "Now a hospital renamed a code. Where did `radius` go? The proof section still
> says the comparison passed — because it compared the columns that still match.
> Passing silently is worse than failing loudly. A pipeline that fails loudly
> gets fixed on Tuesday. This one gets fixed after somebody notices the model
> got worse, three months later."

> "The files on your disk were never modified, by the way. The damage happens in
> memory as they are read. Check `git status` if you don't believe me."

Walk the third card on the slide (duplicated patients) verbally — no command
for it.

---

## 00:52 – 01:00 · Step 2, profile before you model  (slides 12, 11)

```bash
uv run python scripts/02_explore_data.py
```

**Slide 12 — 62.7%**  ← show this *before* discussing any result

> "Before anybody shows you a metric this afternoon, including me, here is the
> number to keep in your head. 357 of our 569 patients are benign. A model that
> answers 'benign' for every single patient scores 62.7% accuracy — and detects
> nothing at all. Zero tumours. That is what accuracy is worth here."

**Slide 11 — fit to model?**

> "We wrote this assessment down *before* fitting anything. Complete, labelled,
> no leakage, workably balanced. Two blockers."

> "No demographics. Not one. No age, no sex, no ethnicity, no comorbidity. So
> the subgroup fairness analysis that any regulator would demand before this
> touched a patient — we cannot run it. Not 'we did not bother'. We *cannot*."

> "Second, one time point, no follow-up. This is diagnosis, not prognosis. If
> anyone asks whether this predicts patient outcomes: it does not, and the data
> makes that impossible."

If time allows, one flag:

```bash
uv run python scripts/02_explore_data.py --feature fractal_dimension
```

> "Some measurements barely separate the groups at all. Should they be in the
> model?"

---

## 01:00 – 01:10 · What a model is  (slides 13, 14, 15)

**Nobody has defined any of this yet.** The morning was FHIR. Do not skip to
the results table — three slides, ten minutes, no typing.

**Slide 13 — two models**

> "A model here is one function. Ten numbers in, one probability out. We build
> it by showing it patients whose biopsy result we already know and letting it
> adjust itself until it mostly agrees with them. That is all 'supervised
> learning' means."

Point at Model A.

> "Logistic regression can only draw one straight boundary. Every measurement
> gets a weight, and you can print the twelve weights out and read them to a
> doctor."

Point at Model B.

> "A random forest grows three hundred decision trees on random slices of the
> data and lets them vote. It can carve out shapes a straight line cannot.
> Nobody reads three hundred trees, so you take the answer on trust."

> "Both pictures are the real models fitted on our real patients, squashed down
> to two dimensions so they fit on a slide. Hold on to one question: is the
> flexible one better? We will have the answer in ten minutes."

**Slide 14 — how we measure**

> "Before you believe any number, ask which patients it was measured on. We put
> 114 of our 569 patients in a locked drawer, train on the other 455, and score
> only the ones in the drawer. A model marking its own homework always looks
> brilliant."

Walk the four cells on the matrix, in this order, and do not name a metric
until you have.

> "Sixty-seven benign patients we correctly left alone. Five healthy patients
> we sent for a biopsy they did not need. Thirty-nine tumours we caught. And
> three — bottom left — three tumours we called benign and sent home. That is
> the cell with a person in it."

> "Now the two fractions, and they come straight off the picture. Recall is the
> bottom row: of all the tumours that were there, how many did we catch?
> Thirty-nine out of forty-two, 0.929. Precision is the right-hand column: of
> all the alarms we raised, how many were real? Thirty-nine out of forty-four,
> 0.886. Accuracy just adds up the two green cells and treats every mistake as
> the same size."

**Slide 15 — one object**

> "Two things go wrong after the maths is finished, and both are on this slide."

> "First: the median we use to fill a gap, and the mean we use to centre a
> column, are *learned* from the training patients. They are part of the model.
> Impute, scale, classify go into one object and get saved as one file. If your
> app recalculates them from whatever data it happens to have, your app is
> running a different model from the one you tested — and nothing anywhere will
> raise an error. `common.py` exists in this repo so that cannot happen."

> "Second: the five bars. Before the drawer is opened at all, the training half
> gets cut five ways and the model refitted five times. Same model, same data,
> and recall comes out anywhere between 0.853 and 0.941 depending on which
> patients it happened to see. One split was never evidence."

---

## 01:10 – 01:20 · Step 3, train and choose  (slides 16, 17)

```bash
uv run python scripts/03_train_model.py
```

**Slide 16 — the two models**

> "Accuracy: 0.930 and 0.930. Identical. On that metric these two models are
> indistinguishable, which tells you accuracy is the wrong summary."

> "Recall: 0.929 against 0.881. Logistic Regression missed three malignant
> tumours out of the 114 patients in the test set. Random Forest missed five.
> Same accuracy. Two more cancers. The simpler model wins, and it wins for a
> reason you can explain to a doctor."

> "So — the answer to the question from three slides ago. The three hundred
> trees were more flexible and they were not better. They were worse at the one
> thing we care about. Complexity is not a strategy."

**Slide 17 — which error?**

> "These two mistakes are not the same size. A false negative sends a patient
> home with an untreated malignancy; it surfaces months later, if ever, and it
> is often irreversible. A false positive sends a healthy patient for a biopsy
> they did not need; it costs money, it is frightening, and it is over in a
> week."

> "Accuracy weights those two equally. That is the whole problem."

**Then the threshold table — section 5 of their output.**

> "Scroll up to section five in your terminal. Seven rows. At threshold 0.20 the
> model misses two tumours and raises nine false alarms. At 0.80 it misses eight
> and raises one."

> "Now the important part: **nothing was retrained between those rows.** One
> model. One set of weights. Seven different answers, because somebody moved a
> number."

> "Which row would you ship? And would your answer change if this were not a
> screening programme, but a confirmatory test after a radiologist had already
> seen something suspicious? It should. Same model, different clinical setting,
> different right answer."

---

## 01:20 – 01:34 · Four flags  (slides 18, 19)

**The longest hands-on block of the afternoon. Ten minutes of typing, four of
talking. Walk the room the whole time.**

**Slide 18 — four flags**

> "Four commands. Each one changes exactly one setting. The script remembers
> your first run, so section six prints the difference for you — you do not
> have to remember what the numbers were."

> "Before you press enter, say out loud to the person next to you which
> direction you think it moves. Then run it and find out whether you were
> right."

```bash
uv run python scripts/03_train_model.py --threshold 0.30
uv run python scripts/03_train_model.py --no-engineered
uv run python scripts/03_train_model.py --missing 0.30
uv run python scripts/03_train_model.py --test-size 0.8
```

Give them eight minutes. Then pull the room back and take the cards in order.

> "One. Lower the threshold to 0.30 and we go from three missed tumours to one,
> at the cost of two more false alarms. Accuracy does not move at all — it
> cannot see the trade you just made."

> "Two, and this is the honest one. We engineered two extra features by hand —
> a shape ratio and a concavity per unit radius — for perfectly good clinical
> reasons. Drop them both and recall, precision and accuracy are *identical*.
> They bought us nothing measurable. That is a real result and you report it.
> The alternative is a career of quietly keeping features because you liked the
> idea."

> "Three. Delete the texture measurement for thirty per cent of the patients.
> No error. No warning. The imputer fills the holes with the median and the run
> completes exactly as before — and two more tumours go home undetected. If you
> only watched the terminal for red text you would have shipped that."

> "Four is the one worth a slide of its own."

**Slide 19 — accuracy rose, the model got worse**

> "Train on 113 patients instead of 455. Accuracy goes *up*, from 0.930 to
> 0.941. Missed tumours go from three to twenty-one."

Let that sit for a moment.

> "If accuracy were the number on your dashboard, that change looks like an
> improvement and you would have promoted it."

> "There is a second problem underneath, and it is worth saying out loud. Those
> two accuracies were not even measured on the same patients — the second run
> tested on 456 people, the first on 114. So they are not comparable at all.
> Any single headline number, on its own, is a decoration."

> "What would you put on the dashboard for a screening tool? Defend it."

---

## 01:34 – 01:40 · Step 4, structure without labels  (slide 20)

**Slide 20 — groups**

```bash
uv run python scripts/04_cluster_patients.py
```

> "This algorithm never saw a diagnosis. It grouped patients purely on the
> measurements. Look at the crosstab — cluster one is almost entirely
> malignant. Adjusted Rand Index against the true diagnosis: 0.65."

> "The signal was already in the data. Labelling only told us which group to be
> frightened of."

> "That is genuinely useful when labels are expensive. Cluster first, then pay a
> pathologist to adjudicate a handful of cases per group instead of the whole
> cohort."

Then:

```bash
uv run python scripts/04_cluster_patients.py --clusters 5
```

> "Ask for five groups and you get five groups. ARI drops from 0.65 to 0.32.
> Can anyone give me a clinical name for group four? No? That is the trap. The
> algorithm will always answer. It has no way of telling you the answer is
> meaningless."

*If you are behind schedule, this is the block to cut. Say the two sentences
about K-Means and move on.*

---

## 01:40 – 01:54 · Step 5, deployment + the two minutes that matter  (slides 21, 22)

**Slide 21 — the app, four numbered moves**

This slide is a walkthrough, not a summary. Read the four boxes out in order and
wait for the room at each one. Nobody moves on until their screen shows a risk
band.

> "A model nobody can call is not a system. Four moves, in order."

**1 · Start it.**

```bash
uv run streamlit run app/streamlit_app.py
```

**2 · Load a real patient.**

> "In the sidebar, click 'Patient with a malignant tumour'. All ten sliders jump
> to that patient's real measurements."

**3 · Move a slider.**

> "Drag Concave points. The probability moves and the risk band changes colour.
> Nothing is being retrained — you are re-scoring one patient."

**4 · Move the threshold.**

> "Now find the Decision threshold slider and move it slowly. The curve in the
> middle of this slide is exactly what you are dragging along."

> "It is telling you, live, what that threshold would do to all 569 patients. At
> 0.20 you miss seven tumours and send thirty-nine healthy women for a biopsy.
> At 0.50 you miss twenty and alarm ten. At 0.80 you miss thirty-four and alarm
> one."

> "The model has not changed once while you did that."

**Slide 22 — what you see**

Put this up the moment you finish reading move 1, and leave it up for the whole
block. It is the reference screen.

> "This is what your laptop should look like after move 2. If yours does not,
> put your hand up now rather than in ten minutes."

Then, at the end of move 4, point at the two sidebars along the top.

> "Those two panels are the same model. Byte for byte the same weights, the
> same 569 patients. One of them sends thirty-four women home."

> "Somebody has to choose between those two panels. In a hospital, who? It is
> not the person who wrote the code, and it is not the model."

**Slide 23 — now over HTTP**

> "Same model, second front door. Start the API, then ask it one question
> twice."

```bash
uv run uvicorn app.api:app --reload
```

### The two minutes that matter

Put the API on the projector. Type these live, one after the other:

```
http://127.0.0.1:8000/sample/P0216?threshold=0.5
http://127.0.0.1:8000/sample/P0216?threshold=0.2
```

> "P0216 is a real patient with a real, biopsy-confirmed malignant tumour."

First response:

> "At the default threshold, our model says **benign**. It missed her."

Second response:

> "At 0.2, the same model says **malignant**. It caught her."

> "Look at the probability field in both responses. 0.2164. Identical. Same
> patient, same model, same numbers. The only thing that changed is a line
> somebody drew."

> "So who is responsible for the difference between those two answers? Not the
> model — it did the same arithmetic both times. That threshold is not a
> hyperparameter. It is a clinical and ethical decision, and it should never be
> set silently in a line of Python by someone who has never met a patient."

Finish the loop:

> "One last thing. This morning you sent JSON over HTTP to a FHIR server and got
> JSON back. Just now you sent JSON over HTTP to your own model and got JSON
> back. That symmetry is not decoration — it is the reason FHIR made clinical AI
> integrable at all."

---

**Slide 24 — full circle**

The last thing they run, and the sentence the whole day was built to earn.

> "Scroll to the bottom of the app and press *Send to record*."

Let the JSON fill the screen before you say anything.

> "This morning you read a FHIR resource. Just now you produced one. Same
> standard, opposite direction. That is the entire day in one screen."

Then slow down on three words.

> "**RiskAssessment**, not Condition. The model contributes a number; it does
> not acquire the right to diagnose. FHIR puts that in the data model, not in
> a policy document."

> "**performer** points at a Device. In five years, anyone reading this chart
> can still tell that software wrote this line and not a doctor."

> "**basis** lists the ten Observations it came from. That is the only reason
> this score can ever be audited."

If someone asks what is still missing before this is real: authentication, a
Provenance resource, a validated model, and a regulator.

---

## 01:54 – 02:00 · Limitations and close  (slide 25)

**Slide 25 — limitations. Do not rush this. It is the whole point.**

Walk all three, slowly.

> "One. This model has never seen a patient from this region or this decade. It
> was fitted on one American hospital's cases from the 1990s. That it transfers
> here is an assumption with no evidence behind it."

> "Two. It cannot be audited for bias, because the fields you would audit on do
> not exist in the data. That is not a limitation you fix with more compute."

> "Three. It predicts a label, not a disease. The target is what a pathologist
> wrote down, errors included, and the model reproduces those errors with
> perfect confidence."

**Closing — say this, do not slide it**

> "Three things per group. One live prediction. Your confusion matrix and the
> metric you chose to optimise, with a reason. And one reason this model is not
> safe to use on real patients."

> "The third one is what I am marking. 'We need more data' does not count.
> Name something specific — a table, a column, a number you saw this afternoon."

Ninety seconds per group. Push back hard on generic third answers:

> "That is true of every model ever built. Tell me something that is true of
> *this* one."

**Close:**

> "Most people can build the model. Far fewer can tell you where it breaks.
> You did the second thing today, which is the part that actually matters once
> there is a patient on the other end. Thank you — enjoy the rest of the week."

---

## Recovery plans

**Running 10 minutes late at 01:00** — cut Step 4 entirely (say the two K-Means
sentences from slide 4's spot and move on). That buys 8 minutes.

**Running 20 minutes late** — cut the flags block on slide 18 down to two
commands, `--threshold 0.30` and `--test-size 0.8`, and run them yourself from
the front. Keep slide 19; it is thirty seconds and it is the best point of the
afternoon.

**Never cut**: Step 1, slides 13–14 (without them the results mean nothing),
slide 19, the P0216 demonstration, and the last 10 minutes.

**Running early** — send them to `EXERCISES.md` section C and D. Or ask them to
predict the direction of a change *before* pressing enter, then check.

---

## Questions you will get, and answers

**"Why is accuracy the same for both models?"**
Coincidence of this test set — 114 patients, and the two models trade a false
negative for a false positive. It is a gift for teaching, not a general rule.

**"Can we just use a bigger model / deep learning?"**
On 569 patients with 10 features, no. And it would not fix either blocker on
slide 10. Ask them which of the two blockers a bigger model solves. Neither.

**"Why 0.5 as the default threshold?"**
Because it is the library default, which is exactly the point. Nobody chose it
for this clinical problem. Somebody should.

**"Is the FHIR data real?"**
The measurements and diagnoses are real, from the published dataset. The FHIR
wrapping is ours — we re-encoded them so you could practise the parsing step.
The data card says so.

**"Why no LOINC codes?"**
Because none exist for image morphometry. We used a local CodeSystem rather
than invent LOINC codes to make the demo look tidier. Real integration projects
lose weeks to exactly this.

**"Could this be deployed in a hospital in the Philippines?"**
Not as it stands, and the honest answer is on slide 20. What it would take:
local data, local validation, demographics for a bias audit, prospective
follow-up, and a regulatory pathway.

---

## One-line cheat sheet

If you forget everything else, these five sentences carry the afternoon:

1. "The FHIR-to-table step is the job. Everything downstream is a library call."
2. "62.7% accuracy, and it detects nothing."
3. "Same accuracy. Two more cancers. The simpler model wins."
4. "Nothing was retrained between those rows."
5. "Who is responsible for the difference between those two answers?"
