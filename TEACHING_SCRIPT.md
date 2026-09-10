# Teaching script — two hours, minute by minute

Minute by minute. Lines in **quotation marks** are things to say more or less
as written; everything else is direction. You will not use all of it — the
point is that you never have to invent a sentence while thirty people watch.

---

## Twenty-three slides, three parts

| | minutes |
|---|---|
| Students typing, running, reading their own output | ~68 |
| You talking | ~52 |
| Slides | 23 |

Slightly over 2 minutes of speaking per slide on average, but the average is
not the point: five pages are one-line punctuation you leave up for forty
seconds, and four are hands-on blocks you stand on for ten minutes each. The
terminal is the teaching material; the slides are punctuation.

**Every step is numbered on the slide it belongs to**, and every command they
have to type is on one, and Page 3 groups the afternoon into the three parts
they belong to. A student who only ever looks at the
projector still knows where they are and what to run.

| Part | What | Slides |
|---|---|---|
| — | Cover, recap of HL7 v2 and FHIR, agenda, ten numbers | 1–4 |
| 0 | Install uv, build the environment | 5 |
| 1 | **To a table** — Bundles in, rows out, and where the data came from | 6–9 |
| 2 | **To a model** — the columns we wrote, train, judge, turn knobs | 10–18 |
| 3 | **To a service** — app, HTTP, and back into the record as FHIR | 19–23 |
| — | Close, no slide | — |

Pages 12–13 and 15–17 exist because the morning was FHIR, not machine
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
cd fhir-ml-workshop
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
2.  git clone https://github.com/AIT-brainlab/fhir-ml-workshop.git
3.  cd fhir-ml-workshop
4.  uv sync                        <- only works inside the folder
```

---

## 00:00 – 00:10 · Framing  (slides 1–4)

**Slide 1 — cover**

> "This morning you were handed a phrase: *impedance mismatch*. Hierarchical
> FHIR trees on one side, flat two-dimensional feature matrices on the other,
> and nothing joining them."

> "For the next two hours we fix that by hand. By the end every one of you will
> have a model running on your own laptop, answering questions over HTTP, and
> you will be able to tell me why it should not be allowed near a patient."

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
> reason the flattening script can name a column after Observation.code — and it is why
> everything you do this afternoon starts from the lower box."

The honest footnote if anyone asks: FHIR did not replace v2. It is usually
bolted onto the front of a hospital that is still running v2 underneath.

If nobody has a question, move straight on.

**Slide 3 — agenda**

Three boxes. Read the headings, not the bodies — the bodies are there for the
people who look back at the projector ten minutes from now.

> "Three moves this afternoon. One: to a table — FHIR Bundles become rows and
> columns. Two: to a model — train two, judge them on the error that costs a
> patient, then turn four knobs and watch. Three: to a service — serve it on
> your own laptop and write the prediction back into the record as FHIR."

> "Every line of code is supplied. Your job is to run it, read what comes back,
> and decide whether the result deserves trust. That last part is the only one
> I am marking."

**Slide 4 — ten numbers**

This gets asked every single time, so answer it before anybody raises it.

First agree with the morning, or this lands as a contradiction.

> "You have just heard that protocols may have to become AI-ready, that MCP and
> RAG are coming. I agree with all of it. Now let me narrow it to the job in
> front of us today."

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
> very good at, and it is the one we are about to do by hand in Part 1 — reading
> a free-text pathology report into structured fields, and mapping a local code
> onto LOINC. That is feature engineering, which has a page of its own after
> the break. It is still an open
> problem, and solving it is worth more than another percent of accuracy on
> stage three."

*Timing check: you should be starting slide 5 at 00:10.*

---

## 00:10 – 00:20 · Get everyone running  (slide 5)

**Slide 5 — install uv first**

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

## 00:20 – 00:44 · Part 1, Bundles become rows  (slides 6, 7, 8, 9)

**Slide 6 — section divider · PART 1, to a table**

> "Everything from here is this morning's material, executed."

**Slide 7 — one patient, twelve resources**

Read the lead-in line first. Do not say "twelve" until the three rows are done.

> "A patient is not one record. In FHIR it is a bag of small linked objects —
> each one is called a resource, each one stands on its own, and each one points
> back at the same person."

Then the three rows, in order.

> "`Patient` — who this is. In our data that is an identifier and nothing else:
> no name, no age, no sex. Remember that when we get to fairness."

> "`Observation` — one measurement each, ten of them. These are the columns of
> the table we are about to build."

> "`Condition` — the biopsy result. That is the label, the thing we predict."

Only now the card.

> "One, ten and one. Twelve resources for one patient, in one file — and that
> is a small bundle. A real chart has hundreds."

Then walk the table on the right. Read three or four codes out loud, not all
ten — the point is that each one is a separate resource with a name.

> "These ten are the Observations. `radius`, `texture`, `perimeter` — every one
> of them arrives as its own object, and every one becomes a column. Nobody
> measured these by hand: they were computed off a digitised image of the cells
> from a needle biopsy."

> "There is no LOINC code for any of them, because LOINC does not cover image
> morphometry. They travel under a local code instead, and that is not an
> exotic problem — it is the normal one."

Now switch to the browser tab with `P0001.json` open. Scroll it slowly.

> "Notice three things. `code` says *what* was measured — the column name comes
> from the coded concept, not from a position in a file. `subject` points back
> at the patient; that is your join key. And the number you actually want,
> 17.99, is buried three levels deep inside `valueQuantity`."

> "Notice also what is *not* here. No name. No age. No sex. Hold that thought —
> we come back to it at the end and it turns out to be the most important thing
> on the slide."

**Slide 8 — flattening**

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

> "Section four. 569 Bundles went in, 569 rows came out, and every one of them
> matches `data/patients.csv` value for value — except P0010, which has the
> hole we just looked at."

> "Two flags in `EXERCISES.md` break this on purpose: `--drop area` makes a
> hospital stop sending a measurement, and `--rename` makes one rename a code.
> Neither raises an error. The second one is worse — the check still passes,
> because it only compares the columns that still match. A pipeline that fails
> loudly gets fixed on Tuesday; this one gets fixed three months after somebody
> notices the model got worse. Run them in the gaps."

> "That matters more than it sounds. What is on your screen is not a demo
> slice. It is the exact table the model trains on in half an hour. Nothing in
> this workshop was flattened for you behind the scenes."

---

**Slide 9 — real or made up?**

Answer this before a student works it out and wonders what else was glossed
over. One minute.

> "Fair question at this point: is any of this real?"

Read the top row of the diagram, left to right.

> "The measurements and the diagnoses are real — 569 patients, a published
> research dataset from one American hospital in the 1990s. That is what the
> model will train on."

> "The FHIR files you just opened, I wrote. That script took all 569 rows and
> packaged each one as a Bundle. Real numbers, our wrapping."

Then the red dashed line.

> "Which is exactly why I can check the parser. I knew the answer before I
> started, so when the script hands back a table it has to match the rows I started
> from, exactly. That is what `Identical to patients.csv : True` means."

> "In a real project nobody hands you the answer. You parse a hospital feed and
> nothing anywhere tells you whether you got it right. That is why this step
> eats the calendar."

If asked why only 20: 569 Bundles is 6,800 resources and nobody can read that.
Twenty is enough to see the shape and to hide one broken record in.

## 00:44 – 00:54 · Part 2 opens, and the columns we wrote  (slides 10, 11)

**Slide 10 — section divider · PART 2, to a model**

> "You have a table. Nothing you have done so far is machine learning. That
> starts now."

**Slide 11 — feature engineering**

Ninety seconds, and it is a set-up, not a result. Do not tell them yet that it
did not work.

> "One thing has to be defined before we go on, because nobody has given you a
> definition. Feature engineering is writing *new columns* out of the ones
> you were sent. No new data arrives from anywhere. You do arithmetic on what
> you already have, because the raw columns do not say the thing you care
> about."

> "The Bundle carried ten measurements. The model is about to train on twelve.
> The other two, we wrote."

Point at the two shapes.

> "These two have exactly the same area. `radius`, `perimeter` and `area` all
> struggle to tell them apart — but perimeter squared over area is 12.6 for the
> round one and 33.4 for the ragged one. That ratio describes shape without
> caring about size, and a small but very irregular mass is exactly the one you
> worry about."

> "So we wrote two: `compactness_ratio` and `concavity_per_radius`. Four lines
> of Python in `common.py`. No hospital sent them; nobody could have. This is
> what feature engineering is, and it is a large part of what a data scientist
> is actually paid to do."

> "Remember that we were pleased with ourselves. We come back to it."

---

## 00:54 – 01:12 · What a model is, and was the split fair  (slides 12, 13)

**Nobody has defined any of this yet.** The morning was FHIR. Do not skip to
the results table — three slides, eight minutes, no typing.

**Slide 12 — two models**

Read the line under the title first. It is the only definition of "model"
anybody gets today.

> "A model is a rule found from examples that already have the answer. Feed it
> a patient it has never seen and it hands back a probability. *Training* is the
> search for that rule — it is not the memorising of answers, and that
> distinction is the whole reason we hold patients back."

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

**Slide 13 — was that split fair?  (k-fold cross-validation)**

The whole page is one question. Ask it before you answer it.

> "We shuffled 569 patients once and locked 114 of them away. That is a *draw*,
> not a measurement. What if the 114 we happened to hold back were the easy
> ones? What if every awkward patient landed in training instead? Nothing
> inside a single split can tell you — the number would look just as
> convincing either way."

Let that sit. Then point at the five bars.

> "So before the drawer is opened at all, the 455 training patients get cut
> five ways and the model refitted five times, a different fifth held back each
> round. Same model, same data. Recall comes out anywhere between 0.853 and
> 0.941 depending on which patients it happened to see."

> "Mean 0.900, spread plus or minus 0.040. That spread is the honest width of
> the answer. When somebody quotes you a single number to three decimals, this
> is the question to ask them — and most of the time nobody has run it."

Only now the dashed box at the top, and keep it short.

> "One more thing falls out of this. Each of those five refits has to relearn
> the median that fills a gap and the mean that centres a column, from its own
> patients only — otherwise the fold is scoring itself on numbers it helped
> compute. That is why impute, scale and classify are saved as one object.
> `common.py` exists so nobody can accidentally take them apart."

---

## 01:12 – 01:26 · Train it, then change one thing  (slide 14)

**The longest hands-on block of the afternoon. Ten minutes of typing, four of
talking. Walk the room the whole time.**

**Slide 14 — change one thing**

**First, the plain run — everybody, now.** This is the baseline every later run
is compared against, and nothing on this page works without it.

```bash
uv run python scripts/03_train_model.py
```

> "Twenty seconds. That is the whole of what people call machine learning. Do
> not try to read the numbers yet — we spend the next three slides on what they
> mean. For now just watch what happens when you change one thing."

> "Two commands. Each one changes exactly one setting, and the script remembers
> your first run, so section five prints the difference for you."

> "Before you press enter, say out loud to the person next to you which
> direction you think it moves. Then run it and find out whether you were
> right."

```bash
uv run python scripts/03_train_model.py --no-engineered
uv run python scripts/03_train_model.py --test-size 0.8
```

Give them five minutes. Then pull the room back and take the cards in order.

> "One. Remember slide eleven — the two features we wrote ourselves, for
> perfectly good clinical reasons, that a pathologist would have nodded at.
> Drop them both. Every number the slides report comes back identical."

*(If somebody is watching the terminal closely: ROC-AUC moves by 0.003. It is
not on any slide because we never defined it — do not open that door unless
you have a spare three minutes.)*

> "And you already saw why, in section seven of the profiling step. `radius`,
> `perimeter` and `area` correlate with each other at 0.99 — one measurement
> written three ways. `compactness_ratio` is perimeter squared over area, built
> out of two columns the model already had and already knew were saying the same
> thing. There was no new information in it to find."

> "They bought us nothing measurable. That is a real result and you report it.
> The alternative is a career of quietly keeping features because you liked the
> idea — and this is the single most useful habit you can take out of today:
> test the thing you are proud of, and believe the answer."

> "Two. Train on 113 patients instead of 455 and accuracy goes *up*, from
> 0.930 to 0.941 — while missed tumours go from three to twenty-one. The two
> runs are not even scored on the same patients. No single headline number
> settles anything, and recall is the one with a person attached to it."

---

> "Hold both of those. In three slides you will know exactly which of those
> numbers was the one that mattered — and it is not the one that moved least."

---

## 01:26 – 01:40 · What those numbers meant  (slides 15, 16, 17, 18)

**Slide 15 — how we measure**

The page is not a list of three definitions. It is one claim: *these three
numbers disagree, and the disagreement is the whole story.*

> "Before you believe any number, ask which patients it was measured on. We put
> 114 of our 569 in a locked drawer, train on the other 455, and score only the
> ones in the drawer. A model marking its own homework always looks brilliant."

Then the three words, slowly. Do not define them with a matrix — define them
with the question each one asks.

> "Accuracy counts every mistake the same. Recall asks how many of the tumours
> we caught. Precision asks how many of our alarms were real."

> "Three numbers, three different questions, same model. Which one you report is
> a decision somebody makes — and the next two slides are about making it."

Two slides before anybody sees a result: what accuracy is worth here, and
which of the two mistakes actually costs a patient. Then run it.

**Slide 16 — 62.7%**  ← the last thing on screen before any number

> "Before anybody shows you a metric this afternoon, including me, here is the
> number to keep in your head. 357 of our 569 patients are benign. A model that
> answers 'benign' for every single patient scores 62.7% accuracy — and detects
> nothing at all. Zero tumours. That is what accuracy is worth here."

**Slide 17 — which error?**

> "These two mistakes are not the same size. A false negative sends a patient
> home with an untreated malignancy; it surfaces months later, if ever, and it
> is often irreversible. A false positive sends a healthy patient for a biopsy
> they did not need; it costs money, it is frightening, and it is over in a
> week."

> "Accuracy weights those two equally. That is the whole problem."

```bash
uv run python scripts/03_train_model.py
```

**Slide 18 — the results**

> "Accuracy: 0.930 and 0.930. Identical. On that metric these two models are
> indistinguishable, which tells you accuracy is the wrong summary."

> "Recall: 0.929 against 0.881. Logistic Regression missed three malignant
> tumours out of the 114 patients in the test set. Random Forest missed five.
> Same accuracy. Two more cancers. The simpler model wins, and it wins for a
> reason you can explain to a doctor."

> "So — the answer to the question the Model A / Model B slide left open, and
> the numbers you already had on screen twenty minutes ago without knowing what
> they meant. The three hundred
> trees were more flexible and they were not better. They were worse at the one
> thing we care about. Complexity is not a strategy."

---

## 01:40 – 01:54 · Part 3, deployment + the two minutes that matter  (slides 19–23)

**Slide 19 — section divider · PART 3, to a service**

> "A model in a notebook helps nobody. The rest of the afternoon is about
> putting it somewhere a clinician could reach it — and getting the answer back
> into the record it came from."

**Slide 20 — the app, four numbered moves**

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

**Slide 21 — what you see**

Put this up the moment you finish reading move 1, and leave it up for the whole
block. It is the reference screen.

> "This is what your laptop should look like after move 2. If yours does not,
> put your hand up now rather than in ten minutes."

Then, at the end of move 4, point at the two sidebars along the top.

> "Those two panels are the same model. Byte for byte the same weights, the
> same 569 patients. One of them sends thirty-four women home."

> "Somebody has to choose between those two panels. In a hospital, who? It is
> not the person who wrote the code, and it is not the model."

**Slide 22 — now over HTTP**

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

**Slide 23 — full circle**

The last thing they run, and the sentence the whole day was built to earn.

> "Scroll to the bottom of the app and press *Send to record*."

Let the JSON fill the screen before you say anything.

> "Remember the Raman spotlight this morning — the last thing it did was
> serialise a sensor reading into FHIR R4. This is the same move. That was an
> instrument writing into the record; this is a model writing into it."

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

## 01:54 – 02:00 · Close  (stay on slide 23)

**No slide for this. Leave FULL CIRCLE up and talk over it.**

There used to be a limitations page. It listed the three answers, which is
exactly the wrong thing to do ninety seconds before asking the room to find
them. Ask first. Use these only to fill a silence, one at a time.

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

The three you are fishing for, if nobody gets there:

- It has never seen a patient from this region or this decade — one American
  hospital, the 1990s. That it transfers here is an assumption with no evidence.
- It cannot be audited for bias, because the fields you would audit on are not
  in the data. That is not a limitation you fix with more compute.
- It predicts a *label*, not a disease — what a pathologist wrote down, errors
  included, reproduced with perfect confidence.

Ninety seconds per group. Push back hard on generic third answers:

> "That is true of every model ever built. Tell me something that is true of
> *this* one."

**Close:**

> "Most people can build the model. Far fewer can tell you where it breaks.
> You did the second thing today, which is the part that actually matters once
> there is a patient on the other end. Thank you — enjoy the rest of the week."

---

## Recovery plans

**Running 10 minutes late at 01:00** — skip the pipeline half of slide 13 and trim the
flags block on slide 14 to one command. That buys 8 minutes.

**Running 20 minutes late** — cut the flags block on slide 14 down to one
command, `--test-size 0.8`, and run it yourself from
the front, and read the second card out rather than making them run it.

**Never cut**: Part 1, slides 15–17 (without them the results mean nothing),
the P0216 demonstration, and the last 10 minutes.

**Running early** — send them to `EXERCISES.md` section C and D. Or ask them to
predict the direction of a change *before* pressing enter, then check.

---

## Questions you will get, and answers

**"Why is accuracy the same for both models?"**
Coincidence of this test set — 114 patients, and the two models trade a false
negative for a false positive. It is a gift for teaching, not a general rule.

**"Can we just use a bigger model / deep learning?"**
On 569 patients with 10 features, no. And it would not fix either blocker on
slide 11. Ask them which of the two blockers a bigger model solves. Neither.

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
Not as it stands, and that is the closing question of the day. What it would take:
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
