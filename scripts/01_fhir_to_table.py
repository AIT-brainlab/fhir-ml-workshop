"""
STEP 1 - FROM FHIR TO A TABLE
This morning you learned what FHIR is. This is where it becomes code.

    uv run python scripts/01_fhir_to_table.py

Reads real FHIR R4 Bundles from data/fhir/ and turns them into the flat table
that every machine learning library expects. Nothing in scikit-learn can read
FHIR. Someone has to write this step, and in most health AI projects it is
where the majority of the work goes.

Break the feed on purpose and run it again. The Bundles on disk are never
modified — the damage is applied in memory as they are read:

    --drop area                 a hospital stops sending one Observation
    --rename radius:tumor_rad   a hospital renames a code
    --drop area --drop symmetry  two at once
"""

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FHIR_DIR = ROOT / "data" / "fhir"
CSV = ROOT / "data" / "patients.csv"

DX_CODE_MALIGNANT = "malignant"


def rule(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Flatten FHIR Bundles into a table.")
    p.add_argument("--drop", action="append", default=[], metavar="CODE",
                   help="drop this Observation code from every Bundle as it is read")
    p.add_argument("--rename", action="append", default=[], metavar="OLD:NEW",
                   help="rename an Observation code, as a hospital might")
    return p.parse_args()


def load_bundles() -> list[dict]:
    files = sorted(FHIR_DIR.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No bundles in {FHIR_DIR}")
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]


def damage(bundles: list[dict], drop: list[str], rename: list[str]) -> None:
    """Simulate a feed change, in memory only. The files on disk are untouched."""
    renames = dict(r.split(":", 1) for r in rename)

    for bundle in bundles:
        kept = []
        for entry in bundle.get("entry", []):
            res = entry.get("resource", {})
            if res.get("resourceType") == "Observation":
                coding = res["code"]["coding"][0]
                if coding["code"] in drop:
                    continue
                if coding["code"] in renames:
                    coding["code"] = renames[coding["code"]]
            kept.append(entry)
        bundle["entry"] = kept

    if drop:
        print(f"[--drop]   removed Observation(s): {', '.join(drop)}")
    for old, new in renames.items():
        print(f"[--rename] '{old}' now arrives as '{new}'")


def flatten(bundle: dict) -> dict:
    """Turn ONE Bundle into ONE row.

    A Bundle is a bag of Resources. We walk it once and pick out:
      Patient    -> the row's identity
      Observation-> one column each, named by its code
      Condition  -> the label we want to predict
    """
    row: dict = {}

    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        kind = resource.get("resourceType")

        if kind == "Patient":
            row["patient_id"] = resource["id"]

        elif kind == "Observation":
            # The column name comes from the coded concept, NOT from the
            # position in the file. This is the whole benefit of coded data.
            code = resource["code"]["coding"][0]["code"]
            row[code] = resource["valueQuantity"]["value"]

        elif kind == "Condition":
            dx = resource["code"]["coding"][0]["code"]
            row["malignant"] = int(dx == DX_CODE_MALIGNANT)

    return row


def main() -> None:
    args = parse_args()
    bundles = load_bundles()
    if args.drop or args.rename:
        damage(bundles, args.drop, args.rename)

    # ------------------------------------------------------- what arrived
    rule("1. WHAT A HOSPITAL ACTUALLY SENDS YOU")
    first = bundles[0]
    kinds = [e["resource"]["resourceType"] for e in first["entry"]]
    print(f"Bundles on disk : {len(bundles)}")
    print(f"First bundle    : {first['id']}  (type '{first['type']}')")
    print(f"Resources in it : {len(kinds)}")
    for kind in sorted(set(kinds)):
        print(f"    {kinds.count(kind):>2} x {kind}")

    print("\nOne patient is not one record. It is a bag of linked resources.")
    print("Here is a single Observation out of that bag:\n")
    sample_obs = next(
        e["resource"] for e in first["entry"] if e["resource"]["resourceType"] == "Observation"
    )
    print(json.dumps(sample_obs, indent=2))

    print("\nNotice:")
    print("  - 'code' says WHAT was measured, using a coded vocabulary")
    print("  - 'subject' points at the Patient resource - that is the join key")
    print("  - the number you want is buried at valueQuantity.value")
    print("  - no LOINC code: these are research measurements from an image,")
    print("    so they use a local CodeSystem. Real projects hit this constantly.")

    # ---------------------------------------------------------- flattening
    rule("2. FLATTEN IT")
    df = pd.DataFrame([flatten(b) for b in bundles])
    df = df.sort_values("patient_id").reset_index(drop=True)

    print(f"{len(bundles)} bundles -> {df.shape[0]} rows x {df.shape[1]} columns\n")
    print(df.head().to_string(index=False))
    print("\nThat is it. That is the whole trick: walk the Bundle, pull the")
    print("coded values out, one row per patient. scikit-learn can read this.")

    # ------------------------------------------------------- missing data
    rule("3. WHAT WENT WRONG (on purpose)")
    missing = df.isna().sum()
    gaps = missing[missing > 0]
    if gaps.empty:
        print("No gaps in this sample.")
    else:
        print("Columns with gaps:")
        print(gaps.to_string())
        for column in gaps.index:
            who = df.loc[df[column].isna(), "patient_id"].tolist()
            print(f"\n  '{column}' is missing for: {', '.join(who)}")
        print("\nThe Observation simply was not in the Bundle. Nothing errored,")
        print("nothing warned - you just silently got a NaN.")
        print("This is the normal condition of real health data. The imputer")
        print("in Step 3's pipeline is what deals with it.")

    # ------------------------------------------------- prove it is the same
    rule("4. PROOF: THIS IS THE SAME DATA YOU WILL TRAIN ON")
    csv = pd.read_csv(CSV)
    subset = csv[csv["patient_id"].isin(df["patient_id"])].reset_index(drop=True)
    shared = [c for c in df.columns if c in subset.columns]

    comparable = df[shared].dropna()
    aligned = subset.set_index("patient_id").loc[comparable["patient_id"]].reset_index()
    identical = comparable.reset_index(drop=True).round(5).equals(
        aligned[shared].reset_index(drop=True).round(5)
    )

    print(f"Patients compared : {len(comparable)} (rows with no gaps)")
    print(f"Columns compared  : {len(shared)}")
    print(f"Identical to patients.csv : {identical}")
    print("\nThat is the training table. Every Bundle on disk was written out")
    print("of data/patients.csv before the workshop, so flattening them lands")
    print("back exactly where they started - which is the only reason this")
    print("check is possible at all. Step 3 trains on this same table.")

    rule("DONE")
    print("In a real project this step would also handle:")
    print("  - paging through /Patient?_count=100 until the server runs out")
    print("  - the same patient appearing twice under two identifiers")
    print("  - one hospital sending mmol/L and another mg/dL")
    print("  - Observations you did not ask for and cannot map to a column")
    print("\nBreak it yourself and watch the column list change:")
    print("  uv run python scripts/01_fhir_to_table.py --drop area")
    print("  uv run python scripts/01_fhir_to_table.py --rename radius:tumor_rad")
    print("\nNext:  uv run python scripts/02_explore_data.py")


if __name__ == "__main__":
    main()
