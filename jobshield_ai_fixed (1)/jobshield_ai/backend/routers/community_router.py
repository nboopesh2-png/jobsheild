"""
Community Scam Reporting Router for JobShield AI.
Crowdsourced threat intelligence enabling students to share, alert, and upvote fraudulent offers.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, CommunityReport
from backend.schemas import CommunityReportCreate, CommunityReportOut
from backend.auth import get_optional_current_user

router = APIRouter(prefix="/api/community", tags=["Community Intelligence"])

@router.post("/reports", response_model=CommunityReportOut, status_code=status.HTTP_201_CREATED)
def submit_report(
    payload: CommunityReportCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Submits a new recruitment fraud report to the community intelligence feed."""
    report = CommunityReport(
        user_id=current_user.id if current_user else None,
        scam_title=payload.scam_title,
        company_claimed=payload.company_claimed,
        recruiter_contact=payload.recruiter_contact,
        scam_description=payload.scam_description,
        payment_demanded=payload.payment_demanded or "None",
        upvotes=1,
        status="verified"
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/reports", response_model=List[CommunityReportOut])
def list_reports(
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Retrieves verified community scam reports sorted by upvotes and recency."""
    return db.query(CommunityReport).filter(
        CommunityReport.status == "verified"
    ).order_by(CommunityReport.upvotes.desc(), CommunityReport.created_at.desc()).limit(limit).all()

@router.post("/reports/{report_id}/upvote", response_model=CommunityReportOut)
def upvote_report(report_id: int, db: Session = Depends(get_db)):
    """Upvotes a scam report to alert other students."""
    report = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Scam report not found.")

    report.upvotes += 1
    db.commit()
    db.refresh(report)
    return report
