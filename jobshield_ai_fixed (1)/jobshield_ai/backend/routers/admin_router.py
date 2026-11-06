"""
Admin Control Center Router for JobShield AI.
Provides platform telemetry, blacklist curation, report moderation, and user oversight.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, ScanRecord, CommunityReport, VerifiedCompany, BlacklistEntry
from backend.schemas import AdminStatsOut, BlacklistCreate, BlacklistOut
from backend.auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin Portal"])

@router.get("/stats", response_model=AdminStatsOut)
def get_admin_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Gathers real telemetry and aggregate statistics across the entire JobShield AI platform."""
    total_users = db.query(User).count()
    total_scans = db.query(ScanRecord).count()
    high_risk_scans = db.query(ScanRecord).filter(ScanRecord.risk_level.ilike("%high%")).count()
    medium_risk_scans = db.query(ScanRecord).filter(ScanRecord.risk_level.ilike("%medium%")).count()
    low_risk_scans = db.query(ScanRecord).filter(ScanRecord.risk_level.ilike("%low%")).count()
    total_community_reports = db.query(CommunityReport).count()
    verified_companies_count = db.query(VerifiedCompany).count()
    blacklisted_entries_count = db.query(BlacklistEntry).count()

    return {
        "total_users": total_users,
        "total_scans": total_scans,
        "high_risk_scans": high_risk_scans,
        "medium_risk_scans": medium_risk_scans,
        "low_risk_scans": low_risk_scans,
        "total_community_reports": total_community_reports,
        "verified_companies_count": verified_companies_count,
        "blacklisted_entries_count": blacklisted_entries_count
    }

@router.get("/users")
def list_all_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Lists all registered student and administrator accounts."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
            "scan_count": len(u.scans)
        }
        for u in users
    ]

@router.get("/blacklist", response_model=List[BlacklistOut])
def list_blacklist(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Lists all active threat indicators on the JobShield AI blacklist."""
    return db.query(BlacklistEntry).order_by(BlacklistEntry.created_at.desc()).all()

@router.post("/blacklist", response_model=BlacklistOut, status_code=status.HTTP_201_CREATED)
def add_blacklist_entry(
    payload: BlacklistCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Adds a new malicious domain, email, phone, or UPI ID to the threat blacklist."""
    existing = db.query(BlacklistEntry).filter(BlacklistEntry.value == payload.value.strip().lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="This indicator is already on the blacklist.")

    entry = BlacklistEntry(
        entry_type=payload.entry_type.lower(),
        value=payload.value.strip().lower(),
        reason=payload.reason,
        added_by=admin_user.full_name
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/blacklist/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blacklist_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Deletes an indicator from the threat blacklist."""
    entry = db.query(BlacklistEntry).filter(BlacklistEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Blacklist entry not found.")
    db.delete(entry)
    db.commit()
    return None

@router.patch("/reports/{report_id}/status")
def update_report_status(
    report_id: int,
    status_str: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """Updates the moderation status of a community fraud report."""
    report = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    report.status = status_str.lower()
    db.commit()
    return {"message": "Status updated successfully.", "id": report_id, "status": report.status}
