"""
Cybersecurity PDF Audit Report Generator for JobShield AI.
Generates comprehensive forensic reports of scanned job offers using ReportLab.
"""
import io
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf_report(scan_data: Dict[str, Any], user_name: str = "Student Candidate") -> bytes:
    """
    Builds a professional cybersecurity evaluation report in PDF format.
    Returns bytes of the compiled document.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Heading1"],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0B132B"),
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "HeaderSub",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#3A506B"),
        alignment=TA_CENTER
    )
    section_title = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1C2541"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2B2D42")
    )
    bold_style = ParagraphStyle(
        "BodyDarkBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("🛡️ JOBSHIELD AI", header_style))
    elements.append(Paragraph("AI-Powered Fake Job Offer & Internship Scam Detection Audit", subtitle_style))
    elements.append(Spacer(1, 14))

    # Meta Info Table
    scan_id = scan_data.get("id", "LIVE-" + datetime.utcnow().strftime("%Y%m%d%H%M"))
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    risk_score = scan_data.get("risk_score", 0.0)
    risk_level = scan_data.get("risk_level", "Unknown")
    verdict = scan_data.get("verdict", "N/A")

    # Pick colors based on risk
    if "high" in risk_level.lower() or "critical" in risk_level.lower():
        status_color = colors.HexColor("#FF0055")
        status_bg = colors.HexColor("#FFE5EC")
    elif "medium" in risk_level.lower():
        status_color = colors.HexColor("#E0A900")
        status_bg = colors.HexColor("#FFF8E1")
    else:
        status_color = colors.HexColor("#00875A")
        status_bg = colors.HexColor("#E3FCEF")

    meta_table_data = [
        [
            Paragraph("<b>Report Identifier:</b>", body_style),
            Paragraph(f"JS-AUDIT-{scan_id}", body_style),
            Paragraph("<b>Generated For:</b>", body_style),
            Paragraph(user_name, body_style)
        ],
        [
            Paragraph("<b>Inspection Date:</b>", body_style),
            Paragraph(timestamp, body_style),
            Paragraph("<b>Scan Mode:</b>", body_style),
            Paragraph(scan_data.get("scan_type", "Text Analysis").upper(), body_style)
        ]
    ]

    meta_table = Table(meta_table_data, colWidths=[110, 160, 110, 160])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7DE")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 14))

    # Verdict Banner
    verdict_data = [
        [
            Paragraph(f"<b>COMPOSITE RISK SCORE: {risk_score}%  |  TIER: {risk_level.upper()}</b>", ParagraphStyle(
                "VerdictTitle", parent=styles["Normal"], fontSize=13, fontName="Helvetica-Bold", textColor=status_color, alignment=TA_CENTER
            )),
        ],
        [
            Paragraph(f"<b>VERDICT: {verdict}</b>", ParagraphStyle(
                "VerdictSub", parent=styles["Normal"], fontSize=10, textColor=status_color, alignment=TA_CENTER
            ))
        ]
    ]
    verdict_table = Table(verdict_data, colWidths=[540])
    verdict_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), status_bg),
        ("BOX", (0, 0), (-1, -1), 1.5, status_color),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))
    elements.append(verdict_table)
    elements.append(Spacer(1, 14))

    # Breakdown Section
    elements.append(Paragraph("Factor Decomposition Analysis", section_title))
    bd = scan_data.get("breakdown", {})
    decomp_data = [
        [Paragraph("<b>Risk Metric Component</b>", bold_style), Paragraph("<b>Score / Contribution</b>", bold_style), Paragraph("<b>Status Assessment</b>", bold_style)],
        [Paragraph("NLP Scikit-Learn Model Confidence", body_style), Paragraph(f"{bd.get('ml_confidence_score', 0)}%", body_style), Paragraph("Linguistic pattern analysis", body_style)],
        [Paragraph("Heuristic Rule Trigger Points", body_style), Paragraph(f"{bd.get('heuristic_risk_score', 0)} pts", body_style), Paragraph("Rule-based pattern matching", body_style)],
        [Paragraph("Recruiter Identity & Email Check", body_style), Paragraph(f"{bd.get('recruiter_risk_score', 0)}%", body_style), Paragraph("Domain & contact legitimacy", body_style)],
        [Paragraph("Enterprise Directory Verification", body_style), Paragraph(f"{bd.get('company_risk_score', 0)}%", body_style), Paragraph("Typo-squatting & registry", body_style)]
    ]
    decomp_table = Table(decomp_data, colWidths=[240, 130, 170])
    decomp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C2541")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7DE")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))
    elements.append(decomp_table)
    elements.append(Spacer(1, 14))

    # Flagged Anomalies Section
    elements.append(Paragraph("Detected Security & Fraud Indicators", section_title))
    flags = scan_data.get("flags", [])
    if flags:
        flag_rows = [
            [Paragraph("<b>Severity</b>", bold_style), Paragraph("<b>Rule Name</b>", bold_style), Paragraph("<b>Evidence / Description</b>", bold_style)]
        ]
        for f in flags:
            rule_name = f.get("rule", "Anomaly")
            sev = str(f.get("severity", "Medium")).upper()
            desc = f.get("description", "")
            match = f.get("match_text", "")
            if match:
                desc = f"Matched: \"{match}\" - {desc}"
            flag_rows.append([
                Paragraph(f"<b>{sev}</b>", body_style),
                Paragraph(rule_name, body_style),
                Paragraph(desc, body_style)
            ])
        flag_table = Table(flag_rows, colWidths=[90, 160, 290])
        flag_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3A506B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7DE")),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))
        elements.append(flag_table)
    else:
        elements.append(Paragraph("No critical fraudulent signals or malicious keywords detected in this sample.", body_style))

    elements.append(Spacer(1, 14))

    # Actionable Safety Checklist
    elements.append(Paragraph("Recommended Safety Actions for Students", section_title))
    recommendations = scan_data.get("recommendations", [])
    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", body_style))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("<b>National Cyber Crime Helpline:</b> Call <b>1930</b> or file an incident at <b>https://cybercrime.gov.in</b>.", bold_style))
    elements.append(Spacer(1, 20))

    # Footer note
    elements.append(Paragraph("JobShield AI — Final Year College Project & Student Recruitment Protection Initiative.", subtitle_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
