"""
Build a clean, high-quality, professional PowerPoint deck for the Morning Theory Session.

Venue: Library Studio Room
Audience: 20 undergraduate engineering students (IT, Agriculture, Mechanical)
Output: slides-morning/orientation-and-health-ai-foundations.pptx

Built from scratch with python-pptx using official AIT brand colors, typography,
and structured card-based layouts. 100% free of leftover afternoon figures or text.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

HERE = Path(__file__).resolve().parent
DST_DECK = HERE / "orientation-and-health-ai-foundations.pptx"
LOGO_PATH = HERE / "assets" / "ait_logo.png"

# Official AIT Brand Color Palette
DARK_GREEN  = RGBColor(0x1B, 0x3E, 0x24)   # #1B3E24 - Deep Forest Green
MED_GREEN   = RGBColor(0x28, 0x5C, 0x36)   # #285C36 - Mid Forest Green
LIME_GREEN  = RGBColor(0x94, 0xBA, 0x33)   # #94BA33 - AIT Lime Accent
BG_LIGHT    = RGBColor(0xF5, 0xF7, 0xF5)   # #F5F7F5 - Clean Off-White Background
CARD_BG     = RGBColor(0xFF, 0xFF, 0xFF)   # Pure White Card
CARD_BORDER = RGBColor(0xD2, 0xDC, 0xD4)   # Subtle Border
DARK_PANEL  = RGBColor(0x13, 0x1E, 0x16)   # #131E16 - Console Code Box
TEXT_DARK   = RGBColor(0x14, 0x21, 0x18)   # Charcoal / Near Black
TEXT_MUTED  = RGBColor(0x52, 0x64, 0x58)   # Slate Gray
TEXT_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)   # White
ALERT_RED   = RGBColor(0xC0, 0x39, 0x2B)   # Crimson Accent
CODE_GREEN  = RGBColor(0xA6, 0xE2, 0x2E)   # Monokai Green for code strings


def create_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_slide_background(slide, prs, dark=False):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_GREEN if dark else BG_LIGHT
    bg.line.fill.background()
    return bg


def add_header(slide, tag_text: str, title_text: str, subtitle_text: str = None, dark=False):
    # Top Category Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = LIME_GREEN if dark else MED_GREEN

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(9.8), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE if dark else DARK_GREEN

    # Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.38), Inches(10.0), Inches(0.4))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_text
        p_s.font.name = "Arial"
        p_s.font.size = Pt(12)
        p_s.font.color.rgb = LIME_GREEN if dark else TEXT_MUTED

    # Logo on top right
    if LOGO_PATH.exists():
        slide.shapes.add_picture(str(LOGO_PATH), Inches(11.1), Inches(0.45), width=Inches(1.5))


def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card


# -----------------------------------------------------------------------------
# SLIDE BUILDERS
# -----------------------------------------------------------------------------

def build_slide_01(prs):
    """Cover Slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs, dark=True)

    if LOGO_PATH.exists():
        slide.shapes.add_picture(str(LOGO_PATH), Inches(0.9), Inches(0.8), width=Inches(2.5))

    # Badge
    b = add_card(slide, Inches(0.9), Inches(2.2), Inches(5.8), Inches(0.45), bg_color=MED_GREEN, border_color=None)
    tf_b = b.text_frame
    tf_b.margin_left = Inches(0.2)
    p_b = tf_b.paragraphs[0]
    p_b.text = "AIT BRAIN LAB · MEDICAL ICT & HEALTH AI WORKSHOP"
    p_b.font.name = "Arial"
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = TEXT_WHITE

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.8), Inches(11.5), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Orientation & Intro to AI in Health Foundations"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(38)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    # Subtitle
    p_sub = tf_t.add_paragraph()
    p_sub.text = "Health Data Ecosystems, Digital Health Standards (HL7 v2, FHIR R4), and AI-Readiness"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = LIME_GREEN
    p_sub.space_before = Pt(12)

    # Info card at bottom
    info = add_card(slide, Inches(0.9), Inches(5.2), Inches(11.5), Inches(1.4), bg_color=MED_GREEN, border_color=None)
    tf_i = info.text_frame
    tf_i.margin_left = Inches(0.3)
    tf_i.margin_top = Inches(0.2)
    p1 = tf_i.paragraphs[0]
    p1.text = "Morning Theory Session: 10:00 – 12:00  |  Venue: Library Studio Room"
    p1.font.name = "Arial"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf_i.add_paragraph()
    p2.text = "Audience: 20 Undergraduate Engineering Students (IT, Agricultural Engineering, Mechanical Engineering)"
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.color.rgb = LIME_GREEN
    p2.space_before = Pt(6)


def build_slide_02(prs):
    """The Two Halves of Today (Two-Column)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Workshop Structure", "The Two Halves of Today: Foundations to Hands-On",
               "Why healthcare machine learning is 80% data curation and standardisation")

    # Left Column: Morning
    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)
    
    p = tf1.paragraphs[0]
    p.text = "MORNING (10:00 – 12:00)"
    p.font.name = "Arial"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = MED_GREEN
    
    p = tf1.add_paragraph()
    p.text = "Health Foundations & Standards"
    p.font.name = "Arial"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Clinical IT Landscape", "How hospitals generate patient telemetry (EHR, LIS, RIS/PACS)."),
        ("Legacy Standards (HL7 v2)", "Message-based pipe-and-hat protocols powering hospitals since 1989."),
        ("Modern Standard (FHIR R4)", "Web APIs, JSON payloads, resources, and coded vocabularies."),
        ("AI-Readiness", "Why machine learning cannot directly consume clinical event streams."),
        ("AIT Telehealth Case Study", "Connecting physical sensors (Raman glucose) to clinical standards.")
    ]
    for b_title, b_desc in bullets:
        p = tf1.add_paragraph()
        p.text = f"• {b_title}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    # Right Column: Afternoon
    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)
    
    p = tf2.paragraphs[0]
    p.text = "AFTERNOON (14:00 – 16:00)"
    p.font.name = "Arial"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = LIME_GREEN
    
    p = tf2.add_paragraph()
    p.text = "From FHIR to Model (Hands-On)"
    p.font.name = "Arial"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets_pm = [
        ("Step 1 · Flatten FHIR", "Read real FHIR Bundles into a tabular dataframe."),
        ("Step 2 · Data Profiling", "Analyse class imbalance, missingness, and diagnostic baselines."),
        ("Step 3 · Train Pipelines", "Fit Logistic Regression & Random Forest; sweep thresholds."),
        ("Step 4 · Unsupervised ML", "Discover natural patient clusters with K-Means."),
        ("Step 5 · Serve & FHIR Out", "Run interactive Streamlit UI, FastAPI service, and export predictions back to FHIR.")
    ]
    for b_title, b_desc in bullets_pm:
        p = tf2.add_paragraph()
        p.text = f"• {b_title}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_03(prs):
    """AIT Research in Action: Telehealth & Assistive Systems (4 Cards)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Research in Action", "AIT Telehealth & Assistive Systems Project",
               "Four work packages connecting physical sensors and robotics to clinical cloud infrastructure")

    wps = [
        ("WP1: Optical Glucose Sensing",
         "Non-Invasive Raman Sensor",
         "Measures blood glucose concentration without skin pricks using optical Raman laser spectroscopy.",
         "POC App: github.com/akraradets/BloodGlucose-App\nEdge ML calibration models.",
         LIME_GREEN),
        ("WP2: Activity & Fall Telemetry",
         "Computer Vision & Wi-Fi CSI",
         "Continuous indoor monitoring for elderly and disabled residents without intrusive wearable tags.",
         "Analyzes micro-Doppler Wi-Fi channel state information (CSI) & vision.",
         MED_GREEN),
        ("WP3: Remote Physical Therapy",
         "Robotic Haptic Rehab",
         "Bilateral force-feedback robotic exoskeleton for remote upper-limb stroke and mobility rehabilitation.",
         "Allows physical therapists to guide patients over internet links.",
         DARK_GREEN),
        ("WP4: Telehealth Cloud Platform",
         "Data Integration & FHIR",
         "Centralized healthcare platform aggregating multi-sensor event streams into standard medical formats.",
         "Real-time clinician dashboards, alert thresholds, and EHR integration.",
         MED_GREEN),
    ]

    card_w = Inches(2.7)
    card_h = Inches(4.7)
    for i, (wp_tag, wp_title, wp_body, wp_tech, tag_col) in enumerate(wps):
        left = Inches(0.8) + i * Inches(2.95)
        c = add_card(slide, left, Inches(2.0), card_w, card_h)
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = wp_tag.upper()
        p.font.name = "Arial"; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = tag_col

        p = tf.add_paragraph()
        p.text = wp_title
        p.font.name = "Arial"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = wp_body
        p.font.name = "Arial"; p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

        p = tf.add_paragraph()
        p.text = wp_tech
        p.font.name = "Arial"; p.font.size = Pt(9.5); p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(12)


def build_slide_04(prs):
    """Why Health AI is Not Consumer Tech"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Clinical AI Foundations", "Why Health AI is Not Consumer Tech",
               "Asymmetric error penalties: why conventional accuracy is dangerous in clinical decisions")

    # Left Card: Clinical Diagnostics
    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), border_color=ALERT_RED)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "HIGH ASYMMETRY / HIGH STAKES"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "Clinical Diagnostic ML"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items = [
        ("False Negative (Missed Cancer)", "A malignant tumor is classified benign. Patient is sent home. Tumor grows untreated for 12 months. Catastrophic outcome."),
        ("False Positive (False Alarm)", "A benign cyst is flagged malignant. Patient receives an extra ultrasound or biopsy. Anxiety and modest cost, but safe."),
        ("Metric Requirement", "Accuracy is meaningless here. We must optimize Recall (Sensitivity) and manage the threshold deliberately.")
    ]
    for h, desc in items:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    # Right Card: Consumer Tech
    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "SYMMETRIC / LOW STAKES"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_MUTED

    p = tf2.add_paragraph()
    p.text = "Consumer Recommenders & Ads"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items2 = [
        ("False Negative (Skipped Song)", "A user is not recommended a track they might have liked. Zero tangible harm; user picks another song."),
        ("False Positive (Irrelevant Ad)", "User sees an advert for running shoes they do not want. User scrolls past. Penalty is negligible."),
        ("Metric Requirement", "Click-through rate (CTR) and Top-K Precision are fine. Mistakes do not cause physical injury.")
    ]
    for h, desc in items2:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_05(prs):
    """Prediction vs. Clinical Decision Support"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Human-In-The-Loop", "Prediction vs. Clinical Decision Support (CDS)",
               "Why medical algorithms triage and assist rather than make autonomous clinical decrees")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE CLINICAL REALITY OF AI DEPLOYMENT"
    p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = MED_GREEN

    p = tf.add_paragraph()
    p.text = "AI Models Do Not Replace Doctors — They Triage Attention"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("Autonomous AI vs. Assistive AI", "In consumer autonomous driving, the car steers. In healthcare, regulatory bodies (FDA, EMA) treat diagnostic ML strictly as Software as a Medical Device (SaMD) operating as decision support with a licensed clinician in the loop."),
        ("Risk Stratification", "Instead of outputting a binary 'healthy vs sick', models assign calibrated risk probabilities. High-risk cases are bumped to the top of the radiologist's queue, reducing time-to-treatment for acute patients."),
        ("Engineering Analogy (Predictive Maintenance)", "For mechanical or agricultural engineering students: think of clinical AI as an anomaly detection telemetry system. The vibration sensor flags a bearing defect; the maintenance engineer decides when to shut down the turbine.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"{t}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(14)
        run = p.add_run()
        run.text = b
        run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_06(prs):
    """The Clinical Data Ecosystem (4 Subsystems)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Hospital IT Architecture", "The Clinical Data Ecosystem: Four Core Subsystems",
               "Patient data is generated across independent departments, databases, and vendor hardware")

    subsystems = [
        ("01. EHR / EMR", "Electronic Health Record",
         "The central patient master record: clinical encounter notes, problem lists, allergies, prescriptions, and vital signs.",
         "Vendor Examples: Epic, Cerner, Meditech"),
        ("02. LIS", "Laboratory Information",
         "Processes blood assays, pathology specimens, biopsies, and microbial cultures. Generates numeric test results and units.",
         "Biopsy morphometry data originates here"),
        ("03. RIS & PACS", "Radiology & Imaging",
         "Radiology Information System (orders/reports) and Picture Archiving System (DICOM image storage for CT, MRI, X-Ray).",
         "Stores multi-gigabyte imaging studies"),
        ("04. Billing & Admin", "Administrative & Claims",
         "Hospital enterprise resource planning: insurance billing, bed management, and standardized ICD-10 diagnostic billing codes.",
         "High data volume, financial governance")
    ]

    for i, (code, title, body, sub) in enumerate(subsystems):
        left = Inches(0.8) + i * Inches(2.95)
        c = add_card(slide, left, Inches(2.0), Inches(2.75), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = code
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9.5); p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(12)


def build_slide_07(prs):
    """The Patient Journey (5 Steps)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Clinical Workflow", "The Patient Journey: Fragmented Event Streams Over Time",
               "Data is recorded asynchronously across separate departmental clocks and software systems")

    steps = [
        ("01. Triage & Admission", "Demographics, admission vitals, presenting complaint logged in EHR."),
        ("02. Physician Orders", "Doctor examines patient; orders blood panel (LIS) and mammogram (RIS)."),
        ("03. Testing & Execution", "Lab analyzes fine needle aspirate (biopsy); radiologist captures scans."),
        ("04. Pathologist Review", "Cell nuclei morphometry measured and signed off as benign or malignant."),
        ("05. Discharge & Billing", "Treatment plan documented, medications dispensed, claim submitted.")
    ]

    for i, (title, desc) in enumerate(steps):
        left = Inches(0.8) + i * Inches(2.38)
        c = add_card(slide, left, Inches(2.0), Inches(2.2), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = f"STEP {i+1}"
        p.font.bold = True; p.font.size = Pt(10); p.font.color.rgb = LIME_GREEN

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)


def build_slide_08(prs):
    """The Interoperability Crisis"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "The Core Dilemma", "The Healthcare Interoperability Crisis",
               "Why hospital systems struggle to communicate without international data standards")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE POINT-TO-POINT TRAP"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "N(N-1)/2 Spaghetti Integration"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Proprietary Data Silos", "Historically, every medical software vendor stored data in bespoke schemas without standard APIs."),
        ("Custom Interfaces", "To connect an EHR to a Lab system, engineers wrote custom translation code. Connecting 10 systems required 45 custom bridges."),
        ("High Fragility", "Upgrading a single hospital subsystem frequently broke dozens of fragile custom interfaces, causing immense maintenance overhead.")
    ]
    for h, d in bullets:
        p = tf1.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "WHAT STANDARDS SOLVE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Hub-and-Spoke Universal Interoperability"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("The 'USB' of Healthcare", "Every system connects to one standard protocol (FHIR). Connecting N systems requires only N interfaces."),
        ("Clinical Continuity", "When a patient changes clinics, their allergy and medication history follows them without manual data reentry."),
        ("Democratizing Health AI", "Algorithms can plug directly into standard FHIR feeds instead of being re-engineered for every hospital database.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_09(prs):
    """Syntactic vs. Semantic Interoperability"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Core Informatics Concepts", "Syntactic vs. Semantic Interoperability",
               "Transporting raw bytes versus agreeing on clinical meaning")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "LEVEL 1 · THE WIRE FORMAT"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "Syntactic Interoperability"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items = [
        ("Definition", "Both systems can successfully parse the incoming data structure (e.g. valid JSON, XML, or delimiter-separated strings)."),
        ("The Guarantee", "The data packets arrive intact over TCP/IP and decode without syntax errors."),
        ("The IT Analogy", "Two web services exchange valid JSON with curly braces and key-value pairs."),
        ("The Limitation", "Syntactic success does NOT mean the receiving system understands what the fields mean!")
    ]
    for h, d in items:
        p = tf1.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "LEVEL 2 · THE CLINICAL MEANING"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Semantic Interoperability"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items2 = [
        ("Definition", "Both systems unambiguously agree on the medical meaning of the numbers and codes."),
        ("Standard Vocabularies", "Code '21908-9' in LOINC means 'mean cell nucleus radius, measured in microns' across all clinics worldwide."),
        ("The Health AI Barrier", "If Hospital A calls glucose 'GLU' and Hospital B calls it 'Blood_Sugar_mg', ML models fail. Semantic harmonization is mandatory.")
    ]
    for h, d in items2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_10(prs):
    """Why Relational Tables Fail at Scale"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Data Modeling", "Why Traditional Relational Tables Fail in Healthcare",
               "Sparse, variable-length event histories cannot fit into static SQL tables")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE DATABASE IMPASSE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf.add_paragraph()
    p.text = "Healthcare Data is an Event Graph, Not a Flat Spreadsheet"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("Extreme Sparsity", "A healthy 20-year-old has 2 medical encounters and 3 lab tests in 5 years. A chronic diabetes patient has 400 lab tests, 50 prescriptions, and 30 specialist consultations. A static SQL table would need thousands of columns, 99% of which are NULL."),
        ("Variable-Length Event Streams", "Every lab test, imaging exam, or medication change is an asynchronous event with its own timestamp, performing clinician, and calibrated instrument."),
        ("Graph-Linked Architecture", "Modern health data standards (FHIR) model healthcare as a graph of resources linked by explicit references (Observation points to Patient; Condition points to DiagnosticReport).")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"{t}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(14)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_11(prs):
    """Module 3 Header: Digital Health Standards"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs, dark=True)

    b = add_card(slide, Inches(0.9), Inches(1.8), Inches(4.5), Inches(0.45), bg_color=MED_GREEN, border_color=None)
    tf_b = b.text_frame
    tf_b.margin_left = Inches(0.2)
    p_b = tf_b.paragraphs[0]
    p_b.text = "MODULE 3 · DIGITAL HEALTH STANDARDS"
    p_b.font.bold = True; p_b.font.size = Pt(10); p_b.font.color.rgb = TEXT_WHITE

    t_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.5), Inches(11.5), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "From HL7 v2 to FHIR R4"
    p_t.font.bold = True; p_t.font.size = Pt(38); p_t.font.color.rgb = TEXT_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "How 35 years of medical IT evolved from 1989 serial delimiters to modern RESTful web APIs"
    p_sub.font.size = Pt(17); p_sub.font.color.rgb = LIME_GREEN
    p_sub.space_before = Pt(12)

    c = add_card(slide, Inches(0.9), Inches(5.0), Inches(11.5), Inches(1.6), bg_color=MED_GREEN, border_color=None)
    tf_c = c.text_frame
    tf_c.margin_left = Inches(0.3); tf_c.margin_top = Inches(0.2)
    p1 = tf_c.paragraphs[0]
    p1.text = "The Key Shift in One Sentence:"
    p1.font.bold = True; p1.font.size = Pt(13); p1.font.color.rgb = LIME_GREEN

    p2 = tf_c.add_paragraph()
    p2.text = "In HL7 v2, you find a value by counting pipe delimiters in a line. In FHIR, you query a standardized URI endpoint and parse standard JSON."
    p2.font.bold = True; p2.font.size = Pt(14); p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)


def build_slide_12(prs):
    """Anatomy of an HL7 v2 Message (Code Panel)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Digital Health Standards", "Anatomy of an HL7 v2 Message",
               "The pipe-and-hat (| and ^) ASCII format powering hospital messaging since 1989")

    # Left: Explanation
    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(4.8), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "MESSAGE STRUCTURE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    segments = [
        ("MSH (Message Header)", "Carries sending application, facility, message type (ORU^R01 lab result), and timestamp."),
        ("PID (Patient Identification)", "Carries patient identifier (MRN), patient name, date of birth, and biological sex."),
        ("OBR (Observation Request)", "Identifies the lab order, ordering physician, and specimen accession number."),
        ("OBX (Observation Result)", "The actual test result: LOINC code, numeric measurement, units (um), and normal flag.")
    ]
    for name, desc in segments:
        p = tf1.add_paragraph()
        p.text = f"{name}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(8)
        run = p.add_run(); run.text = desc; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    # Right: Dark Code Box
    c2 = add_card(slide, Inches(5.9), Inches(2.0), Inches(6.6), Inches(4.8), bg_color=DARK_PANEL, border_color=None)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "// Real HL7 v2.5 ORU^R01 (Lab Result Transmission)"
    p.font.name = "Courier New"; p.font.size = Pt(10.5); p.font.color.rgb = LIME_GREEN

    code_lines = [
        "MSH|^~\\&|LIS_SYS|AIT_HOSP|EMR_SYS|AIT_HOSP|20260909101500||ORU^R01|MSG000124|P|2.5",
        "PID|1||P0001^^^MRN||DOE^JANE||19800512|F",
        "OBR|1|ORD9812|LAB4401|21908-9^Cell Nuclei Biopsy^LN|||20260909093000",
        "OBX|1|NM|21908-9^Mean Radius^LN|1|17.99|um|6.0-20.0|N|||F",
        "OBX|2|NM|99901-1^Mean Texture^LN|1|10.38|score||N|||F",
        "OBX|3|NM|99901-2^Mean Perimeter^LN|1|122.8|um||N|||F"
    ]
    for line in code_lines:
        p = tf2.add_paragraph()
        p.text = line
        p.font.name = "Courier New"; p.font.size = Pt(9.5); p.font.color.rgb = CODE_GREEN
        p.space_before = Pt(8)


def build_slide_13(prs):
    """Why HL7 v2 Broke at Scale (3 Cards)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Standards Evolution", "Why HL7 v2 Broke at Scale: The Integration Debt",
               "\"When you've seen one HL7 v2 implementation... you've seen ONE implementation.\"")

    flaws = [
        ("The 'Z-Segment' Trap", "Non-Standard Custom Extensions",
         "HL7 v2 was so loosely specified that vendors added proprietary custom segments (ZBE, ZPD, ZAL). A message from Hospital A could not be parsed by Hospital B without bespoke translation code.",
         ALERT_RED),
        ("Optionality Chaos", "No Enforceable Schema",
         "Nearly every field in HL7 v2 was optional. Fields could be omitted or swapped without violating the specification. Parsers broke unpredictably on minor hospital software updates.",
         MED_GREEN),
        ("No Standard Web API", "Point-to-Point Socket Piping",
         "HL7 v2 runs over MLLP (raw TCP sockets). There are no URLs, no HTTP status codes, no authentication standards, and no query capabilities. Required costly interface engines (Mirth, Cloverleaf).",
         DARK_GREEN)
    ]

    for i, (title, sub, body, col) in enumerate(flaws):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


def build_slide_14(prs):
    """Enter HL7 FHIR R4"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Modern Interoperability", "Enter HL7 FHIR (Fast Healthcare Interoperability Resources)",
               "Reinventing healthcare communication using the open foundations of the modern internet")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE MODERN HEALTH DATA STANDARD (FHIR R4 NORMATIVE)"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf.add_paragraph()
    p.text = "Standard Web Architecture for Clinical Computing"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    pillars = [
        ("Web-Native Technologies", "Built on HTTP REST verbs (GET, POST, PUT, DELETE), JSON and XML representations, and OAuth2 security (SMART on FHIR). Any software engineer can build against it immediately."),
        ("The '80/20' Rule", "Instead of attempting to model every rare edge-case in medical history, FHIR standardizes the 80% of data concepts common across all healthcare. The remaining 20% is handled through structured, schema-validated Extensions."),
        ("Normative Stability (R4)", "Published in 2019, the core clinical resources (Patient, Observation, Condition) are normative—meaning future FHIR versions will never break backwards compatibility.")
    ]
    for h, b in pillars:
        p = tf.add_paragraph()
        p.text = f"{h}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_15(prs):
    """Four Core FHIR Building Blocks (4 Cards)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "FHIR Architecture", "Four Core FHIR Building Blocks",
               "How clinical concepts are modularized, addressed, and queried in modern health ICT")

    blocks = [
        ("01. Resources", "Modular Clinical Entities",
         "Standardized data schemas for medical concepts: Patient, Observation (tests/vitals), Condition (diagnoses), DiagnosticReport, Medication.",
         MED_GREEN),
        ("02. Logical IDs", "Unambiguous URI Addressing",
         "Every resource has a unique logical identity within the server (e.g., Patient/P0001 or Observation/obs-cell-radius-01).",
         LIME_GREEN),
        ("03. References", "Explicit Typed Pointers",
         "Resources link to each other via explicit reference fields: Observation.subject points to Patient/P0001; Condition.encounter points to Encounter/E102.",
         DARK_GREEN),
        ("04. REST Operations", "Standard HTTP Verbs",
         "Query with GET /Observation?subject=Patient/P0001; create with POST /Observation; update with PUT. Uses standard HTTP 200/404 response codes.",
         MED_GREEN)
    ]

    for i, (code, title, desc, col) in enumerate(blocks):
        left = Inches(0.8) + i * Inches(2.95)
        c = add_card(slide, left, Inches(2.0), Inches(2.75), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = code
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)


def build_slide_16(prs):
    """FHIR Bundles: Packaging Records"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Data Structures", "FHIR Bundles: Packaging Clinical Encounters",
               "How multi-resource patient histories travel together across network boundaries")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE ENVELOPE FOR HEALTHCARE DATA"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf.add_paragraph()
    p.text = "Bundles Package Collections of Resources into One Document"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("Bundle Types", "FHIR Bundles serve multiple purposes: 'searchset' returns query results, 'transaction' guarantees all-or-nothing database commits, and 'collection' transports static clinical records."),
        ("Anatomy of an Afternoon Bundle", "In this afternoon's workshop, every file in data/fhir/ (e.g., P0001.json) is a real FHIR R4 collection Bundle. Each bundle carries: 1 Patient resource, 10 Observation resources (cell nucleus morphometry), and 1 Condition resource (the ground-truth biopsy outcome)."),
        ("The Joining Job", "The afternoon script (scripts/01_fhir_to_table.py) walks each Bundle, matches Observation.subject to the Patient ID, extracts the numeric value, and produces a single row per patient.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"{t}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_17(prs):
    """Coded Vocabularies: The Semantic Glue (3 Cards)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Medical Terminologies", "The Semantic Glue: Standard Coded Vocabularies",
               "Without standard terminologies, computers cannot understand what measurements represent")

    vocabs = [
        ("LOINC", "What Was Measured or Tested",
         "Logical Observation Identifiers Names and Codes. Standardizes laboratory assays, clinical observations, and vital signs.\n\nExample: Code 21908-9 specifies 'Mean radius of cell nuclei'. In Step 1, this LOINC code becomes our dataframe column name!"),
        ("SNOMED CT", "Clinical Findings & Anatomy",
         "Systematized Nomenclature of Medicine. Comprehensive clinical terminology covering diseases, symptoms, anatomical sites, and surgical procedures.\n\nExample: Code 439401001 specifies 'Raman spectroscopy' as a diagnostic testing method."),
        ("ICD-10", "Epidemiology & Hospital Billing",
         "International Classification of Diseases (WHO). Standardizes disease classification, mortality reporting, and insurance claims.\n\nExample: Code C50.9 denotes 'Malignant neoplasm of breast, unspecified'." )
    ]

    for i, (title, sub, body) in enumerate(vocabs):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


def build_slide_18(prs):
    """AIT Case Study: Raman Glucose in FHIR (Code Panel)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "AIT Case Study", "Connecting Sensor Telemetry to FHIR: Raman Glucose",
               "How a reading from the AIT BloodGlucose-App POC is serialized into a standard FHIR Observation")

    # Left: Explanation
    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(4.8), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "THE SENSOR-TO-STANDARD BRIDGE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf1.add_paragraph()
    p.text = "From Laser Optics to Standard JSON"
    p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(4)

    steps = [
        ("1. Optical Sensing", "Raman spectrometer captures molecular vibrational scattering from human tissue."),
        ("2. Edge ML Calibration", "BloodGlucose-App algorithms estimate blood glucose concentration (118 mg/dL)."),
        ("3. Standard LOINC Code", "LOINC 2339-0 unambiguously identifies the measurement as 'Glucose in Blood'."),
        ("4. Method Metadata", "SNOMED CT 439401001 documents that the non-invasive method was Raman spectroscopy.")
    ]
    for h, d in steps:
        p = tf1.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    # Right: FHIR Observation JSON in Dark Box
    c2 = add_card(slide, Inches(5.9), Inches(2.0), Inches(6.6), Inches(4.8), bg_color=DARK_PANEL, border_color=None)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.25)

    p = tf2.paragraphs[0]
    p.text = "// Standard FHIR R4 Observation Resource"
    p.font.name = "Courier New"; p.font.size = Pt(10); p.font.color.rgb = LIME_GREEN

    json_lines = [
        '{\n  "resourceType": "Observation",\n  "id": "obs-glucose-raman-ait-001",\n  "status": "final",',
        '  "code": {\n    "coding": [{\n      "system": "http://loinc.org",\n      "code": "2339-0",\n      "display": "Glucose in Blood"\n    }]\n  },',
        '  "subject": { "reference": "Patient/P0001" },\n  "effectiveDateTime": "2026-09-09T10:30:00+07:00",',
        '  "valueQuantity": {\n    "value": 118,\n    "unit": "mg/dL",\n    "system": "http://unitsofmeasure.org",\n    "code": "mg/dL"\n  },',
        '  "method": {\n    "coding": [{\n      "system": "http://snomed.info/sct",\n      "code": "439401001",\n      "display": "Raman spectroscopy"\n    }]\n  }\n}'
    ]
    for snippet in json_lines:
        p = tf2.add_paragraph()
        p.text = snippet
        p.font.name = "Courier New"; p.font.size = Pt(9); p.font.color.rgb = CODE_GREEN
        p.space_before = Pt(4)


def build_slide_19(prs):
    """The Four Pillars of AI-Readiness (4 Cards)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Health AI Readiness", "The Four Pillars of AI-Readiness in Clinical Data",
               "Having gigabytes of healthcare records does not make them fit for machine learning")

    pillars = [
        ("01. Completeness", "Presence of Critical Confounders",
         "Are essential clinical confounders (patient age, biological sex, comorbidities) recorded alongside the lab measurements?",
         MED_GREEN),
        ("02. Semantic Fidelity", "Harmonized Units & Coding",
         "Are measurement units identical across all clinical sites? Did one clinic report in mg/dL while another reported in mmol/L?",
         LIME_GREEN),
        ("03. Temporal Integrity", "Strict Time-Sequence Ordering",
         "Do feature observations strictly precede the diagnostic outcome? (Including post-diagnosis drugs leaks future labels).",
         ALERT_RED),
        ("04. Provenance", "Understanding Selection Bias",
         "How was the patient cohort selected? Does the dataset represent the community, or only severe tertiary-care referrals?",
         DARK_GREEN)
    ]

    for i, (code, title, desc, col) in enumerate(pillars):
        left = Inches(0.8) + i * Inches(2.95)
        c = add_card(slide, left, Inches(2.0), Inches(2.75), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = code
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)


def build_slide_20(prs):
    """Clinical Realities: Informative Missingness"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Data Quality Realities", "Clinical Reality 1: Informative Missingness",
               "Absence of evidence is not evidence of absence in medical records")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "TESTS ARE NOT ORDERED AT RANDOM"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf.add_paragraph()
    p.text = "The Missingness Itself is Clinical Information"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("Doctors Order Tests for Sick Patients", "In physical telemetry (e.g. soil sensors or vibration gauges), missing data is often random hardware packet loss. In healthcare, a troponin test or a biopsy is only ordered when a doctor suspects severe disease. Healthy patients are missing tests precisely because they are healthy!"),
        ("The Imputation Trap", "Imputing a missing test with the population mean or median falsely assigns a sick value to a healthy patient, distorting the classification boundary."),
        ("Afternoon Demonstration", "In Step 1 (scripts/01_fhir_to_table.py --drop area), patient P0010 comes back with a missing value. The pipeline doesn't crash; it handles missingness safely via scikit-learn's SimpleImputer.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"{t}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_21(prs):
    """Clinical Realities: Class Imbalance & Leakage"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Evaluation Pitfalls", "Clinical Reality 2: Class Imbalance & Label Leakage",
               "Why naive accuracy scores lie, and how feature leakage ruins clinical models")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE ACCURACY TRAP"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "62.7% Majority-Class Baseline"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items = [
        ("The Naive Classifier", "In our cohort of 569 patients, 357 are benign (62.7%) and 212 are malignant (37.3%)."),
        ("Doing Nothing is 62.7% Accurate", "A dummy model predicting 'benign' every single time is already 62.7% accurate, but completely useless—it kills every cancer patient!"),
        ("The Lesson", "Never report raw accuracy alone in healthcare. We evaluate ROC-AUC, Sensitivity (Recall), and False Negatives.")
    ]
    for h, d in items:
        p = tf1.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "FEATURE LEAKAGE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf2.add_paragraph()
    p.text = "Leaking the Future Into Features"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items2 = [
        ("The Symptom", "Model scores 99.8% accuracy on training data, but fails immediately in real-world clinic trials."),
        ("The Cause", "Accidentally including features recorded after the diagnosis: e.g. 'oncologist consultation date' or 'prescribed chemotherapy drug'."),
        ("Rule of Thumb", "Input features MUST only reflect information available to the clinician at the exact moment of decision.")
    ]
    for h, d in items2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_22(prs):
    """The Data Impedance Mismatch (Two-Column)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "The Core Technical Gap", "The Data Impedance Mismatch",
               "Why machine learning frameworks cannot directly ingest clinical FHIR standards")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "HOW HOSPITALS STORE DATA"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "Hierarchical Clinical Events (FHIR)"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items = [
        ("Data Structure", "Deeply nested JSON resource trees linked by logical URIs and references."),
        ("Temporal Characteristics", "Variable-length event histories over months or years. Irregular sampling intervals."),
        ("Heterogeneity", "Mix of coded observations, narrative clinical notes, and multi-value panels.")
    ]
    for h, d in items:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "WHAT MACHINE LEARNING REQUIRES"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "2D Numerical Feature Matrices"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    items2 = [
        ("Data Structure", "Rigid 2D arrays: Feature matrix X in R^{N x D} and target label vector y in {0, 1}."),
        ("Strict Demands", "Every patient must have exactly D columns. Algorithms like Logistic Regression cannot handle raw JSON."),
        ("The Workshop Core", "Step 1 this afternoon (scripts/01_fhir_to_table.py) is the bridge that turns hierarchical FHIR into flat tabular features!")
    ]
    for h, d in items2:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_23(prs):
    """Safe Preprocessing Pipelines"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "ML Engineering", "Safe Preprocessing Pipelines in Scikit-Learn",
               "Preventing data leakage by encapsulating imputation, scaling, and classification")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE GOLD STANDARD: FITTING INSIDE THE FOLD"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf.add_paragraph()
    p.text = "Never Compute Statistics Across the Whole Cohort Before Splitting"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("The Common Bug", "Calculating the median to impute missing values or standardizing features using the mean of all 569 patients before splitting into train/test sets leaks information from the future."),
        ("The Scikit-Learn Pipeline", "We bundle SimpleImputer -> StandardScaler -> Classifier into a single Pipeline object. During cross-validation, the imputer and scaler learn parameters strictly from the training folds."),
        ("Exporting as One Artifact", "When saving models to disk (models/model.joblib in Step 3), we save the entire Pipeline. Serving new incoming FHIR patients requires zero external preprocessing scripts.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"{t}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_24(prs):
    """Closing the Loop: Predictions Back as FHIR"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Clinical Deployment", "Closing the Loop: Predictions Back as FHIR",
               "An AI model that cannot write back to the clinical workflow has zero clinical utility")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "STEP 5 IN THE AFTERNOON WORKSHOP"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf.add_paragraph()
    p.text = "Writing Model Inference Directly Into the Electronic Health Record"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("The Deployment Gap", "A trained machine learning model trapped inside a Jupyter notebook saves zero lives. Clinicians will never open a Python console."),
        ("Standard Clinical Output", "In Step 5c of this afternoon's hands-on session, clicking 'Send to record' in the Streamlit application serializes the predicted cancer probability into a valid FHIR RiskAssessment and Observation resource."),
        ("Seamless EHR Integration", "Because the prediction is returned as a standard FHIR resource, any modern EHR can consume the risk score without knowing or caring that it was generated by scikit-learn.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"{t}: "
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_25(prs):
    """Pre-Lunch Tech Check (3 Cards)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Lunch Checkpoint", "Tech Check Before Lunch (Library Studio Room)",
               "Verify your environment now so the room is 100% ready to run code at 14:00")

    steps = [
        ("STEP 1: REPO ROOT", "Open Terminal on Laptop",
         "Open your terminal application and navigate into the cloned workshop directory:\n\n$ cd fhir-ml-workshop\n\nEnsure git branch is set up."),
        ("STEP 2: SYNC UV", "Download Dependencies",
         "Run the fast package synchronizer from inside the repository:\n\n$ uv sync\n\nDownloads and pins the 66 required libraries (~580 MB)."),
        ("STEP 3: TEST SCIKIT", "Verify Environment",
         "Run the verification one-liner:\n\n$ uv run python -c \"import sklearn; print(sklearn.__version__)\"\n\nShould print 1.6.x cleanly!")
    ]

    for i, (title, sub, body) in enumerate(steps):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.7))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = LIME_GREEN

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.name = "Arial"; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

def main():
    print("Building clean 25-slide presentation deck for Morning Theory Session...")
    prs = create_deck()

    builders = [
        build_slide_01, build_slide_02, build_slide_03, build_slide_04, build_slide_05,
        build_slide_06, build_slide_07, build_slide_08, build_slide_09, build_slide_10,
        build_slide_11, build_slide_12, build_slide_13, build_slide_14, build_slide_15,
        build_slide_16, build_slide_17, build_slide_18, build_slide_19, build_slide_20,
        build_slide_21, build_slide_22, build_slide_23, build_slide_24, build_slide_25,
    ]

    for idx, fn in enumerate(builders, 1):
        fn(prs)
        print(f"  Slide {idx:02d} built successfully.")

    prs.save(DST_DECK)
    print(f"\n[Done] Generated {len(prs.slides)} clean slides in {DST_DECK}!")


if __name__ == "__main__":
    main()
