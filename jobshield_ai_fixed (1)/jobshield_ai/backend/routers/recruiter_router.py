"""
Recruiter Verification Router for JobShield AI.
Inspects sender domains, detects free public mail providers, and flags brand spoofing.
"""
from fastapi import APIRouter
from backend.schemas import RecruiterVerifyRequest, RecruiterVerifyResponse
from backend.services.recruiter_verifier import verify_recruiter_email

router = APIRouter(prefix="/api/recruiter", tags=["Recruiter Verification"])

@router.post("/verify", response_model=RecruiterVerifyResponse)
def check_recruiter(payload: RecruiterVerifyRequest):
    """Analyzes email address to detect recruiter impersonation and disposable domains."""
    return verify_recruiter_email(payload.email, payload.claimed_company)
