# Morning Theory Session: Orientation & Intro to AI in Health Foundations

**Time:** 10:00 – 12:00 (120 minutes)  
**Location:** Library Studio Room  
**Deck Target:** `slides-morning/orientation-and-health-ai-foundations.pptx`  
**Audience:** 20 undergraduate engineering students (Information Technology, Agricultural Engineering, Mechanical Engineering).

---

## Target Audience & Pedagogical Strategy

Because the room consists of **20 undergraduate students from engineering disciplines (IT, Agriculture, Mechanical)** rather than healthcare practitioners, the morning session translates clinical informatics into **systems engineering, sensor networks, and data pipeline concepts**, anchored by **AIT's own research in Telehealth & Sensor Systems**:

1. **AIT Telehealth & Assistive Systems in Action:**
   - Ground theory in the **AIT Telehealth Monitoring and Assistive Systems for Elderly and Disabled People** project ([AIT Project Overview](https://ait.ac.th/project/telehealth-monitoring-and-assistive-systems-for-elderly-and-disabled-people/)).
   - Showcase the **Non-Invasive Blood Glucose POC App** ([GitHub: akraradets/BloodGlucose-App](https://github.com/akraradets/BloodGlucose-App)) built under Work Package 1 (WP1), using **Raman spectroscopy** to measure glucose without skin pricks.
2. **Observations as Sensor Telemetry:**
   - For Mechanical & Ag students, a clinical `Observation` (e.g., Raman spectral peaks, glucose concentration, cell morphometry, soil moisture, vibration telemetry) is simply a **calibrated measurement from a physical sensor/transducer** with units, reference ranges, and method codes.
3. **HL7 v2 as Legacy Industrial Serial Bus:**
   - HL7 v2 is directly comparable to legacy serial protocols (Modbus, NMEA 0183, CAN bus ASCII frames): delimiter-separated strings (`|`, `^`), fixed segment headers, brittle custom extensions, and point-to-point wiring.
4. **FHIR R4 as Modern Microservices & Web Standards:**
   - FHIR represents the transition to standard HTTP REST APIs, structured JSON payloads, and distributed microservices familiar to IT students.
5. **Informative Missingness through an Engineering Lens:**
   - In predictive maintenance (Mechanical) or precision farming (Ag), sensors aren't sampled uniformly at random; you perform an oil spectrography or soil nitrogen core test *when there is an anomaly or concern*. In healthcare, diagnostic tests follow the exact same logic.

---

## Session Overview & Objectives

The morning session lays the theoretical and architectural foundations for the workshop. It bridges the gap between how clinical healthcare data is created, communicated, and standardized in real hospital environments (HL7 v2, FHIR R4) and how modern machine learning pipelines ingest and evaluate health data.

By the end of this session, participants will be able to:
1. **Map the Hospital IT Ecosystem:** Understand how EHR/EMR, LIS, RIS/PACS generate clinical data across the patient journey as interconnected subsystems.
2. **Explore AIT Telehealth Case Studies:** Understand how edge sensor telemetry (e.g. Raman spectroscopy for glucose in `BloodGlucose-App`) integrates into clinical telehealth platforms.
3. **Contrast Digital Health Standards:** Explain why HL7 v2 was built, why point-to-point integration becomes unmaintainable ("Z-segment spaghetti"), and how HL7 FHIR solves this using RESTful APIs, JSON, and standard clinical terminologies (LOINC, SNOMED CT).
4. **Assess AI-Readiness in Clinical Data:** Identify real-world health data challenges including informative missingness, class imbalance, temporal shift, and label leakage.
5. **Understand the Impedance Mismatch:** Explain why ML algorithms cannot directly consume hierarchical FHIR resources and why flattening/preprocessing is where 80% of clinical AI work takes place.
6. **Be Prepared for the Afternoon Hands-on:** Verify their local environment (`uv sync`) before breaking for lunch in the Library Studio Room.

---

## 120-Minute Master Schedule

```
[10:00 - 10:20]  Module 1: Orientation & Foundations of AI in Health (20m)
                 (Including AIT Telehealth & Raman Glucose POC Case Study)
[10:20 - 10:45]  Module 2: Health Data Ecosystems & Clinical ICT (25m)
[10:45 - 11:20]  Module 3: Digital Health Standards: HL7 v2 to FHIR R4 (35m)
[11:20 - 11:45]  Module 4: AI-Readiness & The Data Mismatch (25m)
[11:45 - 12:00]  Module 5: The Bridge to Hands-on & Tech Checkpoint (15m)
```

---

## Slide-by-Slide Storyboard (`.pptx`)

The presentation deck consists of **25 slides** (matching the Canva master template 1-to-1), structured to maintain a crisp 4–5 minute pace per slide with built-in discussion points.

### Module 1: Orientation & Foundations of AI in Health (10:00 – 10:20)

#### Slide 1: Title Slide
- **Title:** Orientation & Intro to AI in Health Foundations
- **Subtitle:** Health Data Ecosystems, Digital Health Standards (HL7 v2, FHIR), and AI-Readiness
- **Visual:** AIT Brain Lab branding, workshop date/venue.
- **Key Talking Point:** Today is split into two halves: this morning we learn how health data lives in hospital systems; this afternoon we build and evaluate ML models on real FHIR data.

#### Slide 2: The Two Halves of Today
- **Title:** The Two Halves of Today: Foundations to Hands-On
- **Visual:** Two-column workflow diagram:
  - *Morning (10:00–12:00):* Clinical workflows → Hospital systems → HL7 v2 → FHIR R4 → AI-readiness.
  - *Afternoon (14:00–16:00):* FHIR Bundles → Feature Extraction → Pipeline (Impute + Scale) → Logistic Regression & Random Forest → Evaluation → FHIR Output.
- **Key Talking Point:** "In health AI, training the model is a library call. Extracting, understanding, and standardising the data is 80% of the job."

#### Slide 3: AIT Research in Action: Telehealth & Sensor Systems
- **Title:** AIT Research: Telehealth & Assistive Systems
- **Subtitle:** Four work packages bridging physical sensors to clinical cloud integration
- **Visual:** 4-stage subsystem card layout:
  - **01. WP1: Non-Invasive Glucose Sensing:** Optical Raman spectroscopy & POC App (`akraradets/BloodGlucose-App`)
  - **02. WP2: Fall & Activity Detection:** Computer vision and Wi-Fi channel state information (CSI) analysis
  - **03. WP3: Remote Haptic Therapy:** Force-feedback robotics for physical therapy and rehabilitation
  - **04. WP4: Cloud Telehealth Platform:** Secure clinical data integration, visualization, and clinician dashboard
- **Key Talking Point:** "At AIT, we build real medical cyber-physical systems. But once a Raman spectrometer calculates glucose, how does that number reach a doctor's EHR without getting lost? That is why digital health standards exist."

#### Slide 4: Why Health AI is Different
- **Title:** Why Health AI is Not Consumer Tech
- **Visual:** Comparison table: Consumer ML vs. Clinical ML (High stakes, asymmetric cost of error, regulatory oversight, privacy/HIPAA/GDPR).
- **Key Talking Point:** Missing a malignant tumour has a catastrophic cost compared to a false alarm. Standard metrics like accuracy can be actively deceptive.

#### Slide 5: Prediction vs. Clinical Decision Support
- **Title:** Prediction vs. Clinical Decision Support
- **Visual:** Human-in-the-loop diagram: Autonomous AI vs. Assistive AI.
- **Key Talking Point:** Clinical AI rarely replaces physicians; it triages, flags outliers, or stratifies risk to assist clinical decisions.

---

### Module 2: Health Data Ecosystems & Clinical ICT (10:20 – 10:45)

#### Slide 6: The Hospital IT Alphabet Soup
- **Title:** The Clinical Data Ecosystem
- **Visual:** Architectural map showing:
  - **HIS / EHR:** Hospital Information System / Electronic Health Record (core patient master)
  - **LIS:** Laboratory Information System (blood tests, pathology, biopsy)
  - **RIS / PACS:** Radiology Information System & Picture Archiving (X-Ray, CT, MRI)
  - **Billing & Admin:** Claims, ICD-10 coding.
- **Key Talking Point:** Clinical data is not stored in one clean relational database. It is scattered across dozens of specialised departmental engines.

#### Slide 7: The Patient Journey: Fragmented Reality
- **Title:** The Longitudinal Record vs. Departmental Silos
- **Visual:** Patient journey timeline (Admission → Triage → Lab Order → Lab Result → Pathology → Discharge).
- **Key Talking Point:** Each stop along the journey writes data in different formats, on different clocks, often with different patient identifiers.

#### Slide 8: The Interoperability Crisis
- **Title:** The Interoperability Dilemma
- **Visual:** Spaghetti integration diagram: $N$ systems requiring $N \times (N-1) / 2$ point-to-point custom interfaces.
- **Key Talking Point:** Hospital integrations historically relied on custom point-to-point code. Upgrading one system broke twelve others.

#### Slide 9: Syntactic vs. Semantic Interoperability
- **Title:** Syntactic vs. Semantic Interoperability
- **Visual:** Diagram comparing:
  - *Syntactic:* Both systems can read the bytes (e.g. valid JSON, XML, or delimited strings).
  - *Semantic:* Both systems agree on the clinical *meaning* (e.g., Code `21908-9` means mean radius of cell nuclei, measured in microns).
- **Key Talking Point:** Having a JSON file is not enough. Without standard clinical terminologies, computers cannot understand what the number represents.

#### Slide 10: Why Relational Databases Break Down
- **Title:** Why Traditional Relational Tables Fail in Healthcare
- **Visual:** A sparse, 1000-column SQL table with 99% NULLs vs. an event-driven clinical model.
- **Key Talking Point:** Patients have sparse, variable-length event histories. One patient has 3 lab tests; another has 500 across 10 hospital stays.

---

### Module 3: Digital Health Standards: HL7 v2 to FHIR (10:45 – 11:20)

#### Slide 11: The Workhorse: HL7 Version 2
- **Title:** HL7 Version 2: The Messaging Workhorse (1989–Present)
- **Visual:** Breakdown of an HL7 v2 message pipe-and-hat format (`MSH|...`, `PID|...`, `OBR|...`, `OBX|...`).
- **Key Talking Point:** HL7 v2 is event-driven messaging over MLLP/TCP. It still powers over 90% of internal hospital interfaces today.

#### Slide 12: Anatomy of an HL7 v2 Lab Message (`ORU^R01`)
- **Title:** Anatomy of an HL7 v2 Message
- **Visual:** Color-coded segments:
  - `MSH` (Message Header: sender, receiver, timestamp)
  - `PID` (Patient Identification: ID, DOB, Sex)
  - `OBR` (Observation Request: Order info)
  - `OBX` (Observation Result: Test name, value, units, abnormal flag)
- **Key Talking Point:** Delimiters: `|` separates fields, `^` separates components. Human-readable if you know the spec, but brittle.

#### Slide 13: Why HL7 v2 Broke at Scale: The "Z-Segment" Trap
- **Title:** Why HL7 v2 Needs Modernisation
- **Visual:** Diagram of two hospitals sending "identical" HL7 v2 messages with divergent custom fields and Z-segments (`ZBE`, `ZPD`).
- **Key Talking Point:** "When you've seen one HL7 v2 implementation... you've seen *one* HL7 v2 implementation." High integration maintenance overhead.

#### Slide 14: Enter HL7 FHIR (Fast Healthcare Interoperability Resources)
- **Title:** The Modern Standard: HL7 FHIR (R4)
- **Visual:** Web-native architecture: RESTful HTTP (GET, POST, PUT), JSON payloads, OAuth2/SMART on FHIR.
- **Key Talking Point:** Built for the internet era using the 80/20 rule: standardize the 80% of data elements common across healthcare; handle the remaining 20% through structured extensions.

#### Slide 15: Core FHIR Concepts: Resources & References
- **Title:** Building Blocks: Resources & References
- **Visual:** Entity-relationship diagram: `Patient` ← `Observation.subject`, `Condition.subject` → `Patient`.
- **Key Talking Point:** FHIR resources are modular clinical building blocks with unambiguous IDs and explicit URI references.

#### Slide 16: FHIR Bundles: Transporting Collections
- **Title:** FHIR Bundles: Bundling Clinical Encounters
- **Visual:** Anatomy of a FHIR `Bundle` (`type: "collection"`, `entry: [...]`).
- **Key Talking Point:** In the afternoon, `data/fhir/P0001.json` is a FHIR Bundle holding 1 `Patient`, 10 `Observation` resources, and 1 `Condition`.

#### Slide 17: Coded Vocabularies: The Semantic Glue
- **Title:** Clinical Terminologies: LOINC, SNOMED CT & ICD-10
- **Visual:** Three-column breakdown:
  - **LOINC:** What was measured or tested (e.g. lab tests, vital signs, radius/texture measurements).
  - **SNOMED CT:** Clinical findings, procedures, body structures (e.g. "Invasive ductal carcinoma").
  - **ICD-10:** Disease classification and billing categories.
- **Key Talking Point:** `Observation.code` maps to LOINC. That code becomes our dataframe column name in the afternoon.

---

### Module 4: AI-Readiness in Health Systems (11:20 – 11:45)

#### Slide 18: What Makes Health Data "AI-Ready"?
- **Title:** What is "AI-Readiness"?
- **Visual:** The 4 pillars: Completeness, Semantic Consistency, Temporal Fidelity, Provenance.
- **Key Talking Point:** Having terabytes of clinical data is useless if codes change midway or units aren't harmonised.

#### Slide 19: Realities of Clinical Data: Informative Missingness
- **Title:** Clinical Reality 1: Informative Missingness
- **Visual:** Chart comparing "Missing Completely at Random" (MCAR) vs. "Informative Missingness" in medicine.
- **Key Talking Point:** In healthcare, data is not missing at random. A troponin level is only measured if the doctor suspects a heart attack. The *absence* of a test is clinical information.

#### Slide 20: Realities of Clinical Data: Class Imbalance & Leakage
- **Title:** Clinical Reality 2: Class Imbalance & Label Leakage
- **Visual:** Majority class illustration (63% Benign baseline = 63% accuracy by doing nothing). Label leakage example (a biopsy order date after diagnosis).
- **Key Talking Point:** If 95% of screening mammograms are benign, an unweighted model predicting "benign" every time achieves 95% accuracy while killing patients.

#### Slide 21: The Fundamental Impedance Mismatch
- **Title:** The Data Mismatch: FHIR Events vs. ML Matrices
- **Visual:** Graphic transformation:
  - Left: Hierarchical, nested, event-based FHIR Bundle.
  - Middle: Transformation Script (`scripts/01_fhir_to_table.py`).
  - Right: Flat 2D NumPy/Pandas Matrix ($X \in \mathbb{R}^{N \times D}$, $y \in \{0, 1\}$).
- **Key Talking Point:** "Nothing in scikit-learn, XGBoost, or PyTorch can read a FHIR Bundle. The flattening step is where decisions on joins, missingness, and aggregation must be made."

#### Slide 22: Feature Engineering & Preprocessing Pipelines
- **Title:** Safe Preprocessing: Preventing Data Leakage
- **Visual:** Scikit-learn Pipeline schematic: `SimpleImputer` → `StandardScaler` → `Classifier`.
- **Key Talking Point:** Why imputers and scalers must be fit strictly on training splits, never across the whole cohort.

---

### Module 5: Bridge to the Afternoon & Hands-On Checkpoint (11:45 – 12:00)

#### Slide 23: The Afternoon Pipeline Preview
- **Title:** Afternoon Preview: The 5-Step Pipeline
- **Visual:** Workflow diagram corresponding to the workshop scripts:
  - `01_fhir_to_table.py` (Parse FHIR Bundles → `patients.csv`)
  - `02_explore_data.py` (Class balance, distributions, correlations)
  - `03_train_model.py` (Pipelines, Logistic Regression vs. Random Forest, ROC-AUC)
  - `04_cluster_patients.py` (Unsupervised K-Means clustering)
  - `app/` (Streamlit interactive UI + FastAPI serving + FHIR export)
- **Key Talking Point:** You will run all of this on your own laptops.

#### Slide 24: Closing the Loop: AI Results Back as FHIR
- **Title:** Closing the Loop: Outputting Predictions as FHIR
- **Visual:** Diagram of ML inference wrapped into a FHIR `RiskAssessment` and `Observation` resource.
- **Key Talking Point:** An AI model is useless if its predictions cannot flow back into the hospital's clinical workflow.

#### Slide 25: Pre-Lunch Tech Check & Instructions
- **Title:** Tech Check Before Lunch
- **Visual:** Step-by-step terminal checklist:
  - `cd fhir-ml-workshop`
  - `uv sync`
  - `uv run python -c "import sklearn; print(sklearn.__version__)"`
- **Key Talking Point:** "Run `uv sync` before you go to lunch. Do not rely on downloading 600MB when the room reconnects at 14:00."

---

## Concrete Technical Artifacts for the Slides

### 1. HL7 v2 vs. FHIR R4 Side-by-Side Comparison

#### HL7 v2 (`ORU^R01` Lab Result Segment)
```hl7
MSH|^~\&|LAB_SYS|HOSPITAL_A|EMR_SYS|HOSPITAL_A|20260909101500||ORU^R01|MSG000124|P|2.5
PID|1||P0001^^^MRN||DOE^JANE||19800512|F
OBR|1|ORD9812|LAB4401|21908-9^Cell Nuclei Measurements^LN|||20260909093000
OBX|1|NM|21908-9^Mean Radius^LN|1|17.99|um|6.0-20.0|N|||F
OBX|2|NM|99901-1^Mean Texture^LN|1|10.38|score||N|||F
```

#### HL7 FHIR R4 Equivalent (`Observation` Resource in JSON)
```json
{
  "resourceType": "Observation",
  "id": "obs-p0001-radius",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "21908-9",
        "display": "Mean radius of cell nuclei"
      }
    ]
  },
  "subject": {
    "reference": "Patient/P0001"
  },
  "valueQuantity": {
    "value": 17.99,
    "unit": "um",
    "system": "http://unitsofmeasure.org",
    "code": "um"
  }
}
```

### 2. AIT Case Study: Raman Spectroscopy Glucose Reading as a FHIR Resource

From **WP1 of the AIT Telehealth Project** and the `BloodGlucose-App` POC, a calibrated Raman spectroscopic glucose measurement is represented in standard FHIR R4:

```json
{
  "resourceType": "Observation",
  "id": "obs-glucose-raman-ait-001",
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "laboratory"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "2339-0",
        "display": "Glucose [Mass/volume] in Blood"
      }
    ]
  },
  "subject": {
    "reference": "Patient/P0001"
  },
  "effectiveDateTime": "2026-09-09T10:30:00+07:00",
  "valueQuantity": {
    "value": 118,
    "unit": "mg/dL",
    "system": "http://unitsofmeasure.org",
    "code": "mg/dL"
  },
  "method": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "439401001",
        "display": "Raman spectroscopy"
      }
    ]
  },
  "device": {
    "display": "AIT Non-Invasive Raman Sensor (WP1)"
  }
}
```

---

## Instructor Delivery Notes & Questions for the Room (Library Studio Room)

With 20 students in a studio room setting, keep discussions interactive and draw on their engineering backgrounds:

1. **At Slide 7 & 8 (Syntactic vs. Semantic Interoperability):**
   - *Prompt for IT students:* *"Who has integrated two web APIs where both return valid JSON, but one calls the field `user_id` and the other calls it `patient_ref` or `subject_id`? That's syntactic success with semantic failure. How does FHIR's canonical URI schema fix this?"*
2. **At Slide 10 & 11 (HL7 v2 Delimiters):**
   - *Prompt for IT & Mech students:* *"Who has parsed NMEA GPS sentences, Modbus packets, or CSV telemetry over a serial port? Notice how HL7 v2 (`MSH|^~\&|...`) is essentially an industrial ASCII packet format from 1989."*
3. **At Slide 12 (HL7 v2 Z-segments):**
   - *Teaching point:* *"HL7 v2 was so flexible that every hospital added custom Z-segments. That flexibility turned into an integration nightmare—like an industrial equipment vendor changing CAN bus IDs on every machine."*
4. **At Slide 18 (Informative Missingness):**
   - *Prompt for Ag & Mech students:* *"In predictive maintenance (vibration diagnostics) or precision agriculture (soil nitrogen testing), do you run expensive lab assays randomly, or only when a subsystem shows distress? If a patient doesn't have a biopsy result, does that mean they are healthy or un-tested?"*
5. **At Slide 20 (The Impedance Mismatch):**
   - *Visual bridge:* *"In robotics or IoT, you ingest streaming JSON sensor events, but to train an anomaly detection classifier in scikit-learn, what data structure do you need? A 2D feature matrix ($N \times D$). The morning lecture explains the events; the afternoon code does the matrix transformation."*
6. **At Slide 24 (Tech Check before Lunch):**
   - *Enforce the sync:* With 20 laptops in the Library Studio Room, verify that every student gets a clean output from `uv run python -c "import sklearn; print(sklearn.__version__)"`. Have two pre-loaded USB drives with `~/.cache/uv` ready for offline sync if the room wifi throttles.
