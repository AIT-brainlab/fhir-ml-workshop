"""
Build the Morning Theory Session presentation deck for the AIT Workshop.

Venue: Library Studio Room
Audience: 20 undergraduate engineering students (IT, Agriculture, Mechanical)
Output: slides-morning/orientation-and-health-ai-foundations.pptx

Bases layouts on the existing AIT-branded Canva master deck (slides/from-fhir-to-a-table.pptx),
preserving all typography (Metropolis), palettes, backgrounds, icons, and logos while
populating the 24 planned morning theory slides.
"""

import copy
from pathlib import Path
from pptx import Presentation
from pptx.text.text import _Paragraph

R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL_ATTRS = (f"{R_NS}embed", f"{R_NS}link", f"{R_NS}id")
P_NS = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

HERE = Path(__file__).resolve().parent
SRC_DECK = HERE.parent / "slides" / "from-fhir-to-a-table.pptx"
DST_DECK = HERE / "orientation-and-health-ai-foundations.pptx"

# Template slide indices (0-based) from SRC_DECK to clone for each morning slide:
# Slide 1: Cover (0)
# Slide 2: Two cards comparison (12)
# Slide 3: Tradeoff / two error cards (16)
# Slide 4: One object / concept focus (14)
# Slide 5: Four subsystems across (3)
# Slide 6: Patient journey / steps (2)
# Slide 7: Interoperability problem statement (10)
# Slide 8: Syntactic vs Semantic two columns (1)
# Slide 9: Why relational tables break down (18)
# Slide 10: HL7 v2 section header (5)
# Slide 11: HL7 v2 message anatomy (7)
# Slide 12: Why HL7 v2 broke / Z-segments (9)
# Slide 13: Enter FHIR R4 section header (5)
# Slide 14: Four FHIR building blocks (17)
# Slide 15: FHIR Bundles / collections (14)
# Slide 16: Three coded vocabularies (24)
# Slide 17: Four pillars of AI readiness (3)
# Slide 18: Clinical reality: Informative missingness (11)
# Slide 19: Clinical reality: Class imbalance & leakage (18)
# Slide 20: Data impedance mismatch (1)
# Slide 21: Safe preprocessing pipelines (13)
# Slide 22: Afternoon 5-step roadmap (2)
# Slide 23: Closing the loop: predictions as FHIR (23)
# Slide 24: Tech check before lunch (24)

TEMPLATE_MAP = [
    0,   # 1. Cover
    12,  # 2. Two Halves of Today
    16,  # 3. Why Health AI is Not Consumer Tech
    14,  # 4. Prediction vs Clinical Decision Support
    3,   # 5. Clinical Data Ecosystem (4 subsystems)
    2,   # 6. Patient Journey
    10,  # 7. Interoperability Crisis
    1,   # 8. Syntactic vs Semantic
    18,  # 9. Why Relational Tables Break Down
    5,   # 10. HL7 v2 The Workhorse
    7,   # 11. Anatomy of HL7 v2 Message
    9,   # 12. The Z-Segment Trap
    5,   # 13. Enter HL7 FHIR R4
    17,  # 14. Core FHIR Building Blocks
    14,  # 15. FHIR Bundles
    24,  # 16. Coded Vocabularies
    3,   # 17. 4 Pillars of AI Readiness
    11,  # 18. Informative Missingness
    18,  # 19. Class Imbalance & Leakage
    1,   # 20. Impedance Mismatch
    13,  # 21. Safe Preprocessing Pipelines
    2,   # 22. Afternoon Roadmap
    23,  # 23. Closing the Loop: Predictions as FHIR
    24,  # 24. Tech Check Before Lunch
]

# Slide content definitions: shape_name -> text
SLIDE_TEXTS = [
    # 1. Cover
    {
        "TextBox 22": "ORIENTATION & INTRO TO\nAI IN HEALTH FOUNDATIONS",
    },
    # 2. Two Halves of Today
    {
        "TextBox 13": "THE TWO HALVES OF TODAY",
        "TextBox 15": "Morning (10:00 – 12:00)",
        "TextBox 18": "Foundations & Ecosystems",
        "TextBox 14": (
            "Clinical IT landscape, HL7 v2 legacy protocols, FHIR R4 modern web standards, "
            "standard clinical vocabularies (LOINC, SNOMED), and AI-readiness principles."
        ),
        "TextBox 16": "Afternoon (14:00 – 16:00)",
        "TextBox 19": "From FHIR to Model Hands-On",
        "TextBox 17": (
            "Parse real FHIR Bundles into flat tables, preprocess & impute missingness, "
            "train Logistic Regression & Random Forest, evaluate ROC/thresholds, and serve."
        ),
    },
    # 3. Why Health AI is Not Consumer Tech
    {
        "TextBox 5": "WHY HEALTH AI IS NOT CONSUMER TECH",
        "TextBox 15": "High Asymmetry",
        "TextBox 9": "Clinical Diagnostics",
        "TextBox 13": (
            "Missing a malignant tumour (False Negative) has catastrophic patient outcomes. "
            "A false alarm (False Positive) costs an extra ultrasound. Standard accuracy is deceptive."
        ),
        "TextBox 16": "Symmetric / Low Risk",
        "TextBox 10": "Consumer Tech & Ads",
        "TextBox 14": (
            "Recommending the wrong film, music track, or online advert carries near-zero penalty. "
            "Consumer metrics cannot be imported blindly into clinical practice."
        ),
    },
    # 4. Prediction vs Clinical Decision Support
    {
        "TextBox 2": "PREDICTION VS. DECISION SUPPORT",
        "TextBox 8": "Assistive AI in the Loop: Why models triage rather than decree",
        "TextBox 7": (
            "Clinical machine learning models rarely replace doctors. Instead, they act as Clinical "
            "Decision Support (CDS): stratifying risk scores, prioritizing urgent patient queues, "
            "and highlighting subtle anomalies.\n\n"
            "For engineering students: think of clinical AI as an advanced telemetry alert system on a "
            "complex mechanical or agricultural system, guiding human oversight."
        ),
    },
    # 5. Clinical Data Ecosystem (4 subsystems)
    {
        "TextBox 3": "THE CLINICAL DATA ECOSYSTEM",
        "TextBox 4": "Four core subsystems generating patient telemetry in modern hospital IT",
        "TextBox 18": "01. EHR / EMR",
        "TextBox 19": "Electronic Health Record: Central patient master, clinical notes, encounters, orders.",
        "TextBox 20": "02. LIS (Laboratory)",
        "TextBox 21": "Lab Information System: Blood panels, cytology, biopsies, physical tissue measurements.",
        "TextBox 22": "03. RIS & PACS",
        "TextBox 23": "Radiology Information System & PACS: X-Ray, CT, MRI scans and image archives.",
        "TextBox 24": "04. Billing & Admin",
        "TextBox 25": "Administrative claims, insurance billing, and ICD-10 diagnostic coding.",
    },
    # 6. Patient Journey
    {
        "TextBox 5": "Patient Journey",
        "TextBox 6": "FRAGMENTED EVENT STREAMS OVER TIME",
        "TextBox 7": (
            "1.  Admission & Triage: Demographics & baseline vital signs logged in EHR\n"
            "2.  Physician Encounter: Differential diagnoses and lab/imaging orders dispatched\n"
            "3.  Diagnostic Testing: LIS analyzes biopsy morphometry, PACS stores images\n"
            "4.  Pathologist Review: Morphological measurements recorded & confirmed\n"
            "5.  Treatment & Discharge: Therapeutics prescribed, diagnostic codes billed\n\n"
            "Data is captured across multiple independent clocks and separate databases."
        ),
    },
    # 7. Interoperability Crisis
    {
        "TextBox 4": "THE INTEROPERABILITY CRISIS",
        "TextBox 5": "Point-to-point integration hell: N systems require N(N-1)/2 custom interfaces",
        "TextBox 10": "DATA SILOS — Historically, hospital systems used proprietary databases with closed schemas and custom exports.",
        "TextBox 11": "BRITTLE WIRING — Upgrading a single hospital departmental system frequently breaks dozens of fragile custom interfaces.",
    },
    # 8. Syntactic vs Semantic
    {
        "TextBox 2": "TWO LEVELS OF COMMUNICATION",
        "TextBox 8": "Syntactic vs. Semantic Interoperability",
        "TextBox 7": (
            "Syntactic Interoperability:\n"
            "Both systems can parse the wire format (e.g., valid JSON, XML, or delimiter-separated strings). "
            "The bytes arrive and decode without syntax error.\n\n"
            "Semantic Interoperability:\n"
            "Both systems agree on the clinical meaning. Code '21908-9' in both systems means 'mean radius of cell nuclei, in microns'. "
            "Without semantic standards, ML models train on meaningless numbers."
        ),
    },
    # 9. Why Relational Tables Break Down
    {
        "TextBox 4": "WHY RELATIONAL TABLES BREAK DOWN",
        "TextBox 5": (
            "In engineering terms, patients are sparse, variable-length event streams. One patient has 3 vital signs over 1 day; "
            "another has 500 lab tests over 10 years across multiple clinics.\n\n"
            "A single relational SQL table would need thousands of columns, where 99% of cells are NULL. "
            "Healthcare data requires graph-linked, event-driven standards."
        ),
    },
    # 10. HL7 v2 The Workhorse
    {
        "TextBox 2": "Digital Health Standards",
        "TextBox 3": "HL7 VERSION 2: THE 1989 WORKHORSE",
        "TextBox 4": (
            "• Event-driven messaging standard created in 1989\n"
            "• Delimiter-based pipe-and-hat format (| and ^)\n"
            "• Transmitted over socket streams via TCP/MLLP\n"
            "• Still powers >90% of internal hospital interfaces worldwide today"
        ),
    },
    # 11. Anatomy of HL7 v2 Message
    {
        "TextBox 16": "HL7 v2 Message Anatomy",
        "TextBox 14": "ORU^R01",
        "TextBox 15": "MSH",
        "TextBox 17": "PID",
        "TextBox 18": "OBX",
        "TextBox 19": "Message Header: Sender, receiver, message type, timestamp",
        "TextBox 20": "Patient ID: Medical record number (MRN), DOB, sex",
        "TextBox 21": "Observation Result: Test code, numeric value, units, status",
        "TextBox 22": "Segments",
        "TextBox 23": "Pipe & Hat",
        "TextBox 24": "Delimited",
        "TextBox 25": "MSH|^~\\&|LAB|HOSP... PID|1||P0001... OBX|1|NM|21908-9^Radius|1|17.99|um",
    },
    # 12. The Z-Segment Trap
    {
        "TextBox 26": "WHY HL7 v2 BROKE AT SCALE",
        "TextBox 27": "'When you have seen one HL7 v2 implementation... you have seen ONE implementation.'",
        "TextBox 31": "Z-Segments",
        "TextBox 28": "Hospitals added non-standard custom fields (ZBE, ZPD), breaking compatibility with external systems.",
        "TextBox 32": "No Schema",
        "TextBox 29": "Loose optionality: fields could be omitted, reordered, or redefined without breaking the parser.",
        "TextBox 33": "No REST API",
        "TextBox 30": "Point-to-point socket connections requiring complex, expensive interface engines (Mirth, Cloverleaf).",
    },
    # 13. Enter HL7 FHIR R4
    {
        "TextBox 2": "Modern Interoperability",
        "TextBox 3": "ENTER HL7 FHIR (R4)",
        "TextBox 4": (
            "• Fast Healthcare Interoperability Resources (R4 Normative)\n"
            "• Built on modern web foundations: HTTP REST, JSON/XML, OAuth2 (SMART on FHIR)\n"
            "• The '80/20 Rule': Standardize the 80% common healthcare concepts; extend the rest\n"
            "• Modular, resource-based microservice architecture replacing legacy serial streams"
        ),
    },
    # 14. Core FHIR Building Blocks
    {
        "TextBox 3": "FOUR CORE FHIR BUILDING BLOCKS",
        "TextBox 4": "How clinical concepts are modeled in the modern health internet",
        "TextBox 18": "01. Resources",
        "TextBox 19": "Discrete clinical entities with standard schemas: Patient, Observation, Condition, DiagnosticReport.",
        "TextBox 20": "02. Logical IDs",
        "TextBox 21": "Every resource has an unambiguous URI address (e.g. Patient/P0001, Observation/obs-01).",
        "TextBox 22": "03. References",
        "TextBox 23": "Explicit typed pointers connecting resources (e.g. Observation.subject points to Patient/P0001).",
        "TextBox 24": "04. RESTful Operations",
        "TextBox 25": "Standard HTTP verbs: GET to search/query, POST to create, PUT to update, DELETE to retract.",
    },
    # 15. FHIR Bundles
    {
        "TextBox 2": "FHIR BUNDLES: PACKAGING RECORDS",
        "TextBox 8": "How multi-resource patient histories travel across the wire",
        "TextBox 7": (
            "A FHIR Bundle is a container holding multiple resources together—used for search results, "
            "batch operations, and complete longitudinal patient encounters.\n\n"
            "In this afternoon's workshop, every file in data/fhir/ (e.g., P0001.json) is a real FHIR R4 "
            "Bundle containing 1 Patient resource, 10 Observation resources (cell nucleus morphometry), "
            "and 1 Condition resource (the confirmed biopsy outcome)."
        ),
    },
    # 16. Coded Vocabularies
    {
        "TextBox 16": "THE SEMANTIC GLUE: CODED VOCABULARIES",
        "TextBox 18": "LOINC",
        "TextBox 17": "Logical Observation Identifiers Names & Codes: Standardizes what was measured (lab tests, vital signs, cell nucleus radius 21908-9).",
        "TextBox 20": "SNOMED CT",
        "TextBox 19": "Systematized Nomenclature of Medicine: Standardizes clinical findings, anatomy, and pathology diagnoses ('Invasive ductal carcinoma').",
        "TextBox 22": "ICD-10",
        "TextBox 21": "International Classification of Diseases: Standardizes epidemiology, morbidity reporting, and administrative billing.",
    },
    # 17. 4 Pillars of AI Readiness
    {
        "TextBox 3": "THE FOUR PILLARS OF AI-READINESS",
        "TextBox 4": "Having terabytes of clinical data does not mean it is fit for machine learning",
        "TextBox 18": "01. Completeness",
        "TextBox 19": "Are essential confounders, baseline parameters, and clinical context recorded?",
        "TextBox 20": "02. Semantic Fidelity",
        "TextBox 21": "Are measurement units harmonized and terminology codes unified across all clinics?",
        "TextBox 22": "03. Temporal Integrity",
        "TextBox 23": "Are event sequences preserved? (Feature observations MUST strictly precede diagnostic labels).",
        "TextBox 24": "04. Provenance",
        "TextBox 25": "Is the sampling mechanism understood, or does the dataset carry hidden hospital selection bias?",
    },
    # 18. Informative Missingness
    {
        "TextBox 4": "CLINICAL REALITY: INFORMATIVE MISSINGNESS",
        "TextBox 5": (
            "In consumer data or physical telemetry, missing values are often random dropouts.\n\n"
            "In healthcare, tests are ordered because a patient is symptomatic. A missing troponin test means the doctor had no reason to suspect heart damage. "
            "The fact that a test was NOT ordered is itself clinical signal.\n\n"
            "Imputing blindly with means or medians distorts the clinical context."
        ),
    },
    # 19. Class Imbalance & Leakage
    {
        "TextBox 4": "ACCURACY LIES IN CLINICAL MACHINE LEARNING",
        "TextBox 5": (
            "In our breast cancer cohort, 63% of tumors are benign. A trivial model predicting 'benign' every time achieves 63% accuracy—and misses every single cancer patient.\n\n"
            "Label leakage is equally lethal: including an 'oncology consultation' or a 'post-op chemotherapy drug' as an input feature will give your model 99% accuracy in training and 0% clinical utility in deployment."
        ),
    },
    # 20. Impedance Mismatch
    {
        "TextBox 2": "THE IMPEDANCE MISMATCH",
        "TextBox 8": "Hierarchical Events vs. Flat Numerical Matrices",
        "TextBox 7": (
            "Healthcare Storage (FHIR R4):\n"
            "Deeply nested JSON trees, variable-length event histories, asynchronous timestamps, and relational URI links.\n\n"
            "Machine Learning Frameworks (scikit-learn, PyTorch, XGBoost):\n"
            "Rigid 2D numerical matrices (X in R^{N x D}) and target vectors (y in {0, 1}).\n\n"
            "The FHIR-to-Table transformation (Step 1 this afternoon) is where 80% of health AI engineering happens."
        ),
    },
    # 21. Safe Preprocessing Pipelines
    {
        "TextBox 2": "SAFE PREPROCESSING PIPELINES",
        "TextBox 8": "Preventing data snooping: Impute, scale, and fit inside the fold",
        "TextBox 7": (
            "Never compute imputation medians or feature scaling means across the entire dataset before splitting!\n\n"
            "Doing so leaks information from the test set into the training set, producing falsely optimistic validation scores. "
            "We wrap our transformers and classifiers into a unified scikit-learn Pipeline so preprocessing parameters are learned strictly from training folds."
        ),
    },
    # 22. Afternoon Roadmap
    {
        "TextBox 5": "Afternoon Roadmap",
        "TextBox 6": "FROM FHIR TO MODEL (14:00 – 16:00)",
        "TextBox 7": (
            "1.  01_fhir_to_table.py — Extract 20 FHIR Bundles into flat rows\n"
            "2.  02_explore_data.py — Assess missingness, class balance, distributions\n"
            "3.  03_train_model.py — Fit Logistic Regression & Random Forest pipelines\n"
            "4.  04_cluster_patients.py — Discover natural patient clusters with K-Means\n"
            "5.  app/ — Interactive Streamlit diagnostic UI + FastAPI live serving\n\n"
            "All code is provided. You will run it, tweak flags, and audit the results."
        ),
    },
    # 23. Closing the Loop: Predictions as FHIR
    {
        "TextBox 2": "FULL CIRCLE: PREDICTIONS AS FHIR",
        "TextBox 8": "Step 5c · Exporting AI inference back to the clinical record",
        "TextBox 7": (
            "A machine learning prediction trapped in a Python notebook does not save lives.\n\n"
            "To be clinically actionable, the model's output must be serialized back into standard healthcare protocols. "
            "In Step 5, our application wraps predicted malignancy risks into valid FHIR RiskAssessment and Observation resources ready for EHR ingestion."
        ),
    },
    # 24. Tech Check Before Lunch
    {
        "TextBox 16": "TECH CHECK BEFORE LUNCH",
        "TextBox 18": "Step 1: Open Terminal",
        "TextBox 17": "cd fhir-ml-workshop\nEnsure you are in the repository root folder on your laptop in the Library Studio Room.",
        "TextBox 20": "Step 2: Sync uv Environment",
        "TextBox 19": "Run: uv sync\nDownloads and locks the 66 pinned dependencies (~580 MB) using uv.lock.",
        "TextBox 22": "Step 3: Verify Scikit-Learn",
        "TextBox 21": "Run: uv run python -c \"import sklearn; print(sklearn.__version__)\"\nIf this prints 1.6.1, your laptop is 100% ready for 14:00!",
    },
]


def clone_page(prs, index: int):
    """Append a copy of slide `index` (0-based) and return the new slide."""
    src = prs.slides[index]
    dst = prs.slides.add_slide(src.slide_layout)

    for shape in list(dst.shapes):  # the layout's placeholders
        shape._element.getparent().remove(shape._element)

    remap = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype.endswith("/slideLayout"):
            continue
        if rel.is_external:
            remap[rid] = dst.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        else:
            # same package, so the copy can point at the very same part
            remap[rid] = dst.part.relate_to(rel.target_part, rel.reltype)

    tree = dst.shapes._spTree
    for shape in src.shapes:
        el = copy.deepcopy(shape._element)
        for node in el.iter():
            for attr in REL_ATTRS:
                old = node.get(attr)
                if old in remap:
                    node.set(attr, remap[old])
        tree.append(el)

    bg = src._element.find(f"{P_NS}cSld/{P_NS}bg")
    if bg is not None:
        dst._element.find(f"{P_NS}cSld").insert(0, copy.deepcopy(bg))

    return dst


def set_text(shape, text: str) -> None:
    """Set text on shape, preserving the first run's font styling."""
    tf = shape.text_frame
    if not tf.paragraphs or not tf.paragraphs[0].runs:
        return
    p0 = tf.paragraphs[0]
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


def main():
    import shutil

    if not SRC_DECK.exists():
        raise SystemExit(f"Source template deck {SRC_DECK} does not exist.")

    print(f"Copying template deck {SRC_DECK} to {DST_DECK}...")
    shutil.copy(SRC_DECK, DST_DECK)
    prs = Presentation(DST_DECK)
    orig_count = len(prs.slides)
    print(f"Original template deck has {orig_count} slides.")

    # Build the 24 morning slides by cloning the respective template layouts
    print(f"Cloning and populating {len(TEMPLATE_MAP)} morning slides...")
    for idx, (tmpl_idx, text_map) in enumerate(zip(TEMPLATE_MAP, SLIDE_TEXTS), start=1):
        new_slide = clone_page(prs, tmpl_idx)

        # Apply texts
        by_name = {s.name: s for s in new_slide.shapes if s.has_text_frame}
        for name, text in text_map.items():
            if name in by_name:
                set_text(by_name[name], text)
            else:
                print(f"  [Warning] Shape '{name}' not found on slide {idx}")

        print(f"  Slide {idx:02d} built (from template slide {tmpl_idx + 1})")

    # Remove the original slides so only the 24 new morning slides remain
    print(f"Removing original {orig_count} template slides...")
    for _ in range(orig_count):
        sid = prs.slides._sldIdLst[0]
        prs.slides._sldIdLst.remove(sid)

    prs.save(DST_DECK)
    final_count = len(prs.slides)
    print(f"\nSuccessfully generated {final_count} slides in {DST_DECK}!")


if __name__ == "__main__":
    main()
