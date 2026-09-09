# Morning Theory Session: Orientation & Intro to AI in Health Foundations

**Time:** 10:00 – 12:00 (120 minutes)  
**Location:** Library Studio Room  
**Deck Target:** `slides-morning/orientation-and-health-ai-foundations.pptx`  
**Audience:** 20 undergraduate engineering students (Information Technology, Agricultural Engineering, Mechanical Engineering).  
**Instructor Scratchpad:** [`slides-morning/HEALTH_STANDARDS_SCRATCHPAD.md`](HEALTH_STANDARDS_SCRATCHPAD.md) (HL7 & FHIR Deep-Dive, Adoption, & Pedagogy)

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
                 (Distributed Systems, The N(N-1)/2 Trap, Hospital Topology & Silos)
[10:45 - 11:20]  Module 3: Digital Health Standards: HL7 v2 to FHIR R4 (35m)
                 (OSI Layer 7, 1989 Context, RESTful Web Standards, Vocabularies & AIT Case Study)
[11:20 - 11:45]  Module 4: AI-Readiness, Classical ML & The GenAI Frontier (25m)
                 (Impedance Mismatch, Pipelines, LLMs, RAG, MCP & AI-Native Standards)
[11:45 - 12:00]  Module 5: The Bridge to Hands-on & Tech Checkpoint (15m)
```

---

## Slide-by-Slide Storyboard (`.pptx`)

The presentation deck consists of **27 slides** ([`slides-morning/orientation-and-health-ai-foundations.pptx`](orientation-and-health-ai-foundations.pptx)), structured to maintain a crisp 4–5 minute pace per slide with built-in engineering discussion points.

### Module 1: Orientation & Foundations of AI in Health (10:00 – 10:20)

#### Slide 1: Title Slide
- **Title:** Orientation & Intro to AI in Health Foundations
- **Subtitle:** Health Data Ecosystems, Digital Health Standards (HL7 v2, FHIR), and AI-Readiness
- **Visual:** AIT Brain Lab branding, workshop date/venue.
- **Key Talking Point:** Today is split into two halves: this morning we learn how health data lives in hospital systems; this afternoon we build and evaluate ML models on real FHIR data.

#### Slide 2: The Two Halves of Today
- **Title:** The Two Halves of Today: Foundations to Hands-On
- **Visual:** Two-column workflow diagram:
  - *Morning (10:00–12:00):* Clinical workflows → Hospital systems → HL7 v2 → FHIR R4 → AI-readiness & GenAI frontiers.
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
- **Title:** The Clinical Data Ecosystem: Four Core Subsystems
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

#### Slide 8: The Interoperability Crisis: The $N(N-1)/2$ Trap
- **Title:** The Healthcare Interoperability Crisis
- **Visual:** Spaghetti integration diagram: $N$ systems requiring $N \times (N-1) / 2$ point-to-point custom interfaces vs. Hub-and-Spoke.
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

#### Slide 11: OSI Layer 7 & The HL7 Mandate
- **Title:** OSI Layer 7 & The HL7 Mandate
- **Visual:** OSI 7-layer stack diagram emphasizing Layer 7 (Application Meaning) over Layers 1–4 (Packet Transport).
- **Key Talking Point:** TCP/IP solved moving bytes between computers. But what do those bytes *mean*? In 1987, HL7 was founded specifically to standardize Layer 7 for healthcare.

#### Slide 12: Anatomy of an HL7 v2 Lab Message (`ORU^R01`)
- **Title:** Anatomy of an HL7 v2 Message
- **Visual:** Color-coded segments:
  - `MSH` (Message Header: sender, receiver, timestamp)
  - `PID` (Patient Identification: ID, DOB, Sex)
  - `OBR` (Observation Request: Order info)
  - `OBX` (Observation Result: Test name, value, units, abnormal flag)
- **Key Talking Point:** Delimiters: `|` separates fields, `^` separates components. Streaming ASCII parsable in $O(1)$ memory buffers.

#### Slide 13: Technological Relativity: Why HL7 v2 in 1989
- **Title:** Technological Relativity: Why HL7 v2 in 1989
- **Visual:** Historical computing context (1989: No web, no JSON, 1–4 MB RAM, 10 Mbps coax) vs. Modern integration debt (Z-segments, no REST APIs).
- **Key Talking Point:** "HL7 v2 was an engineering triumph for 1989 hardware. But 30 years of loose optionality created massive integration debt."

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

#### Slide 18: AIT Case Study: Raman Spectroscopy in FHIR R4
- **Title:** AIT Case Study: Raman Glucose in FHIR R4
- **Visual:** Real FHIR JSON observation with LOINC `2339-0` (Glucose in Blood) and SNOMED CT `439401001` (Raman spectroscopy method).
- **Key Talking Point:** Demonstrates how edge hardware built at AIT integrates directly into global medical standards.

---

### Module 4: AI-Readiness, Classical ML & The GenAI Frontier (11:20 – 11:45)

#### Slide 19: The New Dilemma: Is FHIR R4 Actually "AI-Ready"?
- **Title:** The New Dilemma: Is FHIR R4 Actually "AI-Ready"?
- **Visual:** The 4 pillars of AI-Readiness: Completeness, Semantic Fidelity, Temporal Integrity, Provenance.
- **Key Talking Point:** FHIR was built for Online Transaction Processing (OLTP — fetching one patient chart). ML requires Online Analytical Processing (OLAP — scanning millions of patient records).

#### Slide 20: Realities of Clinical Data: Informative Missingness
- **Title:** Clinical Reality 1: Informative Missingness
- **Visual:** Chart comparing "Missing Completely at Random" (MCAR) vs. "Informative Missingness" in medicine.
- **Key Talking Point:** In healthcare, data is not missing at random. A troponin level is only measured if the doctor suspects a heart attack. The *absence* of a test is clinical information.

#### Slide 21: Realities of Clinical Data: Class Imbalance & Evaluation
- **Title:** Clinical Reality 2: Class Imbalance & Evaluation Pitfalls
- **Visual:** Majority class illustration (63% Benign baseline = 63% accuracy by doing nothing). ROC-AUC vs. Precision-Recall curves.
- **Key Talking Point:** If 95% of screening mammograms are benign, an unweighted model predicting "benign" every time achieves 95% accuracy while killing patients.

#### Slide 22: The Fundamental Impedance Mismatch
- **Title:** The Data Mismatch: FHIR Events vs. ML Matrices
- **Visual:** Graphic transformation:
  - Left: Hierarchical, nested, event-based FHIR Bundle.
  - Middle: Transformation Script (`scripts/01_fhir_to_table.py`).
  - Right: Flat 2D NumPy/Pandas Matrix ($X \in \mathbb{R}^{N \times D}$, $y \in \{0, 1\}$).
- **Key Talking Point:** "Nothing in scikit-learn, XGBoost, or PyTorch can read a FHIR Bundle. The flattening step is where decisions on joins, missingness, and aggregation must be made."

#### Slide 23: Feature Engineering & Preprocessing Pipelines
- **Title:** Safe Preprocessing: Preventing Data Leakage
- **Visual:** Scikit-learn Pipeline schematic: `SimpleImputer` → `StandardScaler` → `Classifier`.
- **Key Talking Point:** Why imputers and scalers must be fit strictly on training splits, never across the whole cohort.

#### Slide 24: Closing the Classical Loop: Outputting Predictions as FHIR
- **Title:** Closing the Loop: Outputting Predictions as FHIR
- **Visual:** Diagram of ML inference wrapped into a FHIR `RiskAssessment` and `Observation` resource.
- **Key Talking Point:** An AI model is useless if its predictions cannot flow back into the hospital's clinical workflow.

#### Slide 25: The GenAI Era: LLMs, Agents, RAG & Context Formats
- **Title:** LLMs, Clinical Agents & Context Formats
- **Visual:** 3-card layout:
  - *The Token Bloat Trap:* Raw FHIR JSON consumes 300–500 tokens per observation, burning 50k+ tokens on schema metadata.
  - *Emerging Context Formats:* Markdown tables (.md) reduce token overhead by 60–75%; Vector RAG indexes clinical narratives.
  - *Agentic Tool-Calling (MCP):* Model Context Protocol tools allow clinical copilots to query structured patient data on demand.
- **Key Talking Point:** Generative AI does not want 50,000 tokens of raw JSON; it wants token-efficient Markdown tables and scoped MCP tools.

#### Slide 26: The Next Frontier: Towards AI-Native Health Data Standards
- **Title:** Towards AI-Native Health Data Standards
- **Visual:** Two-column architecture comparison:
  - *The 3 Eras:* 1989 v2 (Sockets) → 2014 FHIR (REST) → 2026+ AI-Native (Vectors & MCP).
  - *The Dual-Stack Architecture:* FHIR as System of Record (legal, auditable) + AI Feature/Vector Store as System of Intelligence.
- **Key Talking Point:** Just as FHIR replaced v2 for the web era, healthcare is approaching an inflection point requiring an AI-native data layer.

---

### Module 5: Bridge to the Afternoon & Hands-On Checkpoint (11:45 – 12:00)

#### Slide 27: Pre-Lunch Tech Check & Instructions
- **Title:** Tech Check Before Lunch (Library Studio Room)
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
