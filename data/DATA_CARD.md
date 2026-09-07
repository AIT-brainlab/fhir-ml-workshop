# Data card — `patients.csv`

## Source

**Breast Cancer Wisconsin (Diagnostic)** dataset, created by W. N. Street,
W. H. Wolberg and O. L. Mangasarian at the University of Wisconsin. It is
distributed inside scikit-learn (`sklearn.datasets.load_breast_cancer`), which
is why this workshop needs no internet connection.

`scripts/00_build_dataset.py` exported it to CSV. It keeps the ten **mean**
measurements, renames the columns to snake_case, adds a synthetic
`patient_id`, and flips the label so that `1 = malignant`.

> scikit-learn encodes `0 = malignant, 1 = benign`. We invert it because the
> positive class should be the condition you are trying to detect — otherwise
> "recall" measures the wrong thing.

## The FHIR Bundles in `data/fhir/`

The same script re-encodes 20 of these patients (10 malignant, 10 benign) as
FHIR R4 `collection` Bundles, so the afternoon can start where the morning
lecture ended. Each Bundle holds:

| Resource | Count | Carries |
|---|---|---|
| `Patient` | 1 | The identifier only — the source data has no demographics |
| `Observation` | 10 | One measurement each, `valueQuantity` + coded `code` |
| `Condition` | 1 | The biopsy result, `verificationStatus: confirmed` |

These Bundles are a **faithful re-encoding of the same numbers**, not a separate
data source. `scripts/01_fhir_to_table.py` flattens them and asserts the result
is identical to the matching rows of `patients.csv`.

Three deliberate choices worth knowing about:

- **No LOINC codes.** These are morphometry values derived from a digitised
  image, not standard lab tests, so no LOINC concept covers them. They sit under
  a local CodeSystem (`.../CodeSystem/fna-morphometry`). Inventing LOINC codes
  would have made the demo tidier and the lesson false.
- **No SNOMED CT on the diagnosis.** Same reasoning — the `Condition` uses a
  local code. Mapping local pathology vocabulary onto SNOMED is its own project.
- **`P0010` is missing its `texture` Observation on purpose**, so students watch
  a silent `NaN` appear during flattening. Real extracts always have gaps.

Pixel-based measurements carry a plain `unit` string with no UCUM `code`,
because UCUM has no pixel unit. Dimensionless ratios use UCUM `1` correctly.

## What one row is

One row is one fine-needle aspirate (FNA) of a breast mass. A digitised image of
the cell nuclei was measured, and the ten values below are the **mean** of that
measurement across the nuclei in the image.

| Column | Meaning | Unit |
|---|---|---|
| `patient_id` | Synthetic identifier, added for this workshop | — |
| `radius` | Mean distance from nucleus centre to perimeter | pixels |
| `texture` | Standard deviation of grey-scale values | — |
| `perimeter` | Nucleus perimeter | pixels |
| `area` | Nucleus area | pixels² |
| `smoothness` | Local variation in radius length | — |
| `compactness` | perimeter² / area − 1.0 | — |
| `concavity` | Severity of concave portions of the contour | — |
| `concave_points` | Number of concave portions of the contour | — |
| `symmetry` | Symmetry of the nucleus | — |
| `fractal_dimension` | "Coastline approximation" − 1.0 | — |
| `malignant` | **Target.** 1 = malignant, 0 = benign | — |

Two further features are computed in `common.py` at training and at prediction
time — `compactness_ratio` and `concavity_per_radius` — so that shape can be
judged independently of size.

## Size and balance

- 569 patients, no missing values
- 212 malignant (37.3%), 357 benign (62.7%)
- A model that always predicts "benign" scores **62.7% accuracy** and detects
  nothing. Use recall and ROC-AUC instead.

## AI-readiness assessment

| Question | Answer |
|---|---|
| Complete? | Yes — no missing values, which is itself unrealistic |
| Labelled? | Yes — diagnosis confirmed by biopsy |
| Balanced? | Moderately imbalanced (37 / 63) |
| Leakage risk? | Low — every feature is measured before diagnosis is known |
| Temporal alignment? | Single time point, no follow-up |
| Identifiable? | No — de-identified before public release |
| Representative? | **No.** See limitations |

## Limitations — read before believing any result

1. **One hospital, one decade.** Collected in Wisconsin, USA in the 1990s.
   Nothing guarantees it transfers to patients in the Philippines or Thailand,
   or to imaging equipment made in this century.
2. **No demographics.** Age, ethnicity and comorbidities are absent, so you
   cannot audit the model for bias across patient groups — the fairness check
   you would be required to run in practice is simply impossible here.
3. **Measurement depends on the operator.** The features come from a human
   choosing which nuclei to outline. A different technician produces different
   numbers for the same patient.
4. **The label is a biopsy result, not an outcome.** The model predicts what a
   pathologist recorded, including any errors the pathologist made.
5. **Too small and too clean.** 569 rows with zero missing values is a teaching
   dataset. Real EHR extracts arrive with missing columns, duplicated patients,
   and inconsistent units.

## Licence and use

Public research dataset, widely redistributed for education. This copy is used
here for teaching only. Nothing in this repository is a medical device or
clinically validated software.

## A note on the dates

Every `timestamp`, `effectiveDateTime` and `recordedDate` in `data/fhir/` is
**synthetic**. The source dataset carries no dates at all — only measurements
and a diagnosis — so a date had to be invented to produce a valid FHIR
resource. They are all set to a single fixed day chosen to sit in the era the
measurements come from.

The anachronism is deliberate and worth pointing out in class: FHIR did not
exist in the 1990s. What you are reading is old data re-encoded into a modern
standard, which is exactly what a hospital does when it migrates an archive.
