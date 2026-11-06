"""
Scan Router for JobShield AI.
Coordinates Text Analysis, Screenshot OCR Extraction, URL Inspection,
History Persistence, and PDF Report Exports.
"""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, ScanRecord
from backend.schemas import TextScanRequest, ScanResult, UrlScanRequest, UrlScanResponse
from backend.auth import get_optional_current_user, get_current_user
from backend.ai.model import get_classifier
from backend.ai.rules_engine import evaluate_rules
from backend.ai.risk_scorer import calculate_composite_risk
from backend.ai.ocr_engine import extract_text_from_image
from backend.services.company_verifier import verify_company
from backend.services.recruiter_verifier import verify_recruiter_email
from backend.services.url_scanner import scan_url_security
from backend.services.pdf_generator import generate_pdf_report

router = APIRouter(prefix="/api/scan", tags=["Scanners"])

@router.post("/text", response_model=ScanResult)
def scan_text(
    payload: TextScanRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Scans raw job/internship offer text using ML and rule-based heuristics."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Offer text cannot be empty.")

    # 1. AI ML Model Prediction
    clf = get_classifier()
    ml_result = clf.predict(text)
    ml_score = ml_result["scam_probability"]

    # 2. Rule-Based Heuristic Evaluation
    heuristic_flags = evaluate_rules(text)

    # 3. Recruiter Risk (if email supplied)
    recruiter_risk = 0.0
    if payload.recruiter_email:
        rec_eval = verify_recruiter_email(payload.recruiter_email, payload.claimed_company)
        recruiter_risk = rec_eval["risk_score"]
        if rec_eval["risk_score"] > 40:
            heuristic_flags.append({
                "rule": "Suspicious Recruiter Domain",
                "severity": "high",
                "description": "; ".join(rec_eval["flags"]),
                "match_text": payload.recruiter_email,
                "points": 20
            })

    # 4. Company Verification Risk (if company supplied)
    company_risk = 0.0
    if payload.claimed_company:
        comp_eval = verify_company(payload.claimed_company)
        if not comp_eval["is_verified"]:
            company_risk = 25.0
        if comp_eval.get("warning"):
            heuristic_flags.append({
                "rule": "Unverified Employer Alert",
                "severity": "medium",
                "description": comp_eval["warning"],
                "match_text": payload.claimed_company,
                "points": 15
            })

    # 5. Composite Risk Calculation
    risk_data = calculate_composite_risk(
        ml_confidence_score=ml_score,
        heuristic_flags=heuristic_flags,
        recruiter_risk=recruiter_risk,
        company_risk=company_risk
    )

    # 6. Save Record in Database
    scan_record = ScanRecord(
        user_id=current_user.id if current_user else None,
        scan_type="text",
        input_preview=text[:300] + ("..." if len(text) > 300 else ""),
        risk_score=risk_data["composite_risk_score"],
        risk_level=risk_data["risk_level"],
        verdict=risk_data["verdict"],
        confidence=ml_result["confidence"],
        flags_json=json.dumps(heuristic_flags),
        breakdown_json=json.dumps(risk_data["breakdown"])
    )
    db.add(scan_record)
    db.commit()
    db.refresh(scan_record)

    return {
        "id": scan_record.id,
        "scan_type": "text",
        "risk_score": risk_data["composite_risk_score"],
        "risk_level": risk_data["risk_level"],
        "verdict": risk_data["verdict"],
        "confidence": ml_result["confidence"],
        "flags": heuristic_flags,
        "breakdown": risk_data["breakdown"],
        "recommendations": risk_data["recommendations"],
        "input_preview": scan_record.input_preview,
        "created_at": scan_record.created_at
    }

@router.post("/ocr", response_model=ScanResult)
async def scan_ocr(
    file: UploadFile = File(...),
    claimed_company: Optional[str] = Form(None),
    recruiter_email: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Extracts text from uploaded image screenshot and performs AI scam inspection."""
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (PNG, JPG, JPEG).")

    contents = await file.read()
    extracted_text = extract_text_from_image(contents)

    if not extracted_text or len(extracted_text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Insufficient legible text could be extracted from this image. Please upload a clearer screenshot or paste the text into the AI Text Scanner."
        )

    # Forward to text scanner pipeline
    payload = TextScanRequest(
        text=extracted_text,
        claimed_company=claimed_company,
        recruiter_email=recruiter_email
    )
    result = scan_text(payload, db, current_user)
    result["scan_type"] = "ocr"
    return result

@router.post("/url", response_model=UrlScanResponse)
def scan_url(
    payload: UrlScanRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Scans URL for phishing signals, typo-squatting, and malicious reputation."""
    res = scan_url_security(payload.url)

    # Persist in DB
    scan_record = ScanRecord(
        user_id=current_user.id if current_user else None,
        scan_type="url",
        input_preview=payload.url[:300],
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        verdict=res["verdict"],
        confidence=res["risk_score"],
        flags_json=json.dumps([{"rule": "URL Check", "severity": res["risk_level"], "description": d} for d in res["details"]]),
        breakdown_json=json.dumps({"url_risk": res["risk_score"]})
    )
    db.add(scan_record)
    db.commit()

    return res

@router.get("/history")
def get_user_scan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all past scan records for the authenticated user."""
    records = db.query(ScanRecord).filter(
        ScanRecord.user_id == current_user.id
    ).order_by(ScanRecord.created_at.desc()).limit(50).all()

    formatted = []
    for r in records:
        flags = json.loads(r.flags_json) if r.flags_json else []
        breakdown = json.loads(r.breakdown_json) if r.breakdown_json else {}
        formatted.append({
            "id": r.id,
            "scan_type": r.scan_type,
            "input_preview": r.input_preview,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "verdict": r.verdict,
            "confidence": r.confidence,
            "flags": flags,
            "breakdown": breakdown,
            "created_at": r.created_at
        })
    return formatted

@router.get("/{scan_id}/report.pdf")
def download_pdf_report(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Generates and downloads a cybersecurity forensic PDF report for a scan."""
    record = db.query(ScanRecord).filter(ScanRecord.id == scan_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Scan record not found.")

    flags = json.loads(record.flags_json) if record.flags_json else []
    breakdown = json.loads(record.breakdown_json) if record.breakdown_json else {}

    # Context recommendations
    recommendations = [
        "Never transfer money: Genuine employers never charge for applications, tests, or equipment.",
        "Verify all offers on official corporate careers portals.",
        "Report cyber fraud incidents to the National Cyber Crime Helpline (1930)."
    ]

    scan_data = {
        "id": record.id,
        "scan_type": record.scan_type,
        "risk_score": record.risk_score,
        "risk_level": record.risk_level,
        "verdict": record.verdict,
        "breakdown": breakdown,
        "flags": flags,
        "recommendations": recommendations
    }

    user_name = current_user.full_name if current_user else "Student Candidate"
    pdf_bytes = generate_pdf_report(scan_data, user_name)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=jobshield_report_{scan_id}.pdf"}
    )
