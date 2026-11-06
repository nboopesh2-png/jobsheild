"""
Company Verification Router for JobShield AI.
Allows users to check employer legitimacy and query verified enterprises.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import VerifiedCompany
from backend.schemas import CompanyVerifyRequest, CompanyVerifyResponse
from backend.services.company_verifier import verify_company, VERIFIED_ENTERPRISES

router = APIRouter(prefix="/api/company", tags=["Company Verification"])

@router.post("/verify", response_model=CompanyVerifyResponse)
def check_company(payload: CompanyVerifyRequest):
    """Verifies company name against verified database and checks domain match."""
    return verify_company(payload.company_name, payload.offered_domain)

@router.get("/directory")
def get_company_directory():
    """Returns a list of verified tier-1 employers with their official careers portals."""
    return VERIFIED_ENTERPRISES
