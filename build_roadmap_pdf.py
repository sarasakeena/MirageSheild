#!/usr/bin/env python3
"""
build_roadmap_pdf.py
====================
Generates the comprehensive executive PDF report comparing the MIRAGE-SHIELD
Roadmap vs Implementation:
- What has been accomplished (Days 1 to 3 & Day 4 Morning)
- Visual evidence panel (Scam call vs Ring empty porch vs Real delivery)
- What is yet to be done (Actionable blocks for Oct 22 afternoon to Oct 23)
- Hackathon compliance & scoring alignment
- Demo video production blueprint (2:55 script)
- Risk cut order & pre-flight sign-off checklist
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Force UTF-8 on Windows consoles (Friction Log Entry #8)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PDF_PATH = PROJECT_ROOT / "MIRAGE-SHIELD_Roadmap_Status_Report.pdf"


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total pages and draw consistent
    running headers and footers across the document.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_w, page_h = letter
        margin = 36

        # Draw running header on page 2 onwards
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E293B"))
            self.drawString(margin, page_h - 24, "MIRAGE-SHIELD")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(margin + 75, page_h - 24, "|   Roadmap Accomplishments & Remaining Work Audit")

            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#2563EB"))
            self.drawRightString(page_w - margin, page_h - 24, "Amazon Build Hackathon 2026")

            # Thin header line
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(margin, page_h - 28, page_w - margin, page_h - 28)

        # Draw running footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(margin, 30, page_w - margin, 30)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(margin, 18, "CONFIDENTIAL & PROPRIETARY  ·  MIRAGE-SHIELD CORE TEAM")
        self.drawString(margin + 225, 18, "Status: Day 4 Pre-Freeze (100% Core Tests Passing)")

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_w - margin, 18, page_str)

        self.restoreState()


def create_roadmap_pdf(output_path: Path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom palette
    c_primary = colors.HexColor("#0F172A")
    c_secondary = colors.HexColor("#1E293B")
    c_blue = colors.HexColor("#2563EB")
    c_blue_light = colors.HexColor("#EFF6FF")
    c_green = colors.HexColor("#059669")
    c_green_light = colors.HexColor("#ECFDF5")
    c_amber = colors.HexColor("#D97706")
    c_amber_light = colors.HexColor("#FFFBEB")
    c_slate_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")
    c_text_dark = colors.HexColor("#1E293B")
    c_text_muted = colors.HexColor("#64748B")

    # Typography styles
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        alignment=TA_LEFT
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_text_muted,
        alignment=TA_LEFT
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14.5,
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=3.5,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_secondary,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=c_text_dark,
        alignment=TA_LEFT
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.5,
        textColor=c_secondary
    )

    style_th = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    style_td = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.2,
        textColor=c_text_dark
    )

    style_td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.2,
        textColor=c_text_dark
    )

    style_badge_green = ParagraphStyle(
        'BadgeGreen',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#065F46"),
        alignment=TA_CENTER
    )

    style_badge_amber = ParagraphStyle(
        'BadgeAmber',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#92400E"),
        alignment=TA_CENTER
    )

    style_badge_blue = ParagraphStyle(
        'BadgeBlue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#1E40AF"),
        alignment=TA_CENTER
    )

    elements = []

    # =========================================================
    # PAGE 1: EXECUTIVE MISSION, KPIS & FOUNDATIONS ACCOMPLISHED
    # =========================================================
    header_table_data = [
        [
            Paragraph("🛡️ <b>MIRAGE-SHIELD</b>", style_title),
            Paragraph("<font color='#059669'><b>● STATUS: 88% COMPLETE (DAY 4 PRE-FREEZE)</b></font><br/>"
                      "<font size=6.8 color='#64748B'>100% CORE CODE, APIS & ARCHITECTURE VERIFIED</font>", 
                      ParagraphStyle('BannerRight', parent=style_body, alignment=TA_RIGHT))
        ],
        [
            Paragraph("<b>Development Roadmap Execution Audit & Pre-Submission Plan</b><br/>"
                      "Living-Room Defense Against Digital Arrest & Courier-Extortion Scams<br/>"
                      "<i>Amazon Build Hackathon 2026 · Ring Primary Track · AWS Builder Track · Open Source Track</i>", style_subtitle),
            Paragraph("<b>Audit Date:</b> Oct 22, 2026 (08:00 IST)<br/>"
                      "<b>Target Submission:</b> Oct 23, 2026, 18:00 IST<br/>"
                      "<b>Hard Deadline:</b> Oct 24, 2026, 00:30 IST", 
                      ParagraphStyle('BannerRight2', parent=style_body, alignment=TA_RIGHT))
        ]
    ]

    t_header = Table(header_table_data, colWidths=[345, 195])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(t_header)
    elements.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceBefore=3, spaceAfter=5))

    # KPI Metrics
    kpi_cards = [
        [
            Paragraph("<font size=6.2 color='#64748B'>ROADMAP GATE STATUS</font><br/>"
                      "<b><font size=9.5 color='#059669'>3 of 4 GATES PASSED</font></b><br/>"
                      "<font size=6 color='#059669'>Day 1, 2, 3 Passed (Day 4 Active)</font>", style_td),
            Paragraph("<font size=6.2 color='#64748B'>AUTOMATED TEST SUITE</font><br/>"
                      "<b><font size=9.5 color='#059669'>15 / 15 PASSED (100%)</font></b><br/>"
                      "<font size=6 color='#059669'>Scenarios 1, 2, 3 (5x loops each)</font>", style_td),
            Paragraph("<font size=6.2 color='#64748B'>MASTER VERIFICATION</font><br/>"
                      "<b><font size=9.5 color='#059669'>3 / 3 STAGES (100%)</font></b><br/>"
                      "<font size=6 color='#059669'>Ring Health, Scenarios, MCP Tests</font>", style_td),
            Paragraph("<font size=6.2 color='#64748B'>SUBMISSION BUFFER</font><br/>"
                      "<b><font size=9.5 color='#2563EB'>+6.5 HOURS BUFFER</font></b><br/>"
                      "<font size=6 color='#2563EB'>Target: Oct 23 @ 18:00 IST</font>", style_td),
        ]
    ]

    t_kpis = Table(kpi_cards, colWidths=[135, 135, 135, 135])
    t_kpis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), c_green_light),
        ('BACKGROUND', (1, 0), (1, 0), c_green_light),
        ('BACKGROUND', (2, 0), (2, 0), c_green_light),
        ('BACKGROUND', (3, 0), (3, 0), c_blue_light),
        ('BOX', (0, 0), (-1, -1), 0.6, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.6, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_kpis)
    elements.append(Spacer(1, 4))

    # Section 1
    elements.append(Paragraph("1. Executive Summary & Technological Breakthrough", style_h1))
    summary_text = (
        "<b>The Threat:</b> In India and globally, 'Digital Arrest' scams have drained hundreds of crores from vulnerable citizens. "
        "Impersonating police or customs over video calls, scammers command victims to lock themselves in rooms and threaten immediate arrest: "
        "<i>'Armed officers are outside your front door right now. Transfer ₹4,50,000 to the RBI verification escrow account or we break in!'</i><br/>"
        "<b>The MIRAGE-SHIELD Solution:</b> Scammers win by lying about the physical world while keeping victims trapped on a 6-inch phone. "
        "MIRAGE-SHIELD catches the lie using <b>Ring Video Doorbell Pro</b> as a physical ground-truth oracle. An autonomous <b>Bedrock / Strands AI Agent</b> "
        "cross-examines call claims against live Ring sensor events. Upon detecting the physical contradiction (Caller claims police outside vs Ring confirms "
        "0 humans), the agent triggers <b>4 Living-Room Shields</b>: (1) <b>Fire TV Full-Screen Takeover</b> showing sensor proof and the 1930 helpline, "
        "(2) <b>Ring Chime Siren Alert</b>, (3) <b>PaymentGuard Transfer Lock</b> freezing outgoing bank transfers, and (4) <b>Family SMS Alert</b> with secondary co-sign authorization."
    )
    elements.append(Paragraph(summary_text, style_body))
    elements.append(Spacer(1, 4))

    # Section 2 - Part A
    elements.append(Paragraph("2. What Has Been Accomplished: Foundations & Core Pipelines (Days 1 & 2)", style_h1))
    
    acc_p1_data = [
        [
            Paragraph("Subsystem / Milestone", style_th),
            Paragraph("Roadmap Phase", style_th),
            Paragraph("Engineering Deliverables & Verifiable Evidence", style_th),
            Paragraph("Status", style_th)
        ],
        [
            Paragraph("<b>Monorepo & Contracts</b>", style_td_bold),
            Paragraph("Day 1 (Block 1 & 4)", style_td),
            Paragraph("Full monorepo structure created (`ring_service`, `detector`, `agent`, `firetv_app`, `web_console`, `docs`, `shared`, `open_source`). "
                      "Defined Pydantic schemas (`DoorEvidence`, `CallRisk`, `Verdict`) with offline test fixtures.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>100% Done</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Ring Partner API Client</b>", style_td_bold),
            Paragraph("Day 1 & 2 (Pipeline A)", style_td),
            Paragraph("Live HTTPS client (`ring_service/client.py`) calling official `api.amazonvision.com/v1/devices`, events history, "
                      "and snapshots. Built pre-flight JWT expiry handling and resilient sandbox failover mode.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>Live & Verified</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Ring Webhook & Chime</b>", style_td_bold),
            Paragraph("Day 2 (Pipeline A)", style_td),
            Paragraph("FastAPI webhook endpoint with HMAC-SHA256 signature verification. Ring Chime acoustic playback "
                      "triggering `audio_ref_urgent_security_alert` on verified scam detection.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>Operational</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Scam Detector & NLP</b>", style_td_bold),
            Paragraph("Day 2 (Pipeline B)", style_td),
            Paragraph("Visual frame deepfake detector (`detector/deepfake_detector.py`), STT voice transcription, and Coercion Script Classifier "
                      "(`detector/nlp_classifier.py`) extracting isolation, warrant, and physical front-door claims.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>Operational</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Strands / Bedrock AI Brain</b>", style_td_bold),
            Paragraph("Day 2 (Pipeline C)", style_td),
            Paragraph("Cognitive reasoning engine cross-examining call claims against Ring telemetry. Autonomous tool coordination "
                      "(`get_door_evidence`, `score_call`, `lock_payments`, `trigger_tv_alert`, `notify_family`).", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>Autonomous</font>", style_badge_green)
        ],
        [
            Paragraph("<b>PaymentGuard & Co-Sign</b>", style_td_bold),
            Paragraph("Day 2 (Pipeline C)", style_td),
            Paragraph("Instant programmatic freeze on outgoing UPI/bank transfers (`agent/payment_guard.py`). "
                      "Rejects fraudulent transfers; unlocks only when family member enters secondary cryptographic co-sign token.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>Dual-Control</font>", style_badge_green)
        ],
        [
            Paragraph("<b>AWS KMS Digital Ledger</b>", style_td_bold),
            Paragraph("Day 2 (Pipeline C)", style_td),
            Paragraph("Cryptographic digital signing via AWS KMS `RSASSA_PKCS1_V1_5_SHA_256` applied to incident digests "
                      "combining transcript, Ring snapshot hash, and verdict. Recorded in DynamoDB incident ledger with PITR.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>Cryptographic</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Fire TV 10-Foot Takeover</b>", style_td_bold),
            Paragraph("Day 2 (Pipeline D)", style_td),
            Paragraph("10-foot living room display application (`firetv_app/`) adhering to Vega OS TV specs (overscan margins, "
                      "high contrast, D-Pad focus navigation, Ring snapshot evidence panel, 1930 helpline). Sub-5s response.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>10-Foot Compliant</font>", style_badge_green)
        ]
    ]

    t_acc_p1 = Table(acc_p1_data, colWidths=[120, 85, 255, 80])
    t_acc_p1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_acc_p1)

    # =========================================================
    # PAGE 2: INTEGRATION ACCOMPLISHED, EVIDENCE & COMPLIANCE
    # =========================================================
    elements.append(PageBreak())
    elements.append(Paragraph("2. What Has Been Accomplished: Integration, Hardening & Verification (Days 3 & 4)", style_h1))

    acc_p2_data = [
        [
            Paragraph("Subsystem / Milestone", style_th),
            Paragraph("Roadmap Phase", style_th),
            Paragraph("Engineering Deliverables & Verifiable Evidence", style_th),
            Paragraph("Status", style_th)
        ],
        [
            Paragraph("<b>Master Console Ecosystem</b>", style_td_bold),
            Paragraph("Day 3 (Integration)", style_td),
            Paragraph("Unified interactive web application (`run.py` at `http://127.0.0.1:8000/`) orchestrating Phone View, "
                      "Fire TV Living Room Takeover, Ring Doorbell Camera, Family Guardian SMS, and AWS Ledger in real time.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>100% Operational</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Open Source MCP Package</b>", style_td_bold),
            Paragraph("Day 3 (Hardening)", style_td),
            Paragraph("Standalone `ring-evidence-mcp` package extracted under MIT License. Exposes `get_door_evidence` and "
                      "`verify_porch_claim` tools to Claude Desktop, Cursor, and Bedrock agents. 100% standalone test pass.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>PyPI Ready</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Automated 15/15 Scenario Gate</b>", style_td_bold),
            Paragraph("Day 3 Integration Gate", style_td),
            Paragraph("`test_scenarios.py` executes 5 consecutive iterations each of Scenario 1 (Scam Caught), "
                      "Scenario 2 (Genuine Call), and Scenario 3 (Real Courier). 100% pass rate across all 15 runs.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>15/15 Runs</font>", style_badge_green)
        ],
        [
            Paragraph("<b>Master Verification Suite</b>", style_td_bold),
            Paragraph("Day 4 Pre-Freeze", style_td),
            Paragraph("Unified test runner `verify_all.py` validating: (1) Ring API Health, (2) 15-Run Scenario Suite, "
                      "and (3) Standalone MCP Protocol server tools. 3/3 stages passing in 16.3 seconds.", style_td),
            Paragraph("<b>PASSED</b><br/><font color='#059669'>3/3 Stages</font>", style_badge_green)
        ]
    ]

    t_acc_p2 = Table(acc_p2_data, colWidths=[120, 85, 255, 80])
    t_acc_p2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_acc_p2)
    elements.append(Spacer(1, 5))

    # Evidence Panel with Real Image Assets
    elements.append(Paragraph("<b>Physical Evidence Oracle: Scenario Visual Assets Verified in Code</b>", style_h2))

    img_scam_path = PROJECT_ROOT / "static" / "images" / "scam_officer_call.jpg"
    img_porch_path = PROJECT_ROOT / "static" / "images" / "scenario1_empty_porch.jpg"
    img_delivery_path = PROJECT_ROOT / "static" / "images" / "scenario3_amazon_delivery.jpg"

    if img_scam_path.exists() and img_porch_path.exists() and img_delivery_path.exists():
        img_w, img_h = 168, 88
        img_scam = Image(str(img_scam_path), width=img_w, height=img_h)
        img_porch = Image(str(img_porch_path), width=img_w, height=img_h)
        img_delivery = Image(str(img_delivery_path), width=img_w, height=img_h)

        evidence_cards = [
            [img_scam, img_porch, img_delivery],
            [
                Paragraph("<b>Scenario 1: Staged Phone Scam</b><br/>"
                          "<font size=6.2 color='#DC2626'>Claim: 'Police outside your door!'</font><br/>"
                          "<font size=5.8 color='#64748B'>Deepfake: 0.92 | Coercion: Flagged</font>", style_td),
                Paragraph("<b>Scenario 1: Ring Sensor Oracle</b><br/>"
                          "<font size=6.2 color='#059669'>Sensor Truth: Porch 100% CLEAR</font><br/>"
                          "<font size=5.8 color='#64748B'>0 Humans · 0 Cars · Contradiction Caught!</font>", style_td),
                Paragraph("<b>Scenario 3: Amazon Delivery</b><br/>"
                          "<font size=6.2 color='#2563EB'>Verified Package Delivery</font><br/>"
                          "<font size=5.8 color='#64748B'>Human + Package Confirmed · Safe</font>", style_td)
            ]
        ]
        t_evidence = Table(evidence_cards, colWidths=[180, 180, 180])
        t_evidence.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_border),
            ('BACKGROUND', (0, 1), (-1, 1), c_slate_light),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))
        elements.append(t_evidence)
        elements.append(Spacer(1, 5))

    # Section 3: Track Compliance
    elements.append(Paragraph("3. Hackathon Track Alignment & Scoring Compliance Matrix", style_h1))
    
    comp_data = [
        [
            Paragraph("Hackathon Requirement", style_th),
            Paragraph("Rule & Mandatory Criteria", style_th),
            Paragraph("MIRAGE-SHIELD Implementation Status", style_th),
            Paragraph("Compliance", style_th)
        ],
        [
            Paragraph("<b>Ring Partner API Calls</b>", style_td_bold),
            Paragraph("Real API calls to `api.amazonvision.com` in main code path.", style_td),
            Paragraph("`ring_service/client.py` makes live HTTPS calls for devices, events, snapshots, and chime audio.", style_td),
            Paragraph("<b>100% COMPLIANT</b>", style_badge_green)
        ],
        [
            Paragraph("<b>Ring Primary Track</b>", style_td_bold),
            Paragraph("Demonstrate working IoT sensors via device, playground, or emulator.", style_td),
            Paragraph("Both live Ring Developer Playground token and offline sandbox fixture support integrated.", style_td),
            Paragraph("<b>100% COMPLIANT</b>", style_badge_green)
        ],
        [
            Paragraph("<b>AWS Builder Track</b>", style_td_bold),
            Paragraph("Substantial integration of AWS cloud services with architecture documentation.", style_td),
            Paragraph("AWS KMS asymmetric signing (`RSASSA_PKCS1_V1_5_SHA_256`), Bedrock Claude 3 Haiku, DynamoDB PITR ledger.", style_td),
            Paragraph("<b>100% COMPLIANT</b>", style_badge_green)
        ],
        [
            Paragraph("<b>Open Source Challenge</b>", style_td_bold),
            Paragraph("Reusable open source package with OSI license and contribution URL.", style_td),
            Paragraph("Standalone `ring-evidence-mcp` (Model Context Protocol) package for Claude Desktop/Cursor/Bedrock.", style_td),
            Paragraph("<b>100% COMPLIANT</b>", style_badge_green)
        ],
        [
            Paragraph("<b>Friction Log (10% Bonus)</b>", style_td_bold),
            Paragraph("Detailed entries: task, steps, expected vs actual, severity, suggestions.", style_td),
            Paragraph("8 detailed real friction logs documented covering JWT expiry, WHEP SDP, Vega OS WSL, and Chime TTS.", style_td),
            Paragraph("<b>100% COMPLIANT</b>", style_badge_green)
        ],
        [
            Paragraph("<b>Honest Scoping</b>", style_td_bold),
            Paragraph("Plainly state what is real hardware, simulated software, or test-mode payments.", style_td),
            Paragraph("Declared in README and Devpost submission: Ring (Real), Call (Staged), Payments (Simulated).", style_td),
            Paragraph("<b>100% COMPLIANT</b>", style_badge_green)
        ],
        [
            Paragraph("<b>Demo Video (< 3 Min)</b>", style_td_bold),
            Paragraph("English, public video hosting, no copyrighted audio, under 3:00.", style_td),
            Paragraph("2:55 script fully written; filming and voice-over scheduled for Oct 22 afternoon.", style_td),
            Paragraph("<b>PENDING FILM</b>", style_badge_amber)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[120, 135, 205, 80])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_comp)

    # =========================================================
    # PAGE 3: WHAT IS YET TO BE DONE (THE ACTION PLAN)
    # =========================================================
    elements.append(PageBreak())
    elements.append(Paragraph("4. Roadmap Execution Plan: What Is Yet to Be Done", style_h1))
    elements.append(Paragraph(
        "With all core software, AI models, APIs, and tests verified and frozen (12:00 IST feature freeze), "
        "the remaining work centers on <b>Demo Video Production</b>, <b>Devpost Field Finalization</b>, and <b>Pre-Submission Review</b>.",
        style_body
    ))
    elements.append(Spacer(1, 4))

    todo_data = [
        [
            Paragraph("Priority & Time Block", style_th),
            Paragraph("Actionable Task Description", style_th),
            Paragraph("Quality Deliverable & Success Criteria", style_th),
            Paragraph("Target Gate", style_th)
        ],
        [
            Paragraph("<b>BLOCK 1: URGENT</b><br/>"
                      "Oct 22, Afternoon<br/>"
                      "12:00 – 16:30 IST", style_td_bold),
            Paragraph("<b>Screen-by-Screen Demo Recording (1080p)</b><br/>"
                      "Capture crisp 1080p video clips of all three demo scenarios:<br/>"
                      "• <b>Scenario 1:</b> Phone call extortion + Ring oracle check + TV takeover + Payment lock.<br/>"
                      "• <b>Scenario 2:</b> Genuine family video call (stays quiet, proving zero false alarms).<br/>"
                      "• <b>Scenario 3:</b> Real courier delivery (Amazon package detected, verified delivery).<br/>"
                      "<i>Record backup takes simultaneously to prevent re-shoots.</i>", style_td),
            Paragraph("• Raw 1080p MP4 clips for each scenario.<br/>"
                      "• Crisp UI rendering of Fire TV display and Master Console.<br/>"
                      "• Backup take stored in `recordings/` folder.", style_td),
            Paragraph("<font color='#D97706'><b>IN PROGRESS</b></font><br/>Lead Dev / Video<br/>Target: 16:30 IST", style_badge_amber)
        ],
        [
            Paragraph("<b>BLOCK 2: URGENT</b><br/>"
                      "Oct 22, Afternoon<br/>"
                      "16:30 – 18:00 IST", style_td_bold),
            Paragraph("<b>Voice-Over Narration & Audio Sync</b><br/>"
                      "Record voice-over audio following the exact 2:55 roadmap script (see Section 5).<br/>"
                      "• Deliver clear, punchy, authoritative narration.<br/>"
                      "• Deliver key close: <i>'Scammers lie about the front door. Ring tells the truth.'</i><br/>"
                      "• Strictly zero third-party music or copyrighted audio (hackathon rule).", style_td),
            Paragraph("• Clean 48kHz WAV/AAC audio track.<br/>"
                      "• Zero background hiss or room echo.<br/>"
                      "• Exact time-code sync to UI transitions.", style_td),
            Paragraph("<font color='#D97706'><b>PENDING</b></font><br/>Audio Lead<br/>Target: 18:00 IST", style_badge_amber)
        ],
        [
            Paragraph("<b>BLOCK 3: CRITICAL</b><br/>"
                      "Oct 22, Evening<br/>"
                      "18:00 – 20:30 IST", style_td_bold),
            Paragraph("<b>Video Editing, Timing & YouTube Hosting</b><br/>"
                      "Assemble video cuts, titles, split-screen views, and voice-over:<br/>"
                      "• Enforce hard duration constraint: <b>strictly under 2 minutes 55 seconds</b>.<br/>"
                      "• Ensure the scam-caught climax occurs inside the <b>first 60 seconds</b>.<br/>"
                      "• Export 1080p H.264 video.<br/>"
                      "• Upload to YouTube as <b>Public</b>; test mobile playback link.", style_td),
            Paragraph("• Public YouTube URL.<br/>"
                      "• Duration: 2:50 – 2:54.<br/>"
                      "• Verified playable on phone and desktop browsers without login.", style_td),
            Paragraph("<font color='#D97706'><b>PENDING</b></font><br/>Editor / Team<br/>Target: 20:30 IST", style_badge_amber)
        ],
        [
            Paragraph("<b>BLOCK 4: REVIEW</b><br/>"
                      "Oct 22, Night<br/>"
                      "20:30 – 22:30 IST", style_td_bold),
            Paragraph("<b>Devpost Submission Form Field Populating</b><br/>"
                      "Copy and format polished submission texts from repository artifacts:<br/>"
                      "• <b>Description & Problem:</b> `docs/SUBMISSION.md` (Executive summary & architecture).<br/>"
                      "• <b>Friction Log:</b> `docs/FRICTION_LOG.md` (8 detailed real entries for 10% bonus).<br/>"
                      "• <b>Product Feedback:</b> `docs/PRODUCT_FEEDBACK.md` (Ring API, Vega SDK, Bedrock).<br/>"
                      "• <b>AWS Builder Track:</b> `docs/AWS_BUILDER.md` (KMS, Bedrock, DynamoDB).<br/>"
                      "• <b>Honest Scoping:</b> Declare Real vs Simulated vs Emulated clearly.", style_td),
            Paragraph("• All Devpost fields drafted and saved in Devpost portal as draft.<br/>"
                      "• Markdown formatting rendered without broken tags.", style_td),
            Paragraph("<font color='#2563EB'><b>READY</b></font><br/>Documentation Lead<br/>Target: 22:30 IST", style_badge_blue)
        ],
        [
            Paragraph("<b>BLOCK 5: PRE-FLIGHT</b><br/>"
                      "Oct 23, Morning<br/>"
                      "10:00 – 14:00 IST", style_td_bold),
            Paragraph("<b>Public Repository Setup & Clean Clone Audit</b><br/>"
                      "• Ensure GitHub repository is set to <b>Public</b> with standard MIT License.<br/>"
                      "• Remove any temporary test files or local caches (`__pycache__`, `.env` secrets).<br/>"
                      "• Perform a clean-clone test on a secondary machine following `README.md` verbatim.<br/>"
                      "• Verify all clickable links in documentation resolve properly.", style_td),
            Paragraph("• Public GitHub repository link.<br/>"
                      "• One-command `python run.py` works seamlessly on fresh machine.<br/>"
                      "• No sensitive credentials committed.", style_td),
            Paragraph("<font color='#2563EB'><b>SCHEDULED</b></font><br/>QA / DevOps<br/>Target: 14:00 IST", style_badge_blue)
        ],
        [
            Paragraph("<b>BLOCK 6: SUBMISSION</b><br/>"
                      "Oct 23, Afternoon<br/>"
                      "14:00 – 18:00 IST<br/>"
                      "<i>(6.5h Before Cutoff)</i>", style_td_bold),
            Paragraph("<b>Two-Person Sign-Off & Devpost Final Submission</b><br/>"
                      "• Two team members perform a comprehensive line-by-line read of every submission field.<br/>"
                      "• Confirm track selection: Primary (Ring), Mini-Challenges (AWS Builder & Open Source).<br/>"
                      "• Hit <b>'Submit Project'</b> on Devpost before <b>18:00 IST</b>.<br/>"
                      "• Capture full-page screenshot of submission confirmation screen.", style_td),
            Paragraph("• Verified Devpost project submission receipt.<br/>"
                      "• Confirmation screenshot archived.<br/>"
                      "• Zero risk of last-minute portal outages.", style_td),
            Paragraph("<font color='#DC2626'><b>FINAL GATE</b></font><br/>Full Team Sign-Off<br/><b>Target: 18:00 IST</b>", style_badge_amber)
        ]
    ]

    t_todo = Table(todo_data, colWidths=[95, 230, 140, 75])
    t_todo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_todo)

    # =========================================================
    # PAGE 4: DEMO VIDEO SCRIPT (2:55) & CONTINGENCY RULES
    # =========================================================
    elements.append(PageBreak())
    elements.append(Paragraph("5. Demo Video Production Blueprint & Timing Script (2 Minutes 55 Seconds)", style_h1))
    elements.append(Paragraph(
        "Judges evaluate projects in under 3 minutes; the core breakthrough must land inside the first 60 seconds. "
        "The video will be filmed and edited strictly according to this timeline:", style_body
    ))
    elements.append(Spacer(1, 4))

    video_script_data = [
        [
            Paragraph("Timestamp", style_th),
            Paragraph("On-Screen Visual Action", style_th),
            Paragraph("Voice-Over Narration Script (Exact Delivery)", style_th),
            Paragraph("Scene Goal", style_th)
        ],
        [
            Paragraph("<b>0:00 – 0:15</b><br/>(15 sec)", style_td_bold),
            Paragraph("Black screen with bold statistic: <i>₹120+ Crores lost to Digital Arrest scams</i>. "
                      "Transition to phone ringing with high urgency.", style_td),
            Paragraph("<i>'Digital arrest scams are draining innocent citizens worldwide. Scammers trap victims in psychological terror "
                      "by telling one devastating lie about the physical world.'</i>", style_td),
            Paragraph("Hook & Urgency", style_td)
        ],
        [
            Paragraph("<b>0:15 – 0:55</b><br/>(40 sec)", style_td_bold),
            Paragraph("Split-screen: Fake police officer in uniform demanding ₹4.5L escrow. "
                      "Living room TV and Ring live feed shown on right.", style_td),
            Paragraph("<i>'The fake officer claims: \"Armed police are outside your door right now. Transfer the verification escrow "
                      "immediately or we break in!\" On the phone, deepfake score climbs to 0.92; coercion script flags isolation.'</i>", style_td),
            Paragraph("The Physical Lie", style_td)
        ],
        [
            Paragraph("<b>0:55 – 1:25</b><br/>(30 sec)", style_td_bold),
            Paragraph("<b>THE CLIMAX:</b> Strands Agent checks Ring sensor oracle. Porch is CLEAR. "
                      "Fire TV takes over full screen in high-contrast alert. Chime sounds. Bank transfer blocked.", style_td),
            Paragraph("<i>'MIRAGE-SHIELD's AI agent checks the Ring Doorbell oracle. Zero people. Zero vehicles. It is a physical contradiction! "
                      "Instantly, Fire TV takes over the living room, shattering the isolation. The chime rings. Bank transfers freeze.'</i>", style_td),
            Paragraph("<b>Living-Room Takeover</b>", style_badge_green)
        ],
        [
            Paragraph("<b>1:25 – 1:45</b><br/>(20 sec)", style_td_bold),
            Paragraph("Family phone shows SMS alert with verified snapshot hash. "
                      "Son reviews incident and enters secondary co-sign authorization.", style_td),
            Paragraph("<i>'Simultaneously, trusted family receives an emergency SMS alert with cryptographic proof. "
                      "Money remains locked until a family guardian co-signs to release it.'</i>", style_td),
            Paragraph("Dual Co-Sign Guard", style_td)
        ],
        [
            Paragraph("<b>1:45 – 2:10</b><br/>(25 sec)", style_td_bold),
            Paragraph("Rapid sequence: Scenario 2 (genuine daughter call - stays quiet) "
                      "and Scenario 3 (real Amazon delivery - package and human verified).", style_td),
            Paragraph("<i>'MIRAGE-SHIELD never cries wolf. In genuine family calls, it remains silent. When a real Amazon courier arrives, "
                      "Ring confirms package and human events, permitting normal activity.'</i>", style_td),
            Paragraph("Zero False Alarms", style_td)
        ],
        [
            Paragraph("<b>2:10 – 2:35</b><br/>(25 sec)", style_td_bold),
            Paragraph("Architecture diagram highlighting Ring API endpoints, Bedrock Strands agent, "
                      "and AWS KMS cryptographic signature ledger (`RSASSA_PKCS1_V1_5_SHA_256`).", style_td),
            Paragraph("<i>'Built on official Ring Partner APIs, Amazon Bedrock, and AWS KMS for tamper-evident legal records "
                      "admissible under cybercrime reporting portal 1930.'</i>", style_td),
            Paragraph("AWS Architecture", style_td)
        ],
        [
            Paragraph("<b>2:35 – 2:55</b><br/>(20 sec)", style_td_bold),
            Paragraph("Open-source `ring-evidence-mcp` package repository, team credits, and closing logo banner.", style_td),
            Paragraph("<i>'We have also open-sourced ring-evidence-mcp so any AI agent can verify physical entrance truth. "
                      "Scammers weaponize isolation and lie about the front door. Ring tells the truth. MIRAGE-SHIELD defends the living room.'</i>", style_td),
            Paragraph("Open Source & Close", style_td)
        ]
    ]

    t_video = Table(video_script_data, colWidths=[80, 160, 215, 85])
    t_video.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_video)
    elements.append(Spacer(1, 5))

    # Section 6: Contingency & Cut Order
    elements.append(Paragraph("6. Risk Contingency & Approved Graceful Cut Order", style_h1))
    contingency_text = (
        "If video rendering or submission window compresses before the Oct 23, 18:00 IST submission deadline, "
        "the team must strictly follow the roadmap's approved graceful cut order:<br/>"
        "• <b>Approved Cut Order:</b> "
        "(1) <i>Chime audio playback</i> (Fire TV carries warning) ➔ "
        "(2) <i>Family co-sign UI screen</i> (Keep SMS text and payment lock) ➔ "
        "(3) <i>AgentCore deployment</i> (Utilize verified Lambda / local runtime) ➔ "
        "(4) <i>Scenario 3 Courier footage</i> (Focus on Scenario 1 & 2) ➔ "
        "(5) <i>Deepfake video model score</i> (Rely on NLP coercion transcript analysis + Ring physical contradiction).<br/>"
        "• <b>NON-NEGOTIABLE CORE (NEVER CUT UNDER ANY CIRCUMSTANCES):</b> "
        "✔ <b>Real Ring API Calls</b> (`api.amazonvision.com` device ingestion & snapshot hash verification)  |  "
        "✔ <b>Fire TV Full-Screen Intervention Takeover</b> (The 10-foot visual proof shattering the scam isolation)  |  "
        "✔ <b>Scenario 1 (Scam Caught)</b> (The primary digital arrest cross-examination demonstration)."
    )
    elements.append(Paragraph(contingency_text, style_body))

    # =========================================================
    # PAGE 5: PRE-FLIGHT CHECKLIST, SIGN-OFF & ARTIFACT INDEX
    # =========================================================
    elements.append(PageBreak())
    elements.append(Paragraph("7. Final Pre-Flight Submission Checklist (Target: Oct 23 @ 18:00 IST)", style_h1))
    
    checklist_data = [
        [
            Paragraph("Item", style_th),
            Paragraph("Submission Requirement & Verification Step", style_th),
            Paragraph("Target Deadline", style_th),
            Paragraph("Status", style_th)
        ],
        [
            Paragraph("1", style_td_bold),
            Paragraph("Demo Video uploaded to YouTube/Vimeo as Public (Under 2:55, English, no 3rd-party audio)", style_td),
            Paragraph("Oct 22, 20:30 IST", style_td),
            Paragraph("<b>IN PROGRESS</b>", style_badge_amber)
        ],
        [
            Paragraph("2", style_td_bold),
            Paragraph("Devpost description text, architecture diagram, and honest scoping declarations pasted", style_td),
            Paragraph("Oct 22, 22:30 IST", style_td),
            Paragraph("<b>DRAFT READY</b>", style_badge_blue)
        ],
        [
            Paragraph("3", style_td_bold),
            Paragraph("Friction Log (8 entries) and Product Feedback (Ring, Vega, Bedrock, Kiro) populated", style_td),
            Paragraph("Oct 22, 22:30 IST", style_td),
            Paragraph("<b>DRAFT READY</b>", style_badge_blue)
        ],
        [
            Paragraph("4", style_td_bold),
            Paragraph("AWS Builder fields and Open Source (`ring-evidence-mcp`) links and descriptions verified", style_td),
            Paragraph("Oct 22, 22:30 IST", style_td),
            Paragraph("<b>DRAFT READY</b>", style_badge_blue)
        ],
        [
            Paragraph("5", style_td_bold),
            Paragraph("GitHub repository toggled to Public with MIT License (`LICENSE` verified)", style_td),
            Paragraph("Oct 23, 12:00 IST", style_td),
            Paragraph("<b>SCHEDULED</b>", style_badge_blue)
        ],
        [
            Paragraph("6", style_td_bold),
            Paragraph("Final two-person review of all Devpost submission form fields", style_td),
            Paragraph("Oct 23, 16:00 IST", style_td),
            Paragraph("<b>SCHEDULED</b>", style_badge_blue)
        ],
        [
            Paragraph("7", style_td_bold),
            Paragraph("Official Devpost submission finalized before 18:00 IST (+6.5 hour buffer) & screenshot saved", style_td),
            Paragraph("Oct 23, 18:00 IST", style_td),
            Paragraph("<b>TARGET GATE</b>", style_badge_amber)
        ]
    ]

    t_check = Table(checklist_data, colWidths=[25, 335, 95, 85])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_check)
    elements.append(Spacer(1, 6))

    # Section 8: Technical Sign-Off
    elements.append(Paragraph("8. Technical Verification Sign-Off & Audit Certificate", style_h1))
    cert_text = (
        "<b>MASTER PRE-FREEZE VERIFICATION CERTIFICATE</b><br/>"
        "• <b>Master Test Runner:</b> `python verify_all.py` executed cleanly with <b>3 of 3 stages passing</b> in 16.3s.<br/>"
        "• <b>Integration Scenarios:</b> `python test_scenarios.py` completed <b>15 of 15 consecutive iterations (100% pass rate)</b> across Scenarios 1, 2, and 3.<br/>"
        "• <b>Open Source MCP Server:</b> `ring-evidence-mcp` standalone test suite passed <b>4 of 4 tool registration and protocol dispatch tests</b>.<br/>"
        "• <b>Cryptographic Chain of Custody:</b> AWS KMS asymmetric signature generation verified (`RSASSA_PKCS1_V1_5_SHA_256`).<br/>"
        "• <b>Code Freeze Status:</b> <b>FROZEN as of Oct 22, 12:00 IST</b>. Zero architectural or breaking code changes permitted during video production."
    )
    t_cert = Table([[Paragraph(cert_text, style_callout)]], colWidths=[540])
    t_cert.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_green_light),
        ('BOX', (0, 0), (-1, -1), 0.75, c_green),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_cert)
    elements.append(Spacer(1, 6))

    # Section 9: Documentation Index
    elements.append(Paragraph("9. Project Documentation Artifacts & Resource Index", style_h1))
    doc_index_data = [
        [
            Paragraph("Document Artifact", style_th),
            Paragraph("File Path in Workspace", style_th),
            Paragraph("Purpose & Hackathon Deliverable Mapping", style_th)
        ],
        [
            Paragraph("<b>Full Submission Package</b>", style_td_bold),
            Paragraph("`docs/SUBMISSION.md`", style_td),
            Paragraph("Complete 320+ line Devpost submission draft with executive summary, friction log, and honest scoping.", style_td)
        ],
        [
            Paragraph("<b>Developer Friction Log</b>", style_td_bold),
            Paragraph("`docs/FRICTION_LOG.md`", style_td),
            Paragraph("8 detailed developer friction entries across Ring API, Vega OS, and AWS KMS (10% bonus submission).", style_td)
        ],
        [
            Paragraph("<b>Product Feedback</b>", style_td_bold),
            Paragraph("`docs/PRODUCT_FEEDBACK.md`", style_td),
            Paragraph("Structured actionable feedback for Ring API, Vega SDK, Bedrock, and Kiro product teams.", style_td)
        ],
        [
            Paragraph("<b>AWS Builder Architecture</b>", style_td_bold),
            Paragraph("`docs/AWS_BUILDER.md`", style_td),
            Paragraph("Technical reference for Bedrock Strands Agent, KMS asymmetric signing, and DynamoDB incident ledger.", style_td)
        ],
        [
            Paragraph("<b>Open Source MCP Server</b>", style_td_bold),
            Paragraph("`ring-evidence-mcp/`", style_td),
            Paragraph("Standalone Model Context Protocol server exposing Ring sensor tools to AI agents under MIT license.", style_td)
        ],
        [
            Paragraph("<b>Unified Server Launcher</b>", style_td_bold),
            Paragraph("`run.py`", style_td),
            Paragraph("Single-command master launcher hosting Master Console, Fire TV view, and API docs at `127.0.0.1:8000`.", style_td)
        ]
    ]

    t_doc_index = Table(doc_index_data, colWidths=[130, 140, 270])
    t_doc_index.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_slate_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_doc_index)

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"✔ PDF report successfully generated at: {output_path}")


if __name__ == "__main__":
    create_roadmap_pdf(OUTPUT_PDF_PATH)
