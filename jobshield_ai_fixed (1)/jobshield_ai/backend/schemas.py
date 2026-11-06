"""
Pydantic Schemas for JobShield AI data validation and API payloads.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field

# Authentication
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6)
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Scan Schemas
class RiskBreakdown(BaseModel):
    ml_confidence_score: float
    heuristic_risk_score: float
    recruiter_risk_score: float
    company_risk_score: float
    composite_risk_score: float

class FlagItem(BaseModel):
    rule: str
    severity: str  # critical, high, medium, low
    description: str
    match_text: Optional[str] = None

class ScanResult(BaseModel):
    id: Optional[int] = None
    scan_type: str
    risk_score: float  # 0 to 100
    risk_level: str  # Low, Medium, High / Critical
    verdict: str
    confidence: float
    flags: List[FlagItem]
    breakdown: RiskBreakdown
    recommendations: List[str]
    input_preview: str
    created_at: Optional[datetime] = None

class TextScanRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    claimed_company: Optional[str] = None
    recruiter_email: Optional[str] = None

class UrlScanRequest(BaseModel):
    url: str

class UrlScanResponse(BaseModel):
    url: str
    domain: str
    is_suspicious_tld: bool
    is_ip_address: bool
    typo_squatting_detected: bool
    matched_legit_company: Optional[str] = None
    virustotal_malicious: int
    risk_score: float
    risk_level: str
    verdict: str
    details: List[str]

# Company & Recruiter Verification
class CompanyVerifyRequest(BaseModel):
    company_name: str
    offered_domain: Optional[str] = None

class CompanyVerifyResponse(BaseModel):
    query_company: str
    is_verified: bool
    matched_official_name: Optional[str] = None
    official_domain: Optional[str] = None
    careers_url: Optional[str] = None
    domain_match: bool
    warning: Optional[str] = None

class RecruiterVerifyRequest(BaseModel):
    email: str
    phone: Optional[str] = None
    claimed_company: Optional[str] = None

class RecruiterVerifyResponse(BaseModel):
    email: str
    is_free_provider: bool
    provider_name: str
    is_disposable: bool
    domain_matches_company: bool
    risk_score: float
    verdict: str
    flags: List[str]

# Community Reports
class CommunityReportCreate(BaseModel):
    scam_title: str
    company_claimed: str
    recruiter_contact: str
    scam_description: str
    payment_demanded: Optional[str] = "None"

class CommunityReportOut(BaseModel):
    id: int
    user_id: Optional[int] = None
    scam_title: str
    company_claimed: str
    recruiter_contact: str
    scam_description: str
    payment_demanded: str
    upvotes: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Admin Schemas
class BlacklistCreate(BaseModel):
    entry_type: str
    value: str
    reason: str

class BlacklistOut(BaseModel):
    id: int
    entry_type: str
    value: str
    reason: str
    added_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class AdminStatsOut(BaseModel):
    total_users: int
    total_scans: int
    high_risk_scans: int
    medium_risk_scans: int
    low_risk_scans: int
    total_community_reports: int
    verified_companies_count: int
    blacklisted_entries_count: int
