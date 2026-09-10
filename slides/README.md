# Slides

`from-fhir-to-a-table.pptx` — 16 slides, built on the AIT brand presentation
template from Canva. Open and edit it in PowerPoint or Keynote as normal.

## Every number comes from a real run

`collect_results.py` executes the actual pipeline with the pinned seed
(`random_state=42`, `test_size=0.2`) and writes `results.json`. The deck text,
the figures and the instructor notes all read that file — no figure in the deck
is typed by hand, so the slides cannot drift away from the code.

```bash
uv run python slides/collect_results.py    # re-run the workshop, record the facts
python3 slides/apply_results.py            # push them into the existing deck
```

`apply_results.py` and `build_from_template.py` need **python-pptx**, which is
deliberately *not* a workshop dependency — students never run them. Install it
separately if you want to rebuild the deck: `pip install python-pptx`.

## How it was made

1. The AIT brand template was copied in Canva and exported as `.pptx`
   (29 layout pages, all AIT photography, logo and colours intact).
2. `build_from_template.py` keeps 15 of those pages, reorders them, and
   replaces the template's placeholder copy with the workshop content.
   Replacement strings are kept close to the original length so nothing
   overflows the boxes the template designer sized.
3. `make_figures.py` renders every image in the deck from the workshop's own
   artefacts — the real `data/fhir/P0001.json`, the real terminal output of
   `scripts/01_fhir_to_table.py`, the ROC curve and confusion matrix from the
   trained model, the K-Means projection. No stock photography.
4. `swap_figures.py` repoints the template's campus photographs at those
   figures, leaving the AIT logo and icons untouched.

To rebuild from scratch, re-export the Canva copy as `ait-template.pptx`, then:

```bash
uv run python slides/collect_results.py
python3 slides/build_from_template.py
uv run python slides/make_figures.py
python3 slides/swap_figures.py
```

If only the numbers changed and the template did not, skip all that and run
`collect_results.py` then `apply_results.py`.

## Two template pages were deliberately dropped

The template's donut chart (50/35/85%) and bar chart (JAN–SEP) are exported by
Canva as flat PNGs, not as editable charts. Their numbers cannot be corrected,
so they were excluded rather than shown next to real results.

## Pages written after the Canva export

The template export (`ait-template.pptx`) is not committed and Canva will not
reproduce it byte-for-byte, so five pages were built by copying a layout that
was already in the deck:

```bash
python3 slides/clone_page.py --page 13 --after 13   # ONE OBJECT
python3 slides/clone_page.py --page 3  --after 16   # TWO FLAGS
python3 slides/clone_page.py --page 11 --after 17   # ACCURACY ROSE
python3 slides/apply_results.py                     # fills the text
```

`ORDER` in `build_from_template.py` holds a string, not a page number, for each
of these. `apply_results.py` refreshes them like any other page;
`build_from_template.py` cannot rebuild them and says so.

Their figures come from `make_figures.py`, which writes into `slides/figures/`
(gitignored — the images are already inside the .pptx).
