# Morning Theory Session: Orientation & Intro to AI in Health Foundations

**Time:** 10:00 – 12:00 (120 minutes)  
**Location:** Library Studio Room  
**Deck Target:** [`slides-morning/orientation-and-health-ai-foundations.pptx`](orientation-and-health-ai-foundations.pptx) (30 Slides, 16:9 Widescreen)  
**Audience:** 20 undergraduate engineering students (Information Technology, Agricultural Engineering, Mechanical Engineering).  
**Instructor Scratchpad:** [`slides-morning/HEALTH_STANDARDS_SCRATCHPAD.md`](HEALTH_STANDARDS_SCRATCHPAD.md) (Complete 2+1 Phase Narrative, History & Pedagogy)

---

## Pedagogical Strategy for Engineering Undergraduates

Because the room consists of **20 undergraduate students from engineering disciplines (IT, Agriculture, Mechanical)** rather than medical doctors, the morning session translates clinical informatics into **systems engineering, distributed networks, sensor telemetry, and data pipeline concepts**, anchored by **AIT's own research in Telehealth & Sensor Systems**:

1. **AIT Telehealth & Assistive Systems in Action:**
   - Ground theory in the **AIT Telehealth Monitoring and Assistive Systems for Elderly and Disabled People** project ([AIT Project Overview](https://ait.ac.th/project/telehealth-monitoring-and-assistive-systems-for-elderly-and-disabled-people/)).
   - Showcase the **Non-Invasive Blood Glucose POC App** ([GitHub: akraradets/BloodGlucose-App](https://github.com/akraradets/BloodGlucose-App)) built under Work Package 1 (WP1), using **optical Raman laser spectroscopy** to measure glucose without skin pricks.
2. **Observations as Sensor Telemetry:**
   - For Mechanical & Ag students, a clinical `Observation` (e.g., Raman spectral peaks, glucose concentration, cell morphometry, soil moisture, vibration telemetry) is simply a **calibrated measurement from a physical sensor/transducer** with units, reference ranges, and method codes.
3. **HL7 v2 as Legacy Industrial Serial Bus:**
   - HL7 v2 is directly comparable to legacy serial protocols (Modbus, NMEA 0183, CAN bus ASCII frames): delimiter-separated strings (`|`, `^`), fixed segment headers, brittle custom extensions, and point-to-point wiring over raw TCP sockets (MLLP).
4. **FHIR R4 as Modern Microservices & Web Standards:**
   - FHIR represents the transition to standard HTTP REST APIs, structured JSON payloads, and distributed microservices familiar to IT students.
5. **Informative Missingness through an Engineering Lens:**
   - In predictive maintenance (Mechanical) or precision farming (Ag), sensors aren't sampled uniformly at random; you perform an oil spectrography or soil nitrogen core test *when there is an anomaly or concern*. In healthcare, diagnostic tests follow the exact same logic.

---

## The "2 + 1" Master Schedule (120 Minutes)

```
[10:00 - 10:05]  Prologue: Orientation & The 2 + 1 Roadmap (5m)
[10:05 - 10:50]  Phase 1: History of Medical & Hospital IT Systems (45m)
                 (Pre-1960 Paper ──> 1960s Mainframe & MUMPS ──> 1970s Silos & ASTM ──> 
                  1980s Sockets & HL7 v2 ──> 2003 XML Flop ──> 2014+ FHIR REST APIs)
[10:50 - 11:35]  Phase 2: Evolution of Clinical Data Modalities for ML & AI (45m)
                 (1. Tabular ML ──> 2. Spatial/Imaging ──> 3. Time-Series Telemetry ──> 
                  4. Unstructured Text/LLMs ──> Token Bloat vs. Markdown ──> MCP & RAG)
[11:35 - 11:55]  Phase +1: AIT Research Spotlight — Telehealth & WP1 (20m)
                 (Dedicated Presentation for Prof. Chaklam Silpasuwanchai / AIT Brain Lab:
                  WP1 Optical Glucose Raman Sensor, BloodGlucose-App POC, FHIR R4 Mapping)
[11:55 - 12:00]  Epilogue: Bridge to Afternoon & Pre-Lunch Tech Check (5m)
```

---

## Slide-by-Slide Storyboard (`.pptx`)

The presentation deck consists of **30 clean slides** ([`slides-morning/orientation-and-health-ai-foundations.pptx`](orientation-and-health-ai-foundations.pptx)), 16:9 widescreen, custom card layouts, and official AIT brand palette.

### Prologue: Welcome & Architecture (10:00 – 10:05)

#### Slide 1: Cover Slide
- **Title:** Orientation & Intro to AI in Health Foundations
- **Subtitle:** Hospital IT History, Modern Standards (HL7 v2, FHIR R4), and Clinical AI Modalities
- **Visual:** AIT Brain Lab branding, date, venue, and audience metadata.

#### Slide 2: The 2 + 1 Session Architecture
- **Title:** The 2 + 1 Session Architecture
- **Visual:** 3-card roadmap:
  - *Phase 1 (45m):* History of Hospital IT (Pre-1960 to modern FHIR).
  - *Phase 2 (45m):* Evolution of AI Modalities (Tabular, Spatial, Time-Series, Text/LLMs).
  - *Phase +1 (20m):* AIT Research in Action (Telehealth & Raman Glucose POC for Dr. Chaklam).

---

### Phase 1: History of Medical & Hospital IT Systems (10:05 – 10:50)

#### Slide 3: Pre-1960: The Analog Era
- **Title:** Pre-1960: How Hospitals Kept Records Before Digital
- **Visual:** Card detailing basement paper record rooms, bed foot clipboards, pneumatic vacuum tube canisters, and lost medical memory.
- **Key Talking Point:** Physical records could not travel between clinics; two doctors treating the same patient had no way to see each other's notes in real time.

#### Slide 4: The 1960s: Mainframes & MUMPS
- **Title:** The 1960s: Mainframes, Magnetic Tapes & MUMPS
- **Visual:** 2 cards: IBM 360/370 mainframes and the "sneakernet" vs. 1966 MUMPS at Massachusetts General Hospital.
- **Key Talking Point:** MUMPS invented dynamic hierarchical sparse trees (`^PATIENT(id, 'LAB', 'GLU')`). Epic Systems still runs its core database engine on a MUMPS derivative today.

#### Slide 5: The 1970s: Departmental Silos & Early Standards
- **Title:** The 1970s: Departmental Silos & Early Standards
- **Visual:** 3 cards: DEC PDP-11 minicomputers, ASTM Committee E31 (invented pipe delimiters `|`), and UB-82 billing claim formats.
- **Key Talking Point:** ASTM E1238 invented the pipe and caret syntax that HL7 later adopted.

#### Slide 6: The 1980s: The Networking Crisis
- **Title:** The 1980s: Local Networks & The Integration Crisis
- **Visual:** 2 cards: The $N(N-1)/2$ point-to-point spaghetti trap (and ACR-NEMA 50-pin cable) vs. OSI Layers 1–4 (packets) vs. Layer 7 (clinical meaning).
- **Key Talking Point:** Ethernet solved moving packets; healthcare needed an agreement at Layer 7 (Application Layer) to understand what the data meant.

#### Slide 7: 1987–1989: The Birth of HL7
- **Title:** 1987–1989: The Birth of HL7 (Health Level Seven)
- **Visual:** 3 chronological milestones: March 1987 HUP committee, October 1987 HL7 v1.0 draft (84 pages), and 1989 HL7 v2.1 commercial explosion.
- **Key Talking Point:** Built to synchronize ADT (Admission, Discharge, Transfer) over raw TCP sockets using MLLP byte framing.

#### Slide 8: Anatomy of an HL7 v2 Message (`ORU^R01`)
- **Title:** Anatomy of an HL7 v2 Message (`ORU^R01`)
- **Visual:** Split panel: Segment structure explanations (`MSH`, `PID`, `OBR`, `OBX`) alongside real dark terminal code panel.

#### Slide 9: Technological Relativity: Why HL7 v2 in 1989
- **Title:** Technological Relativity: Why HL7 v2 in 1989
- **Visual:** 3 cards: The 1989 hardware context (no web, 1–4 MB RAM, 10 Mbps coax, $O(1)$ C streaming buffers) vs. 30 years of Z-segment integration debt.

#### Slide 10: 2003: The HL7 v3 Cautionary Tale
- **Title:** 2003: The Cautionary Tale of HL7 Version 3
- **Visual:** The dangers of over-engineering: The Reference Information Model (RIM), massive XML overhead, and the developer rebellion.
- **Key Talking Point:** Pragmatic, developer-friendly standards always defeat theoretically "pure" but unusable models.

#### Slide 11: 2014–Today: Enter HL7 FHIR (Built for the Web)
- **Title:** 2014–Today: Enter HL7 FHIR (Built for the Web)
- **Visual:** 3 cards: Web-native standards (HTTP REST, JSON, URLs), the 80/20 rule, and FHIR R4 Normative stability (2019).

#### Slide 12: Core FHIR Architecture: Resources & References
- **Title:** Core FHIR Architecture: Resources, References & Bundles
- **Visual:** 4 quadrants: `Patient` (demographics), `Observation` (vitals/labs), `Condition` (diagnoses), and `Bundle` (packaged collections).

#### Slide 13: Coded Vocabularies: The Semantic Glue
- **Title:** Coded Vocabularies: The Semantic Glue
- **Visual:** 3 cards: **LOINC** (lab measurements), **SNOMED CT** (clinical findings & procedures), and **ICD-10** (epidemiology & billing).

#### Slide 14: FHIR, The Semantic Web & KRR (Knowledge Representation)
- **Title:** FHIR, The Semantic Web & KRR (Knowledge Representation)
- **Visual:** 2 cards:
  - *The Semantic Web (W3C Linked Data):* Universal Resource Identifiers (URIs), RDF Triples (`Subject -> Predicate -> Object`), W3C RDF/Turtle standard (`fhir/rdf.html`), SPARQL graph querying.
  - *KRR (Knowledge Representation & Reasoning):* Description Logics (SNOMED CT $\mathcal{EL}^{++}$ profile of OWL 2), automated subsumption inference (inferring Bacterial Pneumonia $\sqsubseteq$ Respiratory Infection), pragmatic KRR vs. academic OWL.

#### Slide 15: Global Adoption Spectrum
- **Title:** Global Adoption: From Federal Law to Thailand
- **Visual:** 2 cards: Mandated by law (US Cures Act & EU EHDS) vs. Thailand MOPH HIE initiatives and legacy hospital hybrid reality.

---

### Phase 2: Evolution of Clinical Data Modalities for ML & AI (10:50 – 11:35)

#### Slide 16: Phase 2 Section Header: The Four Modalities of Health AI
- **Title:** The Four Modalities of Health AI
- **Visual:** Full-bleed Dark Green header: Different mathematics, different algorithms across tabular, spatial, telemetry, and text.

#### Slide 17: Modality 1: Tabular Data (Classical ML)
- **Title:** Tabular Data: The Classical Machine Learning Engine
- **Visual:** 2 cards: Data representation ($X \in \mathbb{R}^{n \times d}$, $y \in \{0, 1\}$) vs. Algorithms (Logistic Regression, Random Forest, XGBoost) and Afternoon Workshop Step 1/3 link.

#### Slide 18: Modality 2: Spatial & Imaging Data (Computer Vision)
- **Title:** Spatial & Imaging Data: Computer Vision in Medicine
- **Visual:** High-dimensional spatial tensors: DICOM standard, 2D/3D/4D tensors ($C \times D \times H \times W$), CNNs, Vision Transformers, and U-Net segmentation.

#### Slide 19: Modality 3: Time-Series & Continuous Telemetry
- **Title:** Time-Series & Telemetry: Continuous Physiological Streams
- **Visual:** Sequential temporal signals: ICU multi-parameter waveforms, 12-lead ECG, continuous glucose monitors, sliding windows, LSTMs, and Mamba state space models.

#### Slide 20: Modality 4: Unstructured Text ("What 90% Mean by AI")
- **Title:** Unstructured Text: What 90% of People Mean by 'AI'
- **Visual:** 2 cards: The unstructured majority (80% of health data in free-text notes) vs. The GenAI paradigm (Clinical LLMs, Med-PaLM, ambient AI scribing).

#### Slide 21: The Formatting Dilemma: Why LLMs Choke on Raw FHIR
- **Title:** The Formatting Dilemma: Why LLMs Choke on Raw FHIR
- **Visual:** 2 cards: The raw JSON trap (token bloat, 50k+ tokens per chart, diluted attention) vs. Clean Markdown tables (.md) reducing token consumption by 60–75%.

#### Slide 22: Clinical AI Agents: RAG & Model Context Protocol (MCP)
- **Title:** Clinical AI Agents: RAG & Model Context Protocol (MCP)
- **Visual:** 2 cards: Knowledge retrieval via clinical vector DBs (RAG) vs. Deterministic tool-calling via MCP (`get_patient_labs`).

#### Slide 23: The Fundamental Data Impedance Mismatch
- **Title:** The Fundamental Data Impedance Mismatch
- **Visual:** 2 contrast cards: Hierarchical FHIR event trees vs. 2D numerical feature matrices ($X \in \mathbb{R}^{n \times d}$). The core role of `scripts/01_fhir_to_table.py`.

#### Slide 24: Clinical Realities: Informative Missingness & Class Imbalance
- **Title:** Clinical Realities: Informative Missingness & Class Imbalance
- **Visual:** 2 warning cards: Tests ordered for sick patients (informative missingness) vs. The 63% accuracy trap (rare disease class imbalance).

#### Slide 25: Towards AI-Native Health Data Standards
- **Title:** Towards AI-Native Health Data Standards
- **Visual:** 2 architecture panels: The 3 Eras of Health Data vs. The Dual-Stack Solution (FHIR as System of Record + AI Vector/Feature Store as System of Intelligence).

---

### Phase +1: AIT Research in Action — Telehealth & WP1 (11:35 – 11:55)

#### Slide 26: Phase +1 Section Header: AIT Research in Action
- **Title:** Telehealth & Assistive Systems (Prof. Chaklam Silpasuwanchai)
- **Visual:** Full-bleed Dark Green header: Grounding theory in real AIT systems engineering.

#### Slide 27: The AIT Telehealth Project: Four Work Packages
- **Title:** AIT Telehealth Project: Four Work Packages
- **Visual:** 4 cards:
  - **WP1:** Non-Invasive Glucose (Raman spectroscopy & edge ML).
  - **WP2:** Activity & Fall Detection (Computer vision & Wi-Fi CSI).
  - **WP3:** Remote Haptic Therapy (Robotic rehabilitation force-feedback).
  - **WP4:** Cloud Telehealth Platform (Secure FHIR integration & dashboards).

#### Slide 28: WP1 Deep Dive: Non-Invasive Glucose via Raman Spectroscopy
- **Title:** WP1 Deep Dive: Non-Invasive Glucose via Raman Spectroscopy
- **Visual:** 2 cards: The optical sensor principle (785nm laser, molecular inelastic scattering) vs. The ML engine (Modality 3 → Modality 1 mapping, `BloodGlucose-App` POC).

#### Slide 29: Closing the Circuit: Mapping AIT Raman Readings into FHIR
- **Title:** Closing the Circuit: Mapping AIT Raman Readings into FHIR
- **Visual:** Split layout: Standards harmonization (LOINC `2339-0`, SNOMED CT `439401001`, UCUM `mg/dL`) alongside real FHIR JSON observation code panel.

---

### Epilogue & Transition to Afternoon (11:55 – 12:00)

#### Slide 30: Closing the Classical Loop & Tech Checkpoint
- **Title:** Closing the Classical Loop & Tech Checkpoint
- **Visual:** 3 cards: Closing the loop (Step 5c ML predictions back into FHIR `RiskAssessment`), Terminal navigation, and Pre-lunch `uv sync` verification.

---

## Concrete Technical Artifacts for the Slides

### 1. HL7 v2 (`ORU^R01` Lab Result Segment)
```hl7
MSH|^~\&|LAB_SYS|AIT_HOSP|EMR_SYS|AIT_HOSP|20260909101500||ORU^R01|MSG000124|P|2.5
PID|1||P0001^^^MRN||DOE^JANE||19800512|F
OBR|1|ORD9812|LAB4401|21908-9^Cell Nuclei Measurements^LN|||20260909093000
OBX|1|NM|21908-9^Mean Radius^LN|1|17.99|um|6.0-20.0|N|||F
OBX|2|NM|99901-1^Mean Texture^LN|1|10.38|score||N|||F
```

### 2. AIT Case Study: Raman Spectroscopy Glucose Reading in FHIR R4
```json
{
  "resourceType": "Observation",
  "id": "ait-raman-glucose-001",
  "status": "final",
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
        "display": "In-vivo Raman spectroscopy"
      }
    ]
  }
}
```
