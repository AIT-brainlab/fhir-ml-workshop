"""
Build a clean, high-quality, professional PowerPoint deck for the Morning Theory Session.

Curriculum Structure: "2 + 1" Phase Architecture
- Phase 1: History of Medical & Hospital IT Systems (Pre-1960 to Today)
- Phase 2: Evolution of Clinical Data Modalities for ML & AI (Tabular, Spatial, Time-Series, Text/LLMs)
- Phase +1: AIT Research in Action — Telehealth & WP1 Raman Glucose POC (Dr. Chaklam Spotlight)

Venue: Library Studio Room
Audience: 20 undergraduate engineering students (IT, Agriculture, Mechanical)
Output: slides-morning/orientation-and-health-ai-foundations.pptx
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

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


# =============================================================================
# PROLOGUE & WELCOME
# =============================================================================

def build_slide_01(prs):
    """Cover Slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs, dark=True)

    if LOGO_PATH.exists():
        slide.shapes.add_picture(str(LOGO_PATH), Inches(0.9), Inches(0.8), width=Inches(2.5))

    b = add_card(slide, Inches(0.9), Inches(2.2), Inches(6.2), Inches(0.45), bg_color=MED_GREEN, border_color=None)
    tf_b = b.text_frame
    tf_b.margin_left = Inches(0.2)
    p_b = tf_b.paragraphs[0]
    p_b.text = "AIT BRAIN LAB · MEDICAL ICT & HEALTH AI WORKSHOP"
    p_b.font.bold = True; p_b.font.size = Pt(10); p_b.font.color.rgb = TEXT_WHITE

    t_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.8), Inches(11.5), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Orientation & Intro to AI in Health Foundations"
    p_t.font.bold = True; p_t.font.size = Pt(38); p_t.font.color.rgb = TEXT_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Hospital IT History, Modern Standards (HL7 v2, FHIR R4), and Clinical AI Modalities"
    p_sub.font.size = Pt(17); p_sub.font.color.rgb = LIME_GREEN
    p_sub.space_before = Pt(12)

    info = add_card(slide, Inches(0.9), Inches(5.2), Inches(11.5), Inches(1.4), bg_color=MED_GREEN, border_color=None)
    tf_i = info.text_frame
    tf_i.margin_left = Inches(0.3); tf_i.margin_top = Inches(0.2)
    p1 = tf_i.paragraphs[0]
    p1.text = "Morning Theory Session: 10:00 – 12:00  |  Venue: Library Studio Room"
    p1.font.bold = True; p1.font.size = Pt(14); p1.font.color.rgb = TEXT_WHITE

    p2 = tf_i.add_paragraph()
    p2.text = "Audience: 20 Undergraduate Engineering Students (IT, Agricultural Engineering, Mechanical Engineering)"
    p2.font.size = Pt(12); p2.font.color.rgb = LIME_GREEN
    p2.space_before = Pt(6)


def build_slide_02(prs):
    """The 2 + 1 Session Architecture"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Workshop Roadmap", "The 2 + 1 Session Architecture",
               "A structured journey from medical computing history to cutting-edge AI and AIT research")

    phases = [
        ("PHASE 1 (45 MINS)", "History of Hospital IT",
         "How healthcare evolved from paper charts and 1960s mainframes to HL7 v2 and modern FHIR R4 web standards.\n\n• Pre-1960 Analog Paper & Tubes\n• 1960s Mainframes & MUMPS\n• 1980s Sockets & HL7 Delimiters\n• 2014+ FHIR REST APIs",
         MED_GREEN),
        ("PHASE 2 (45 MINS)", "Evolution of AI Modalities",
         "How medical data transforms into mathematical representations across four core AI paradigms.\n\n• 1. Tabular (Classical ML)\n• 2. Spatial / Images (Vision)\n• 3. Time-Series (Telemetry)\n• 4. Text & LLMs (RAG / MCP)",
         DARK_GREEN),
        ("PHASE +1 (20 MINS)", "AIT Research in Action",
         "Dedicated spotlight for Prof. Chaklam Silpasuwanchai and the AIT Telehealth Project.\n\n• Telehealth & Assistive Systems\n• WP1 Raman Spectroscopy POC\n• Mobile App (BloodGlucose-App)\n• Real-World FHIR R4 Mapping",
         LIME_GREEN)
    ]

    for i, (badge, title, body, col) in enumerate(phases):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = badge
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


# =============================================================================
# PHASE 1: HISTORY OF MEDICAL & HOSPITAL IT SYSTEMS
# =============================================================================

def build_slide_03(prs):
    """Pre-1960: The Analog Era"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "Pre-1960: How Hospitals Kept Records Before Digital",
               "Physical charts, pneumatic vacuum tubes, and the dangers of lost medical memory")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE ANALOG HEALTHCARE SYSTEM"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf.add_paragraph()
    p.text = "Paper Folders, Bed Clipboards, and Vacuum Tubes"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("The Basement Record Room", "Patient histories lived as physical paper sheets in cardboard folders filed in massive hospital basements. Retrieving a record required orderlies to manually locate and pull folders."),
        ("Clipboards at the Foot of the Bed", "Vital signs (temperature, pulse, blood pressure) and medication doses were hand-scribbled by nurses onto paper flowsheets hanging on patient beds."),
        ("Pneumatic Tube Transport", "Blood vials and paper requisition forms were loaded into brass canisters and propelled through hospital pneumatic vacuum tubes directly into the laboratory."),
        ("The Severe Failure Mode", "Records were frequently misfiled, stained, illegible, or lost in fires. If a patient moved to another town or hospital, their clinical history vanished completely.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True; p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_04(prs):
    """The 1960s: Mainframes & MUMPS"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "The 1960s: Mainframes, Magnetic Tapes & MUMPS",
               "The birth of digital healthcare computing and the operating system that still runs today")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "HARDWARE & SNEAKERNET"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "IBM Mainframes & Punch Cards"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Mainframe Era", "Hospitals installed giant IBM 360/370 systems. Data was entered on 80-column Hollerith punch cards and 9-track magnetic tapes."),
        ("The Sneakernet", "No computer networks existed. To submit billing to Medicare or Blue Cross, technicians backed up data to tape reels, loaded them into car trunks, and physically drove them across town."),
        ("Centralized Processing", "Computing was strictly batch-oriented. Doctors could not view real-time records at the bedside.")
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
    p.text = "SOFTWARE REVOLUTION"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "1966: MUMPS at Mass General"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Created for Medicine", "Neil Pappalardo and Dr. Octo Barnett built MUMPS (Mass General Multi-Programming System) specifically for sparse medical records."),
        ("Hierarchical Tree Globals", "Used dynamic sparse trees (^PATIENT(id, 'LAB', 'GLUCOSE') = 105) rather than rigid relational SQL tables."),
        ("The Modern Legacy", "MUMPS powered the US Veterans Affairs VistA network. Today, Epic Systems (the world's largest EHR company) still runs its core backend on an advanced MUMPS engine (Caché / IRIS)!")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_05(prs):
    """The 1970s: Departmental Silos & The First Standards"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "The 1970s: Departmental Silos & Early Standards",
               "Minicomputers fragmented the hospital into specialized islands; ASTM invented pipe delimiters")

    steps = [
        ("Minicomputers", "DEC PDP-11 & VAX",
         "Departments broke away from the central mainframe. Pathology, Radiology, and Pharmacy bought dedicated minicomputers running isolated software."),
        ("ASTM Committee E31", "The Ancestor of HL7",
         "ASTM standardized automated blood analyzer serial communication (ASTM E1238). Crucially, ASTM invented the pipe and caret delimiter syntax (| and ^)!"),
        ("UB-82 Billing", "Financial Standardization",
         "National Uniform Billing Committee created UB-82 paper and fixed-width ASCII tape claim formats. Standardized billing codes, but zero clinical clinical depth.")
    ]

    for i, (title, sub, body) in enumerate(steps):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = MED_GREEN

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


def build_slide_06(prs):
    """The 1980s: The Networking Crisis"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "The 1980s: Local Networks & The Integration Crisis",
               "Ethernet connected the hardware, but software was trapped in quadratic complexity")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE INTEGRATION SPAGHETTI"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "The N(N-1)/2 Point-to-Point Trap"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Quadratic Explosion", "Every medical vendor used a bespoke schema. Connecting 10 departmental systems required 45 custom interfaces. Connecting 50 required 1,225 bridges!"),
        ("ACR-NEMA 50-Pin Cable", "In 1985, CT and MRI scanners required a custom, thick 50-pin copper cable running directly from scanner to console before DICOM existed."),
        ("Brittle Fragility", "Upgrading a single blood analyzer broke dozens of unmaintained point-to-point translation scripts.")
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
    p.text = "THE ARCHITECTURAL GAP"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "OSI Layers 1–4 vs. Layer 7"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("TCP/IP Solved Moving Packets", "Layers 1 through 4 (Ethernet, IP, TCP) successfully routed raw bytes from Computer A to Computer B."),
        ("What Do the Bytes Mean?", "When a blood machine sent packets to an EHR, the receiving software had no idea whether the payload was a patient's potassium or a billing invoice."),
        ("The Layer 7 Mandate", "Healthcare desperately needed an agreement at the OSI Application Layer (Layer 7). That realization sparked the creation of HL7.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_07(prs):
    """1987-1989: The Birth of HL7"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "1987–1989: The Birth of HL7 (Health Level Seven)",
               "A grassroots group at the University of Pennsylvania solves hospital communication")

    milestones = [
        ("MARCH 1987", "Committee Formed at HUP",
         "Dr. Sam Schultz (Hospital of the University of Pennsylvania) and Dr. Ed Hammond (Duke) convene hospital IT leaders to bypass slow academic standards."),
        ("OCTOBER 1987", "HL7 Version 1.0 (Draft)",
         "An 84-page working draft covering basic Admission, Discharge, Transfer (ADT). Syncs patient room assignments over raw TCP sockets via MLLP framing."),
        ("1989", "HL7 Version 2.1 (Commercial)",
         "First production standard widely adopted by major commercial vendors (Baxter, SMS, Sunquest). Becomes the global workhorse of medicine.")
    ]

    for i, (date, title, body) in enumerate(milestones):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = date
        p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = LIME_GREEN

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


def build_slide_08(prs):
    """Anatomy of an HL7 v2 Message (Code Panel)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "Anatomy of an HL7 v2 Message (`ORU^R01`)",
               "The pipe-and-hat (| and ^) ASCII format powering hospital messaging since 1989")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(4.8), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "SEGMENT STRUCTURE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    segments = [
        ("MSH (Message Header)", "Carries sending application, facility, message trigger (ORU^R01 lab result), and timestamp."),
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


def build_slide_09(prs):
    """Technological Relativity: Why HL7 v2 in 1989"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "Technological Relativity: Why HL7 v2 in 1989",
               "An engineering triumph for 1989 hardware that accumulated 30 years of Z-segment integration debt")

    flaws = [
        ("The Context of 1989", "Why Not JSON / REST?",
         "The Web didn't exist (HTTP came in 1991, JSON in 2001). Hardware was 1–4 MB RAM and 10 Mbps coax. Delimiter-separated ASCII allowed O(1) streaming directly into C buffers over raw TCP sockets without memory bloat.",
         MED_GREEN),
        ("The 'Z-Segment' Trap", "Non-Standard Custom Extensions",
         "HL7 v2 was so loosely specified that vendors added proprietary custom segments (ZBE, ZPD, ZAL). A message from Hospital A could not be parsed by Hospital B without bespoke translation code.",
         ALERT_RED),
        ("The Modern Debt", "Point-to-Point Socket Piping",
         "HL7 v2 runs over MLLP (raw TCP sockets). There are no URLs, no HTTP status codes, no authentication standards, and no query capabilities. Required costly interface engines (Mirth, Cloverleaf).",
         DARK_GREEN)
    ]

    for i, (title, sub, body, col) in enumerate(flaws):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
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


def build_slide_10(prs):
    """2003: The HL7 v3 Cautionary Tale"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "2003: The Cautionary Tale of HL7 Version 3",
               "The mathematically 'perfect' XML standard that software engineers completely rejected")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "THE DANGERS OF OVER-ENGINEERING"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf.add_paragraph()
    p.text = "How Abstract Modeling Alienated Real-World Developers"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("The Reference Information Model (RIM)", "HL7 attempted to create an all-encompassing, mathematically pure object-oriented model of all medicine. Everything was modeled as an Act, Entity, or Role."),
        ("Massive XML Overhead", "A simple patient temperature reading required thousands of lines of deeply nested XML tags, schemas, and abstract classes. Parsing was agonizingly slow on 2003 hardware."),
        ("The Developer Rebellion", "Software engineers refused to adopt it. It was too difficult to learn and implement without multimillion-dollar consulting contracts. Hospitals stuck with HL7 v2, cementing v3 as a famous software failure."),
        ("The Engineering Lesson", "In computing, pragmatic, developer-friendly designs always beat theoretically 'pure' but unusable standards.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True; p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_11(prs):
    """2014-Today: Enter HL7 FHIR"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "2014–Today: Enter HL7 FHIR (Built for the Web)",
               "Grahame Grieve redesigns healthcare data around HTTP REST, JSON, and web standards")

    cards = [
        ("Web-Native Standards", "HTTP, REST & JSON",
         "Built entirely on modern internet protocols. Developers query standard URLs (GET /Patient/P0001) and receive clean, human-readable JSON payloads."),
        ("The '80/20 Rule'", "Pragmatic Scope",
         "FHIR standardizes only the 80% of data concepts common across all healthcare globally. The remaining 20% edge cases are handled through explicitly validated Extensions."),
        ("Normative Stability", "FHIR R4 (2019)",
         "In 2019, FHIR Release 4 achieved Normative status. Core resources (Patient, Observation, Condition) are frozen with guaranteed permanent backwards compatibility.")
    ]

    for i, (title, sub, body) in enumerate(cards):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = LIME_GREEN

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


def build_slide_12(prs):
    """Core FHIR Architecture: Resources & References"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "Core FHIR Architecture: Resources, References & Bundles",
               "Modular clinical building blocks interconnected by unambiguous logical references")

    quads = [
        ("Patient Resource", "Demographics & Master ID",
         "The root subject. Contains biological sex, birthdate, identifier MRN, and contact info. Every clinical observation links here.",
         DARK_GREEN),
        ("Observation Resource", "Measurements & Vitals",
         "Clinical measurements: lab tests, vital signs, biopsy metrics. Contains coded LOINC tag, timestamp, and numeric value with UCUM units.",
         MED_GREEN),
        ("Condition Resource", "Clinical Diagnoses",
         "Active health problems or diagnoses. Links to Patient and contains ICD-10 or SNOMED CT problem codes with clinical status (active/resolved).",
         LIME_GREEN),
        ("Bundle Resource", "Packaging Patient Records",
         "A container resource holding multiple items. In this afternoon's lab, data/fhir/P0001.json is a Bundle packing 1 Patient, 10 Observations, and 1 Condition.",
         ALERT_RED)
    ]

    for i, (title, sub, desc, col) in enumerate(quads):
        row = i // 2
        col_idx = i % 2
        left = Inches(0.8) + col_idx * Inches(5.95)
        top = Inches(2.0) + row * Inches(2.45)
        c = add_card(slide, left, top, Inches(5.75), Inches(2.3))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(6)


def build_slide_13(prs):
    """Coded Vocabularies: The Semantic Glue"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "Coded Vocabularies: The Semantic Glue",
               "FHIR provides the grammatical schema; medical terminologies provide the dictionary")

    vocabs = [
        ("LOINC", "Logical Observation Identifiers",
         "The universal dictionary for lab assays and measurements.\n\n• Code 2339-0: Blood Glucose\n• Code 21908-9: Mean Cell Radius\n\nBecomes column headers in ML feature matrices.",
         MED_GREEN),
        ("SNOMED CT", "Systematized Nomenclature",
         "The global clinical terminology for findings, body sites, and procedures.\n\n• Code 439401001: Raman spectroscopy\n• Code 44054006: Ductal carcinoma\n\nDefines precise anatomical and procedural meaning.",
         DARK_GREEN),
        ("ICD-10 / ICD-11", "Disease Classification",
         "The World Health Organization standard for diagnoses and epidemiology.\n\n• Code C50.9: Malignant breast tumor\n• Code E11.9: Type 2 diabetes\n\nUsed globally for insurance claims and disease surveillance.",
         LIME_GREEN)
    ]

    for i, (title, sub, body, col) in enumerate(vocabs):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


def build_slide_semantic_krr(prs):
    """FHIR, The Semantic Web & KRR"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Computer Science & AI", "FHIR, The Semantic Web & KRR (Knowledge Representation)",
               "How FHIR implements W3C Linked Data, RDF Triples, and Description Logic reasoning in production")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE SEMANTIC WEB (W3C LINKED DATA)"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "URIs & The RDF Knowledge Graph"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Universal Resource Identifiers (URIs)", "Nothing in FHIR is a loose string. Every concept, coding system, and extension is anchored to a globally resolvable URI (e.g. http://loinc.org|2339-0)."),
        ("RDF Triples in Practice", "FHIR references form directed graph triples: Subject (Observation/obs-01) -> Predicate (subject) -> Object (Patient/P0001). Zero duplication; infinite traversal."),
        ("W3C RDF/Turtle Standard", "HL7 and W3C officially standardized the FHIR RDF specification (fhir/rdf.html). Entire hospital populations can be queried as a unified knowledge graph via SPARQL.")
    ]
    for h, d in bullets:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "KRR (KNOWLEDGE REPRESENTATION & REASONING)"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Description Logics & Automated Deduction"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Formal Ontologies (SNOMED CT)", "SNOMED CT is mathematically structured in Description Logic (the EL++ profile of OWL 2). Concepts possess formal relationships and subsumption hierarchies (Is-A)."),
        ("Automated Logical Inference", "If an AI clinical rule states 'Alert if patient has Respiratory Infection', a reasoner infers that Bacterial Pneumonia is a subclass of Respiratory Infection and fires the alert—even if those words never appear in the chart!"),
        ("Pragmatic KRR Success", "FHIR succeeded where academic Semantic Web stalled: it hid complex Description Logics under clean, friendly JSON REST APIs that web developers love.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_14(prs):
    """Global Adoption Spectrum"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 1 · History of Hospital IT", "Global Adoption: From Federal Law to Thailand",
               "Where FHIR is legally mandated, and the reality of legacy hospital engines")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "MANDATED BY LAW"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "United States & Europe"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("US 21st Century Cures Act", "Made clinical 'data blocking' illegal. Certified hospital software MUST expose standardized FHIR APIs (SMART on FHIR). Apple Health connects directly to thousands of US clinics via FHIR."),
        ("European Health Data Space (EHDS)", "Mandates cross-border clinical record exchange across all EU member states using FHIR.")
    ]
    for h, d in bullets:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "LOCAL & REGIONAL REALITY"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Thailand & Legacy Systems"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Thailand MOPH Initiatives", "The Ministry of Public Health and Thai health-tech agencies are actively implementing FHIR-based Health Information Exchanges (HIE) for national universal coverage digital claims."),
        ("The Hybrid Reality", "Replacing hospital databases costs millions. Many provincial hospitals still run HL7 v2 and MySQL engines; FHIR is deployed as an API Gateway wrapper sitting on top.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


# =============================================================================
# PHASE 2: EVOLUTION OF CLINICAL DATA MODALITIES FOR ML & AI
# =============================================================================

def build_slide_15(prs):
    """Phase 2 Section Header"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs, dark=True)

    b = add_card(slide, Inches(0.9), Inches(1.8), Inches(6.0), Inches(0.45), bg_color=MED_GREEN, border_color=None)
    tf_b = b.text_frame
    tf_b.margin_left = Inches(0.2)
    p_b = tf_b.paragraphs[0]
    p_b.text = "PHASE 2 · CLINICAL DATA MODALITIES FOR AI"
    p_b.font.bold = True; p_b.font.size = Pt(10); p_b.font.color.rgb = TEXT_WHITE

    t_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.5), Inches(11.5), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "The Four Modalities of Health AI"
    p_t.font.bold = True; p_t.font.size = Pt(38); p_t.font.color.rgb = TEXT_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "From 2D Tabular Feature Matrices to Spatial Tensors, Signal Telemetry, and LLM Agents"
    p_sub.font.size = Pt(17); p_sub.font.color.rgb = LIME_GREEN
    p_sub.space_before = Pt(12)

    c = add_card(slide, Inches(0.9), Inches(5.0), Inches(11.5), Inches(1.6), bg_color=MED_GREEN, border_color=None)
    tf_c = c.text_frame
    tf_c.margin_left = Inches(0.3); tf_c.margin_top = Inches(0.2)
    p1 = tf_c.paragraphs[0]
    p1.text = "Different Math, Different Algorithms:"
    p1.font.bold = True; p1.font.size = Pt(13); p1.font.color.rgb = LIME_GREEN

    p2 = tf_c.add_paragraph()
    p2.text = "There is no single 'Health AI algorithm.' Tabular data requires gradient trees; radiology requires 3D convolution; telemetry requires temporal state spaces; notes require LLMs."
    p2.font.bold = True; p2.font.size = Pt(13.5); p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)


def build_slide_16(prs):
    """Modality 1: Tabular Data (Classical ML)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Modality 1", "Tabular Data: The Classical Machine Learning Engine",
               "Structured numeric matrices powering clinical risk stratification and lab assays")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "DATA REPRESENTATION"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "2D Matrices: X in R^{N x D}"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Clinical Sources", "Automated lab panels (glucose, creatinine), vital signs, cell morphometry from biopsies, and patient demographics."),
        ("Mathematical Structure", "A rectangular table of N patients (rows) by D features (columns). Targets y in {0, 1}."),
        ("Strict Requirements", "Every cell must be a valid float. Algorithms cannot handle raw nested JSON or string codes without preprocessing.")
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
    p.text = "ALGORITHMS & WORKSHOP LINK"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Afternoon Workshop Focus"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Core Models", "Logistic Regression, Random Forests, XGBoost, and k-Means Clustering."),
        ("Step 1 (Flatten FHIR)", "In scripts/01_fhir_to_table.py, we parse real FHIR bundles and extract LOINC observations into tabular columns."),
        ("Step 3 (Train Pipelines)", "We fit Logistic Regression and Random Forest models to predict malignancy from 30 cell nucleus features.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_17(prs):
    """Modality 2: Spatial & Imaging Data"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Modality 2", "Spatial & Imaging Data: Computer Vision in Medicine",
               "Radiographs, 3D CT/MRI scans, and gigapixel histology whole-slide images")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "HIGH-DIMENSIONAL SPATIAL TENSORS"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf.add_paragraph()
    p.text = "From 2D X-Rays to 3D/4D Volumetric Tensors"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("The DICOM Standard", "Medical images are not simple JPEGs. They are DICOM files storing calibrated pixel arrays alongside spatial metadata (slice thickness, magnetic field strength, patient positioning)."),
        ("Mathematical Format", "Tensors in R^{C x D x H x W} where C = Channels/Sequences, D = Depth/Slices, H, W = Image dimensions. Whole Slide Images (WSI) reach 100,000 x 100,000 pixels."),
        ("AI Architectures", "Convolutional Neural Networks (ResNet, EfficientNet), Vision Transformers (ViT), and U-Net encoder-decoder models for anatomical tumor segmentation."),
        ("Clinical Challenge", "Multi-gigabyte file sizes, spatial resolution vs compute memory trade-offs, and requirement for expert radiologist pixel-level annotations.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True; p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_18(prs):
    """Modality 3: Time-Series & Continuous Telemetry"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Modality 3", "Time-Series & Telemetry: Continuous Physiological Streams",
               "High-frequency sensor waveforms from ICU monitors, ECG leads, and wearable devices")

    c = add_card(slide, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "SEQUENTIAL TEMPORAL SIGNALS"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf.add_paragraph()
    p.text = "Streaming Signals at 250 Hz to 1 Sample/Hour"
    p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    points = [
        ("Clinical Telemetry Streams", "12-lead Electrocardiography (ECG), continuous arterial blood pressure in ICUs, pulse oximetry (PPG), and Continuous Glucose Monitors (CGM)."),
        ("Mathematical Representation", "1D sequential arrays x(t) sampled at high frequency. Processed via sliding windows, Fast Fourier Transforms (FFT), or Continuous Wavelet Transforms."),
        ("Algorithms", "Recurrent Neural Networks (LSTMs), 1D Temporal Convolutional Networks (TCN), and modern State Space Models (Mamba) for predicting acute sepsis 6 hours in advance."),
        ("Engineering Reality", "Sensor motion artifacts, loose electrodes, and non-stationary baseline drift require heavy digital signal processing before ML.")
    ]
    for t, b in points:
        p = tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True; p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = b; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_19(prs):
    """Modality 4: Unstructured Text & Clinical Notes"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Modality 4", "Unstructured Text: What 90% of People Mean by 'AI'",
               "Physician progress notes, discharge summaries, operative logs, and clinical LLMs")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE UNSTRUCTURED MAJORITY"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "80% of Health Data Lives in Text"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Clinical Narratives", "Doctors do not fill out structured dropdown forms; they write narrative stories explaining clinical reasoning, nuance, and history."),
        ("Complex Medical Jargon", "Heavy abbreviations ('sob' = shortness of breath, not an insult!), medical shorthand, and typos make rule-based parsers fail."),
        ("Rich Hidden Signal", "Social determinants of health (living alone, smoking history) are only documented in free-text clinical notes.")
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
    p.text = "THE GENAI PARADIGM"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Clinical LLMs & Copilots"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Medical Foundation Models", "Specialized models (Med-PaLM 2, BioGPT, ClinicalBERT) trained on medical literature and clinical corpora."),
        ("Ambient Clinical Scribing", "Microphones listen to doctor-patient conversation in real time and automatically draft the clinical note into the EHR."),
        ("Clinical Question Answering", "Synthesizing complex multi-year patient records into concise diagnostic briefings for busy clinicians.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_20(prs):
    """The Formatting Dilemma for LLMs: Token Bloat vs. Markdown"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · LLMs & Formats", "The Formatting Dilemma: Why LLMs Choke on Raw FHIR",
               "Nested JSON metadata dilutes clinical signal; Markdown tables provide the cure")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), border_color=ALERT_RED)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE RAW JSON TRAP"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "Token Bloat & Hallucination"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Severe Token Overhead", "A single FHIR Observation consumes 300–500 tokens of nested boilerplate (resourceType, meta, system, coding). A patient chart burns 50,000+ tokens!"),
        ("Diluted Clinical Signal", "The critical clinical number ('Glucose: 118') is buried inside hundreds of curly braces, degrading LLM attention."),
        ("Hallucination Risk", "High token boilerplate increases the probability that an LLM misassociates a test value with the wrong timestamp.")
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
    p.text = "THE MODERN SOLUTION"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Clean Markdown (.md) Tables"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("60–75% Token Reduction", "Converting FHIR resources into clean Markdown tables preserves semantic clarity while stripping thousands of redundant JSON lines."),
        ("Superior LLM Recall", "Foundation models are pre-trained heavily on Markdown tables and bulleted text, leading to faster inference and zero syntactic hallucinations."),
        ("Clean Architecture", "FHIR remains the backend database protocol; Markdown is the token-efficient presentation layer for LLM prompts.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_21(prs):
    """Clinical AI Agents & Tool Calling: MCP & RAG"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · AI Agents", "Clinical AI Agents: RAG & Model Context Protocol (MCP)",
               "Moving from passive chatbots to autonomous clinical copilots with deterministic tools")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "KNOWLEDGE RETRIEVAL"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "Clinical RAG & Vector DBs"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Semantic Embeddings", "Clinical narrative notes and medical guidelines are chunked and converted into vector embeddings via clinical embedding models."),
        ("Vector Databases", "Stored in high-speed vector stores (pgvector, Chroma, Pinecone) for sub-millisecond similarity search."),
        ("Grounded Answers", "When an agent answers a question, it retrieves the top-3 most relevant patient notes and clinical trial guidelines to prevent hallucinations.")
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
    p.text = "DETERMINISTIC ACTION"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Model Context Protocol (MCP)"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Tool-Calling Paradigm", "Agents do not guess; they invoke structured tools: get_patient_labs(patient_id='P0001', code='2339-0')."),
        ("Scoped & Auditable", "Every action an agent takes is logged, authenticated, and constrained by role-based access control."),
        ("The Future Standard", "MCP provides the open protocol for connecting AI agents to hospital databases and diagnostic instruments safely.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_22(prs):
    """The Data Impedance Mismatch"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Data Architecture", "The Fundamental Data Impedance Mismatch",
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
    """Clinical Realities: Missingness & Imbalance"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Data Realities", "Clinical Realities: Informative Missingness & Class Imbalance",
               "Healthcare data is not sampled at random; absence of evidence is clinical information")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), border_color=ALERT_RED)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "DATA QUALITY REALITY"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "Informative Missingness"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("Tests Ordered for Sick Patients", "In sensors, missing data is hardware loss. In medicine, a troponin test or biopsy is ordered because disease is suspected! Healthy patients lack tests because they are healthy."),
        ("The Imputation Trap", "Imputing missing values with population mean assigns sick values to healthy people. Must be handled deliberately via SimpleImputer inside cross-validation folds.")
    ]
    for h, d in bullets:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "EVALUATION PITFALL"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Class Imbalance (63% Trap)"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("The Baseline Illusion", "In cancer screening, 63% (or 95%) of patients are benign. A dummy model predicting 'benign' every time achieves 63% accuracy while failing 100% of cancer cases!"),
        ("Metric Requirements", "Accuracy is dangerous. We evaluate models using Recall (Sensitivity), ROC-AUC, and tune the classification threshold deliberately.")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_24(prs):
    """Towards AI-Native Health Data Standards"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase 2 · Future Architecture", "Towards AI-Native Health Data Standards",
               "The emerging Dual-Stack Architecture uniting legal compliance and continuous learning")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE THREE ERAS OF HEALTH DATA"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "From Sockets to Autonomous AI"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    eras = [
        ("Era 1: 1989–2011 (Local Machines)", "HL7 v2: Pipe-delimited ASCII strings over TCP sockets for local hospital LANs."),
        ("Era 2: 2014–2025 (Web & Mobile)", "HL7 FHIR: JSON REST APIs and web standards for apps, clinicians, and portals."),
        ("Era 3: 2026+ (Artificial Intelligence)", "AI-Native Stack: Vector embeddings, token-optimized Markdown, and Agentic MCP tool protocols.")
    ]
    for h, d in eras:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "THE DUAL-STACK SOLUTION"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Record Layer + Intelligence Layer"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    layers = [
        ("Layer A · System of Record (FHIR)", "FHIR remains the authoritative, legally audited, and human-verified patient ledger for billing, medication safety, and clinical charts."),
        ("Layer B · System of Intelligence (AI Store)", "High-performance vector stores and feature stores (e.g. Feast, pgvector) continuously ingest FHIR streams, serving ML models and LLM agents in milliseconds."),
        ("Health MCP Protocol Standard", "Standardizing tool schemas so any clinical AI agent can query and propose treatment orders across any hospital safely.")
    ]
    for h, d in layers:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


# =============================================================================
# PHASE +1: AIT RESEARCH IN ACTION — TELEHEALTH & WP1 (CHAKLAM SPOTLIGHT)
# =============================================================================

def build_slide_25(prs):
    """Phase +1 Section Header: AIT Research in Action"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs, dark=True)

    b = add_card(slide, Inches(0.9), Inches(1.8), Inches(6.2), Inches(0.45), bg_color=MED_GREEN, border_color=None)
    tf_b = b.text_frame
    tf_b.margin_left = Inches(0.2)
    p_b = tf_b.paragraphs[0]
    p_b.text = "PHASE +1 · AIT RESEARCH IN ACTION (CHAKLAM'S SPOTLIGHT)"
    p_b.font.bold = True; p_b.font.size = Pt(10); p_b.font.color.rgb = TEXT_WHITE

    t_box = slide.shapes.add_textbox(Inches(0.9), Inches(2.5), Inches(11.5), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Telehealth & Assistive Systems"
    p_t.font.bold = True; p_t.font.size = Pt(38); p_t.font.color.rgb = TEXT_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Monitoring and Assistive Systems for Elderly and Disabled People — Prof. Chaklam Silpasuwanchai"
    p_sub.font.size = Pt(17); p_sub.font.color.rgb = LIME_GREEN
    p_sub.space_before = Pt(12)

    c = add_card(slide, Inches(0.9), Inches(5.0), Inches(11.5), Inches(1.6), bg_color=MED_GREEN, border_color=None)
    tf_c = c.text_frame
    tf_c.margin_left = Inches(0.3); tf_c.margin_top = Inches(0.2)
    p1 = tf_c.paragraphs[0]
    p1.text = "Grounding Theory in Real AIT Systems Engineering:"
    p1.font.bold = True; p1.font.size = Pt(13); p1.font.color.rgb = LIME_GREEN

    p2 = tf_c.add_paragraph()
    p2.text = "Connecting optical Raman laser sensors, computer vision telemetry, and haptic rehabilitation robotics to global clinical standards and FHIR microservices."
    p2.font.bold = True; p2.font.size = Pt(13.5); p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)


def build_slide_26(prs):
    """The AIT Telehealth Project: Four Work Packages"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase +1 · AIT Spotlight", "AIT Telehealth Project: Four Work Packages",
               "Bridging physical sensor engineering, edge robotics, and secure clinical cloud platforms")

    wps = [
        ("WP1: Optical Glucose Sensing",
         "Non-Invasive Raman Sensor",
         "Measures blood glucose without skin pricks using 785nm optical Raman laser spectroscopy.",
         "POC App: github.com/akraradets/BloodGlucose-App\nEdge ML calibration models.",
         LIME_GREEN),
        ("WP2: Activity & Fall Telemetry",
         "Computer Vision & Wi-Fi CSI",
         "Monitors elderly mobility and detects falls in real time using privacy-preserving camera feeds and Wi-Fi disturbance.",
         "Continuous spatial & time-series AI\nEdge inference on embedded hardware.",
         MED_GREEN),
        ("WP3: Remote Haptic Therapy",
         "Robotic Physical Rehabilitation",
         "Upper-limb rehabilitation device providing programmable force-feedback for stroke patient recovery.",
         "Bi-directional physical telemetry\nRemote clinician tele-operation.",
         DARK_GREEN),
        ("WP4: Cloud Telehealth Platform",
         "Secure FHIR Integration",
         "Consolidates telemetry from WP1–WP3 into an encrypted cloud backend for clinician review.",
         "Standardized FHIR R4 resources\nReal-time web & mobile dashboards.",
         ALERT_RED)
    ]

    for i, (badge, title, body, sub, col) in enumerate(wps):
        left = Inches(0.8) + i * Inches(2.95)
        c = add_card(slide, left, Inches(2.0), Inches(2.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = badge
        p.font.bold = True; p.font.size = Pt(10.5); p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9.5); p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(10)


def build_slide_27(prs):
    """WP1 Deep Dive: Non-Invasive Glucose via Raman Spectroscopy"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase +1 · AIT Spotlight", "WP1 Deep Dive: Non-Invasive Glucose via Raman Spectroscopy",
               "Translating raw optical spectra into calibrated physiological biomarkers (BloodGlucose-App)")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.35)

    p = tf1.paragraphs[0]
    p.text = "THE OPTICAL SENSOR PRINCIPLE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    p = tf1.add_paragraph()
    p.text = "Inelastic Photon Scattering"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets = [
        ("The Clinical Need", "Diabetic and elderly patients require frequent daily blood checks. Finger-prick lancets cause tissue damage, infection risks, and poor patient compliance."),
        ("Raman Spectroscopy", "A 785nm near-infrared laser illuminates interstitial fluid. Photons scatter inelastically off glucose molecules, yielding a unique spectral fingerprint around 1125 cm⁻¹."),
        ("Mobile POC App", "Built at AIT (github.com/akraradets/BloodGlucose-App). Connects over Bluetooth Low Energy (BLE) to the Raman hardware spectrometer.")
    ]
    for h, d in bullets:
        p = tf1.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.35)

    p = tf2.paragraphs[0]
    p.text = "THE MACHINE LEARNING ENGINE"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = LIME_GREEN

    p = tf2.add_paragraph()
    p.text = "Modality 3 → Modality 1 Mapping"
    p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = DARK_GREEN
    p.space_before = Pt(6)

    bullets2 = [
        ("Signal Preprocessing", "Raw spectra suffer from skin autofluorescence and dark current noise. Preprocessing uses baseline polynomial subtraction and Standard Normal Variate (SNV) scaling."),
        ("Edge Calibration Model", "Partial Least Squares (PLS) regression and Random Forests map the continuous 1D spectral curve directly to blood glucose (mg/dL)."),
        ("The Standard Challenge", "Once the phone calculates '118 mg/dL', how do we push it to a hospital EHR without losing context? We serialize it to FHIR!")
    ]
    for h, d in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED


def build_slide_28(prs):
    """Closing the Circuit: Mapping AIT Raman Reading into FHIR R4"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Phase +1 · AIT Spotlight", "Closing the Circuit: Mapping AIT Raman Readings into FHIR",
               "How physical sensor telemetry becomes a globally interoperable clinical resource")

    c1 = add_card(slide, Inches(0.8), Inches(2.0), Inches(4.8), Inches(4.8))
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "STANDARDS HARMONIZATION"
    p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = MED_GREEN

    items = [
        ("LOINC 2339-0", "Standard test code for Glucose [Mass/vol] in Blood. Guarantees that any EHR on Earth recognizes the value as blood sugar."),
        ("SNOMED CT 439401001", "Identifies the measurement method as In-vivo Raman spectroscopy rather than a laboratory venous blood draw."),
        ("UCUM Units (mg/dL)", "Explicit unit coding eliminates fatal confusion between US (mg/dL) and European/Thai (mmol/L) scales.")
    ]
    for h, d in items:
        p = tf1.add_paragraph()
        p.text = f"{h}:\n"
        p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(10)
        run = p.add_run(); run.text = d; run.font.bold = False; run.font.color.rgb = TEXT_MUTED

    c2 = add_card(slide, Inches(5.9), Inches(2.0), Inches(6.6), Inches(4.8), bg_color=DARK_PANEL, border_color=None)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "// AIT WP1 Raman Glucose in FHIR R4 JSON"
    p.font.name = "Courier New"; p.font.size = Pt(10.5); p.font.color.rgb = LIME_GREEN

    json_lines = [
        '{\n  "resourceType": "Observation",\n  "id": "ait-raman-glucose-001",\n  "status": "final",',
        '  "code": {\n    "coding": [{\n      "system": "http://loinc.org",\n      "code": "2339-0",\n      "display": "Glucose [Mass/vol] in Blood"\n    }]\n  },',
        '  "subject": { "reference": "Patient/P0001" },\n  "effectiveDateTime": "2026-09-09T10:30:00+07:00",',
        '  "valueQuantity": {\n    "value": 118,\n    "unit": "mg/dL",\n    "system": "http://unitsofmeasure.org",\n    "code": "mg/dL"\n  },',
        '  "method": {\n    "coding": [{\n      "system": "http://snomed.info/sct",\n      "code": "439401001",\n      "display": "In-vivo Raman spectroscopy"\n    }]\n  }\n}'
    ]
    for snippet in json_lines:
        p = tf2.add_paragraph()
        p.text = snippet
        p.font.name = "Courier New"; p.font.size = Pt(9); p.font.color.rgb = CODE_GREEN
        p.space_before = Pt(4)


# =============================================================================
# EPILOGUE & TRANSITION TO AFTERNOON
# =============================================================================

def build_slide_29(prs):
    """Closing the Loop & Tech Check"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_background(slide, prs)
    add_header(slide, "Bridge to Afternoon", "Closing the Classical Loop & Tech Checkpoint",
               "Verify your environment now so the room is 100% ready to run code at 14:00")

    steps = [
        ("CLOSING THE LOOP", "Predictions Back as FHIR",
         "In Step 5c of this afternoon's workshop, clicking 'Send to record' wraps our scikit-learn cancer risk prediction back into a valid FHIR RiskAssessment and Observation resource."),
        ("TERMINAL CHECK", "Navigate to Repo Root",
         "Open your terminal application and verify your current working directory:\n\n$ cd fhir-ml-workshop\n\nEnsure git branch is clean."),
        ("SYNC ENVIRONMENT", "Verify Libraries Before Lunch",
         "Run the fast package synchronizer from inside the repository:\n\n$ uv sync\n\nVerify sklearn:\n$ uv run python -c \"import sklearn; print(sklearn.__version__)\"")
    ]

    for i, (title, sub, body) in enumerate(steps):
        left = Inches(0.8) + i * Inches(3.95)
        c = add_card(slide, left, Inches(2.0), Inches(3.75), Inches(4.8))
        tf = c.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = LIME_GREEN

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = DARK_GREEN
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.name = "Arial"; p.font.size = Pt(10.5); p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


# -----------------------------------------------------------------------------
# MAIN BUILDER
# -----------------------------------------------------------------------------

def main():
    print("Building clean 30-slide presentation deck for Morning Theory Session (2 + 1 Architecture)...")
    prs = create_deck()

    builders = [
        build_slide_01, build_slide_02, build_slide_03, build_slide_04, build_slide_05,
        build_slide_06, build_slide_07, build_slide_08, build_slide_09, build_slide_10,
        build_slide_11, build_slide_12, build_slide_13, build_slide_semantic_krr, build_slide_14,
        build_slide_15, build_slide_16, build_slide_17, build_slide_18, build_slide_19,
        build_slide_20, build_slide_21, build_slide_22, build_slide_23, build_slide_24,
        build_slide_25, build_slide_26, build_slide_27, build_slide_28, build_slide_29,
    ]

    for idx, fn in enumerate(builders, 1):
        fn(prs)
        print(f"  Slide {idx:02d} built successfully.")

    prs.save(DST_DECK)
    print(f"\n[Done] Generated {len(prs.slides)} clean slides in {DST_DECK}!")


if __name__ == "__main__":
    main()
