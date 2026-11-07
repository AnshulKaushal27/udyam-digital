import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_pptx):
    prs = Presentation()
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6] # blank layout

    cover_bg = r'E:\Airtel\template_assets\ppt\media\image2.jpg'
    inside_bg = r'E:\Airtel\template_assets\ppt\media\image1.jpg'

    # Color palette
    RED = RGBColor(228, 0, 0)         # Airtel Red
    DARK_RED = RGBColor(170, 0, 0)
    NAVY = RGBColor(16, 24, 40)       # Dark Slate / Navy
    LIGHT_BG = RGBColor(248, 249, 250)
    BORDER_COL = RGBColor(220, 224, 230)
    WHITE = RGBColor(255, 255, 255)
    GRAY_TEXT = RGBColor(100, 110, 125)
    DARK_TEXT = RGBColor(30, 41, 59)
    GREEN = RGBColor(16, 149, 79)
    GOLD = RGBColor(245, 158, 11)

    def set_font(p, text, size=12, bold=False, color=DARK_TEXT, align=PP_ALIGN.LEFT, font_name="Segoe UI"):
        p.text = text
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = align

    def add_card(slide, left, top, width, height, fill_color=WHITE, line_color=BORDER_COL):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        if line_color:
            shape.line.color.rgb = line_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    s1.shapes.add_picture(cover_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))

    # Dark translucent container for text readability
    c1 = add_card(s1, Inches(0.8), Inches(0.7), Inches(8.4), Inches(4.2), fill_color=RGBColor(10, 15, 25), line_color=RED)

    # Content
    tb = s1.shapes.add_textbox(Inches(1.1), Inches(0.9), Inches(7.8), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    set_font(p, "AIRTEL SYNC 2026 · DIGITAL TRACK (CASE & PROTOTYPE ROUND)", size=11, bold=True, color=GOLD)

    p = tf.add_paragraph()
    set_font(p, "PROJECT UDYAM DIGITAL", size=28, bold=True, color=WHITE)

    p = tf.add_paragraph()
    set_font(p, "Making India's 6.3 Crore MSMEs Go Digital in One Sitting", size=15, bold=False, color=RGBColor(220, 225, 235))

    p = tf.add_paragraph()
    p.space_before = Pt(12)
    set_font(p, "A mobile-first, GenAI-guided conversational onboarding platform that transforms slow, paper-heavy B2B telecom sales into a 15-minute digital journey with automated KYC and transparent bundling.", size=11, bold=False, color=RGBColor(180, 190, 205))

    # Team & Submission info box inside cover
    p = tf.add_paragraph()
    p.space_before = Pt(18)
    set_font(p, "TEAM NAME: Halo  |  CAMPUS: Thapar Institute of Engineering & Technology", size=11, bold=True, color=WHITE)

    p = tf.add_paragraph()
    set_font(p, "AIRTEL SYNC 2026 · DIGITAL TRACK  |  DATE: November 2026", size=10, bold=False, color=RGBColor(200, 210, 225))

    # Metric Badges at bottom of cover
    y_m = Inches(3.9)
    metrics_data = [
        ("+200% Conversion Lift", "7.36% -> 22.0% Net Conv.", GREEN),
        ("80% TAT Reduction", "17.6 Days -> 3.5 Days", RED),
        ("75% CAC Reduction", "Rs 15,000 -> Rs 3,800", GOLD)
    ]
    for idx, (m_title, m_sub, col) in enumerate(metrics_data):
        b_x = Inches(1.1 + idx * 2.65)
        add_card(s1, b_x, y_m, Inches(2.5), Inches(0.8), fill_color=RGBColor(20, 30, 45), line_color=col)
        tb_m = s1.shapes.add_textbox(b_x + Inches(0.1), y_m + Inches(0.08), Inches(2.3), Inches(0.65))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p_m = tf_m.paragraphs[0]
        set_font(p_m, m_title, size=11, bold=True, color=col)
        p_m2 = tf_m.add_paragraph()
        set_font(p_m2, m_sub, size=9, bold=False, color=WHITE)

    # Helper function for header in inside slides
    def add_slide_header(slide, title, category="AIRTEL SYNC 2026 · DIGITAL TRACK"):
        # Header text
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.65), Inches(8.8), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = 0
        tf.margin_bottom = 0
        p_cat = tf.paragraphs[0]
        set_font(p_cat, category.upper(), size=9, bold=True, color=RED)
        p_tit = tf.add_paragraph()
        set_font(p_tit, title, size=16, bold=True, color=NAVY)

    # =========================================================================
    # SLIDE 2: FUNNEL DIAGNOSTIC & PROBLEM FRAMING
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    s2.shapes.add_picture(inside_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    add_slide_header(s2, "Funnel Diagnostic: The Rs 15k CAC & 17.6-Day Onboarding Crisis")

    # Left Container: Funnel Flow (4.2 inches wide)
    add_card(s2, Inches(0.6), Inches(1.4), Inches(4.3), Inches(3.6), fill_color=LIGHT_BG)
    tb_fn = s2.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(4.0), Inches(3.4))
    tf_fn = tb_fn.text_frame
    tf_fn.word_wrap = True

    p = tf_fn.paragraphs[0]
    set_font(p, "EMPIRICAL CONVERSION FUNNEL (5,000 LEADS)", size=11, bold=True, color=NAVY)

    funnel_rows = [
        ("1. Leads Generated", "5,000 (100%)", "Tier 1 & Tier 2 Cities", NAVY),
        ("2. Contacted", "3,406 (68.1%)", "805 unreachable, 531 no time for visit", NAVY),
        ("3. Needs Assessed", "1,974 (39.5%)", "470 not interested, 325 ISP locked", NAVY),
        ("4. Quote Accepted", "861 (17.2%)", "STEEPEST DROP: 56.4% collapse at quote!", RED),
        ("5. KYC Complete", "588 (11.8%)", "173 drops: paperwork long / missing docs", NAVY),
        ("6. Activated", "368 (7.36%)", "98 drops: install delayed >21 days", GREEN)
    ]
    for stage, count, note, col in funnel_rows:
        p = tf_fn.add_paragraph()
        p.space_before = Pt(4)
        set_font(p, f"{stage}: {count}", size=10, bold=True, color=col)
        p_sub = tf_fn.add_paragraph()
        set_font(p_sub, f"  └ {note}", size=8.5, bold=False, color=GRAY_TEXT)

    # Right Container: 3 Core Bottlenecks (4.3 inches wide)
    add_card(s2, Inches(5.1), Inches(1.4), Inches(4.3), Inches(3.6), fill_color=WHITE)
    tb_rt = s2.shapes.add_textbox(Inches(5.25), Inches(1.5), Inches(4.0), Inches(3.4))
    tf_rt = tb_rt.text_frame
    tf_rt.word_wrap = True

    p = tf_rt.paragraphs[0]
    set_font(p, "KEY STRUCTURAL BOTTLENECK ANALYSIS", size=11, bold=True, color=RED)

    bottlenecks = [
        ("Opaque, Multi-Day Quotes (56.4% Drop)", 
         "Quotes take 3-5 days to prepare and arrive as confusing multi-page PDFs with telecom product SKUs. 621 leads dropped citing 'Price too high' or 'Competitor cheaper'."),
        ("Tedious Paperwork & Verification (31.7% Drop)", 
         "Physical collection of GST, Udyam, utility bills, and signatory IDs causes severe merchant dropouts. GST-registered leads convert 4.8x higher (9.56% vs 2.05%)."),
        ("Black-Hole Status Tracking & Churn (37.4% Drop)", 
         "Customers wait 17.6 days on average and call 3+ times to chase status. 98 leads cancelled due to >21 day installation delays. Unsustainable blended CAC of Rs 15,000!")
    ]
    for b_title, b_desc in bottlenecks:
        p = tf_rt.add_paragraph()
        p.space_before = Pt(8)
        set_font(p, f"• {b_title}", size=10, bold=True, color=NAVY)
        p_desc = tf_rt.add_paragraph()
        set_font(p_desc, b_desc, size=8.5, bold=False, color=DARK_TEXT)

    # =========================================================================
    # SLIDE 3: DETAILED COMPETITIVE ANALYSIS & STRATEGIC ADVANTAGE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    s3.shapes.add_picture(inside_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    add_slide_header(s3, "Competitive Landscape: Strategic Advantage of Project Udyam")

    # Add Table for Competitive Analysis
    table_shape = s3.shapes.add_table(5, 5, Inches(0.6), Inches(1.4), Inches(8.8), Inches(2.7))
    t = table_shape.table
    t.columns[0].width = Inches(1.8)
    t.columns[1].width = Inches(1.7)
    t.columns[2].width = Inches(1.7)
    t.columns[3].width = Inches(1.7)
    t.columns[4].width = Inches(1.9)

    headers = ["Evaluation Metric", "Incumbent Telcos\n(Jio Biz / Tata Tele)", "Digital SaaS\n(Zoho / Khatabook)", "Unorganized\nLocal Vendors", "Accel / Airtel\n(Project Udyam)"]
    for i, h in enumerate(headers):
        cell = t.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RED if i == 4 else NAVY
        p = cell.text_frame.paragraphs[0]
        set_font(p, h, size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    matrix_rows = [
        ("Full-Stack Offering", "Connectivity only; apps sold via separate partners", "Apps only (invoicing/CRM); no network/SIMs", "Broadband or SIM only; zero SLA/support", "Unified: Connectivity + Cloud + SaaS + Security"),
        ("Onboarding Experience", "Slow field rep visits; 3-5 day PDF quotes", "Fast self-serve DIY, but limited to app setup", "Doorstep cash deal, highly manual & fragmented", "15-Min Multilingual GenAI Advisor + Instant Quote"),
        ("KYC & Verification", "Manual paper collection (GST, Udyam, ID proofs)", "Self-certified email/mobile login (no DoT KYC)", "Unverified SIMs / local broadband registration", "Automated Registry Lookup + OCR (<90d check)"),
        ("Billing & Support", "Multiple bills per product; disjointed support", "Fragmented credit card SaaS subscriptions", "Multiple cash/UPI vendors with zero SLA", "Single Unified Bill + 24/7 Proactive SLA Tracker")
    ]
    for row_idx, r_data in enumerate(matrix_rows):
        for col_idx, text in enumerate(r_data):
            cell = t.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(254, 242, 242) if col_idx == 4 else (WHITE if row_idx % 2 == 0 else LIGHT_BG)
            p = cell.text_frame.paragraphs[0]
            col = RED if col_idx == 4 else (NAVY if col_idx == 0 else DARK_TEXT)
            set_font(p, text, size=8, bold=(col_idx == 4 or col_idx == 0), color=col, align=PP_ALIGN.LEFT)

    # Strategic Advantage Callout Card at bottom
    add_card(s3, Inches(0.6), Inches(4.2), Inches(8.8), Inches(0.85), fill_color=RGBColor(240, 249, 255), line_color=RGBColor(56, 189, 248))
    tb_callout = s3.shapes.add_textbox(Inches(0.75), Inches(4.25), Inches(8.5), Inches(0.75))
    tf_c = tb_callout.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    set_font(p, "THE AIRTEL FULL-STACK MOAT:", size=9.5, bold=True, color=NAVY)
    p2 = tf_c.add_paragraph()
    set_font(p2, "SaaS players lack network infrastructure, and legacy telcos lack digital customer experience. Airtel owns the high-speed pipe (5G AirFiber/Biz Fibre) and bundles critical digital tools (Google Workspace, WhatsApp API, Cloud CCTV) on a SINGLE bill, slashing churn from 15.2% to <6%.", size=8.5, bold=False, color=DARK_TEXT)

    # =========================================================================
    # SLIDE 4: PROPOSED APPROACH — PRODUCT BUNDLING & GENAI ADVISOR
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    s4.shapes.add_picture(inside_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    add_slide_header(s4, "Approach: GenAI Discovery Engine & Rule-Based Bundling")

    # Left Container: GenAI Conversational Advisor
    add_card(s4, Inches(0.6), Inches(1.4), Inches(4.3), Inches(3.6), fill_color=WHITE)
    tb_adv = s4.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(4.0), Inches(3.4))
    tf_adv = tb_adv.text_frame
    tf_adv.word_wrap = True

    p = tf_adv.paragraphs[0]
    set_font(p, "1. CONVERSATIONAL BUSINESS DISCOVERY", size=11, bold=True, color=RED)

    adv_points = [
        ("Consultative Sales Experience in Regional Tongues", "Behaves like an experienced Airtel MSME salesperson. Converses in Hindi, Hinglish, and English via Groq LLaMA 3.3 70B. 1 question at a time (5-25 words)."),
        ("Adaptive 7-Category Needs Assessment", "Extracts business category, employee count, branch count, payment failover needs, CCTV, and cloud tools without technical telecom jargon."),
        ("Deterministic Recommendation Rule Engine", "LLM discovers needs; deterministic 5-factor scoring engine selects bundles from product_catalogue.csv. Kirana stores NEVER receive manufacturing suites."),
        ("Explainable Value & Honest Budget Advice", "Directly explains why a bundle solves their exact pain point (e.g. UPI failover) and alerts if stated budget differs with down-tier alternatives.")
    ]
    for title, desc in adv_points:
        p = tf_adv.add_paragraph()
        p.space_before = Pt(5)
        set_font(p, f"• {title}", size=9, bold=True, color=NAVY)
        p_desc = tf_adv.add_paragraph()
        set_font(p_desc, desc, size=7.8, bold=False, color=DARK_TEXT)

    # Right Container: 4 Hero Bundles & Modular Checkout
    add_card(s4, Inches(5.1), Inches(1.4), Inches(4.3), Inches(3.6), fill_color=LIGHT_BG)
    tb_bnd = s4.shapes.add_textbox(Inches(5.25), Inches(1.5), Inches(4.0), Inches(3.4))
    tf_bnd = tb_bnd.text_frame
    tf_bnd.word_wrap = True

    p = tf_bnd.paragraphs[0]
    set_font(p, "2. 4 HERO BUNDLES & TRANSPARENT 18% GST", size=11, bold=True, color=NAVY)

    bundles = [
        ("Kirana Digital Starter", "Rs 1,999 / mo", "Biz 5G AirFiber 100 + POS 4G Backup + WhatsApp API + UPI Guest Wi-Fi. Solves payment failure crisis in 2-day wireless setup."),
        ("Clinic & Office Suite", "Rs 3,499 / mo", "Biz Fibre 300 + Google Workspace + 1TB Cloud Backup + Secure Wi-Fi. 99.9% uptime for patient, legal & tax files."),
        ("Multi-Site Retail Pro", "Rs 7,999 / mo", "Biz Fibre 1G + SD-WAN + 4x Cloud CCTV + Managed Firewall. Centralized store management across cities."),
        ("Small Manufacturing Suite", "Rs 14,999 / mo", "1:1 Leased Line 100M + Cloud Voice + Telemetry + DDoS Shield. Dedicated industrial ERP connectivity.")
    ]
    for b_name, b_price, b_detail in bundles:
        p = tf_bnd.add_paragraph()
        p.space_before = Pt(4)
        set_font(p, f"{b_name} — {b_price}", size=9, bold=True, color=RED)
        p_det = tf_bnd.add_paragraph()
        set_font(p_det, b_detail, size=7.5, bold=False, color=DARK_TEXT)

    p_mod = tf_bnd.add_paragraph()
    p_mod.space_before = Pt(6)
    set_font(p_mod, "Transparent Pricing: Itemized base, optional add-ons, exact 18% GST, and one-time setup fee with 1-click order creation — ZERO 5-day quote wait!", size=8, bold=True, color=GREEN)

    # =========================================================================
    # SLIDE 5: PROPOSED APPROACH — SMART KYC & DPDP COMPLIANCE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    s5.shapes.add_picture(inside_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    add_slide_header(s5, "Smart KYC: Zero-Friction Verification & DPDP Compliance")

    # 3 Cards for KYC Architecture
    kyc_cards = [
        ("1. Instant Registry APIs\n(Zero Manual Typing)", 
         [("Mock GSTIN Registry API", "Validates 15-char format (with 'X' check). Auto-populates Legal Name, Trade Name, Registered Address, and Active/Cancelled status in <500ms."),
          ("Mock Udyam Registry API", "Validates 'UDYAM-XX-00-XXXXXXX' structure. Auto-verifies MSME enterprise classification (Micro, Small, Medium)."),
          ("Direct Value", "Eliminates 94 dropouts caused by missing or misplaced registration documents.")],
         WHITE),
        ("2. Cross-Field Validation & Exceptions\n(Actionable Error Resolution)", 
         [("Deterministic 90-Day Rule", "Strict benchmark: 15-Jul-2026. Flags K05 (186d old) & K11 (257d old) as expired; approves K02 (54d old) & K03 (46d old)."),
          ("Resolution Anomaly Catchers", "Detects low-res scans (K04 blur @ 38.5% confidence) & triggers re-upload prompt with 4-corner guide."),
          ("Bilingual Exception Guidance", "Never displays 'KYC Failed'. Explains exact issue in English & Hindi (Cancelled GSTIN, old bill, or address mismatch).")],
         WHITE),
        ("3. DPDP Act, 2023 Compliance\n(Privacy-by-Design)", 
         [("Explicit Bilingual Consent", "Granular, unbundled consent modal in the customer's language before camera/document capture."),
          ("Strict Data Minimization", "Collects solely statutory DoT telecom parameters. Zero hoarding of bank statements or unrelated financial files."),
          ("PII Masking & Purging", "PAN and Aadhaar numbers masked in logs/UI (e.g. 27AAAAA****1ZX). Raw documents encrypted at rest (AES-256) and purged post-verification.")],
         RGBColor(240, 253, 244))
    ]
    for idx, (c_title, c_items, bg_c) in enumerate(kyc_cards):
        c_x = Inches(0.6 + idx * 2.95)
        add_card(s5, c_x, Inches(1.4), Inches(2.9), Inches(3.6), fill_color=bg_c, line_color=RED if idx==2 else BORDER_COL)
        tb_k = s5.shapes.add_textbox(c_x + Inches(0.12), Inches(1.5), Inches(2.65), Inches(3.4))
        tf_k = tb_k.text_frame
        tf_k.word_wrap = True
        p = tf_k.paragraphs[0]
        set_font(p, c_title, size=10, bold=True, color=NAVY)

        for item_t, item_d in c_items:
            p = tf_k.add_paragraph()
            p.space_before = Pt(6)
            set_font(p, f"• {item_t}", size=8.5, bold=True, color=RED if idx==2 else NAVY)
            p_sub = tf_k.add_paragraph()
            set_font(p_sub, item_d, size=7.5, bold=False, color=DARK_TEXT)

    # =========================================================================
    # SLIDE 6: ASSISTED PARTNER ECOSYSTEM & AI QUOTE RECOVERY ENGINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    s6.shapes.add_picture(inside_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    add_slide_header(s6, "Assisted Partner Ecosystem & AI Quote Recovery Engine")

    # Left Container: AI Quote Recovery Engine (Phase 3)
    add_card(s6, Inches(0.6), Inches(1.4), Inches(4.3), Inches(3.6), fill_color=WHITE)
    tb_arch = s6.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(4.0), Inches(3.4))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p = tf_arch.paragraphs[0]
    set_font(p, "1. AI QUOTE RECOVERY ENGINE (1,113 LEADS)", size=11, bold=True, color=NAVY)

    arch_layers = [
        ("8-Class Objection Classifier & Priority Scoring", "Analyzes abandonments across price, competitor, complexity, missing features, and SLA. Dynamic priority score (0-100) ranks high-value recoverable deals."),
        ("Down-Tiering & Catalogue Add-on Solver", "Detects budget mismatches and suggests viable alternative bundles (e.g. ₹1,999 Kirana plan) or matching add-ons (Cloud CCTV, Static IP) with single-click quotation update."),
        ("Contextual AI Outreach Generator", "Generates empathetic, natural WhatsApp and email drafts in Hindi and English with plain-language talking points for field and desk agents."),
        ("Secure Re-Entry Tokens & DPDP Opt-Out", "Allows merchants to resume saved quotes via 1-click expiring links. Enforces explicit DPDP 2023 opt-out with permanent communication suppression.")
    ]
    for layer, desc in arch_layers:
        p = tf_arch.add_paragraph()
        p.space_before = Pt(5)
        set_font(p, f"• {layer}", size=8.8, bold=True, color=RED)
        p_d = tf_arch.add_paragraph()
        set_font(p_d, desc, size=7.8, bold=False, color=DARK_TEXT)

    # Right Container: Channel Partner Ecosystem (Phase 4)
    add_card(s6, Inches(5.1), Inches(1.4), Inches(4.3), Inches(3.6), fill_color=LIGHT_BG)
    tb_part = s6.shapes.add_textbox(Inches(5.25), Inches(1.5), Inches(4.0), Inches(3.4))
    tf_part = tb_part.text_frame
    tf_part.word_wrap = True

    p = tf_part.paragraphs[0]
    set_font(p, "2. ASSISTED PARTNER ECOSYSTEM & COMMISSIONS", size=11, bold=True, color=RED)

    partner_points = [
        ("Dual-Aspect Assisted Tablet Mode", "Empowers Airtel field reps and local partners on visits: Customer Canvas (left 60%) for simple discovery + Private Partner AI Sales Co-Pilot (right 40%)."),
        ("Consultative Coaching & Hindi Field Prompts", "Co-pilot generates live consultative questions in Hindi/Hinglish, handles price/complexity rebuttals, and checks satisfied vs unmet needs."),
        ("Branded Dynamic QR & 30-Day First-Touch Lock", "Offline SVG QR codes and referral links attribute merchants with 30-day first-touch protection, preventing partner commission conflict."),
        ("Activation-Gated Ledger (Rs 1,500 Parameter)", "Zero payout risk: commission is stamped 'pending' upon order, unlocked to 'eligible' strictly on Step 5 installation activation, with admin RBAC.")
    ]
    for p_title, p_desc in partner_points:
        p = tf_part.add_paragraph()
        p.space_before = Pt(5)
        set_font(p, f"• {p_title}", size=8.8, bold=True, color=NAVY)
        p_d = tf_part.add_paragraph()
        set_font(p_d, p_desc, size=7.8, bold=False, color=DARK_TEXT)

    # =========================================================================
    # SLIDE 7: PROJECTED IMPACT, UNIT ECONOMICS & ROLLOUT ROADMAP
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    s7.shapes.add_picture(inside_bg, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    add_slide_header(s7, "Business Impact, Unit Economics & Phased Rollout Roadmap")

    # Top: 4 Key Metric Badges
    top_metrics = [
        ("Lead Conversion", "7.36% -> 25.0%", "+240% lift via pricing & recovery", GREEN),
        ("Activation TAT", "17.6d -> 2.8 Days", "-84% via Smart KYC & pre-feasibility", RED),
        ("Blended CAC", "Rs 15,000 -> Rs 6,850", "-54.3% via digital self-serve", GOLD),
        ("Chase Calls", "3.01 -> 0.2 Calls", "-93% via proactive milestone tracking", NAVY)
    ]
    for idx, (m_tit, m_val, m_desc, col) in enumerate(top_metrics):
        b_x = Inches(0.6 + idx * 2.22)
        add_card(s7, b_x, Inches(1.4), Inches(2.1), Inches(1.05), fill_color=WHITE, line_color=col)
        tb_m = s7.shapes.add_textbox(b_x + Inches(0.08), Inches(1.45), Inches(1.94), Inches(0.95))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p = tf_m.paragraphs[0]
        set_font(p, m_tit, size=9, bold=True, color=GRAY_TEXT)
        p2 = tf_m.add_paragraph()
        set_font(p2, m_val, size=12, bold=True, color=col)
        p3 = tf_m.add_paragraph()
        set_font(p3, m_desc, size=7.5, bold=False, color=DARK_TEXT)

    # Bottom Left: Unit Economics Card (4.3 inches wide)
    add_card(s7, Inches(0.6), Inches(2.6), Inches(4.3), Inches(2.4), fill_color=WHITE)
    tb_ue = s7.shapes.add_textbox(Inches(0.75), Inches(2.65), Inches(4.0), Inches(2.3))
    tf_ue = tb_ue.text_frame
    tf_ue.word_wrap = True

    p = tf_ue.paragraphs[0]
    set_font(p, "TRANSFORMATIVE UNIT ECONOMICS", size=10.5, bold=True, color=NAVY)

    ue_points = [
        ("CAC Payback Period:", "Drops from 6.0 months (Rs 15,000 / Rs 2,500 ARPU) to 1.8 months (Rs 6,850 CAC / Rs 3,850 blended ARPU)."),
        ("LTV / CAC Ratio:", "Jumps from 2.1x to 9.4x driven by 4 hero bundles and churn reduction from 15.2% to <5%."),
        ("Incremental Annual Revenue:", "Capturing 940 activations vs 368 baseline yields +Rs 2.64 Crore incremental annualized B2B revenue.")
    ]
    for u_t, u_d in ue_points:
        p = tf_ue.add_paragraph()
        p.space_before = Pt(4)
        set_font(p, f"• {u_t}", size=8.5, bold=True, color=RED)
        p_sub = tf_ue.add_paragraph()
        set_font(p_sub, u_d, size=8, bold=False, color=DARK_TEXT)

    # Bottom Right: 3-Phase Rollout Roadmap (4.3 inches wide)
    add_card(s7, Inches(5.1), Inches(2.6), Inches(4.3), Inches(2.4), fill_color=LIGHT_BG)
    tb_rm = s7.shapes.add_textbox(Inches(5.25), Inches(2.65), Inches(4.0), Inches(2.3))
    tf_rm = tb_rm.text_frame
    tf_rm.word_wrap = True

    p = tf_rm.paragraphs[0]
    set_font(p, "3-PHASE EXECUTION ROADMAP", size=10.5, bold=True, color=RED)

    roadmap_steps = [
        ("Operations Command Centre", "Predictive risk engine monitors bundle SLAs (Kirana 2d, Clinic 3d, Pro 7d, Mfg 14d) with unified exception action queue."),
        ("Phase 1: Pilot Launch (M1-M3)", "Deploy Web & WhatsApp advisor in 5 top Tier 1 cities (NCR, Mumbai, Bengaluru, Hyderabad, Chennai) targeting Kirana & Clinic segments."),
        ("Phase 2 & 3: Scale & Expand (M4-M12)", "Scale to 25 Tier 2 industrial hubs with 5,000 assisted partners and AI what-if scenario simulations.")
    ]
    for r_t, r_d in roadmap_steps:
        p = tf_rm.add_paragraph()
        p.space_before = Pt(4)
        set_font(p, f"• {r_t}", size=8.5, bold=True, color=NAVY)
        p_sub = tf_rm.add_paragraph()
        set_font(p_sub, r_d, size=8, bold=False, color=DARK_TEXT)

    # Save presentation
    os.makedirs(os.path.dirname(output_pptx), exist_ok=True)
    prs.save(output_pptx)
    print(f"Presentation saved successfully to: {output_pptx}")

if __name__ == "__main__":
    out_file = r"E:\Airtel\submission\Halo_Thapar.pptx"
    create_deck(out_file)
