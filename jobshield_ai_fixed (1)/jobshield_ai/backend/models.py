"""
SQLAlchemy ORM models for JobShield AI.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="student", nullable=False)  # student or admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    scans = relationship("ScanRecord", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("CommunityReport", back_populates="user", cascade="all, delete-orphan")

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    scan_type = Column(String(50), nullable=False)  # text, ocr, url
    input_preview = Column(Text, nullable=False)
    risk_score = Column(Float, nullable=False)  # 0 to 100
    risk_level = Column(String(50), nullable=False)  # Low, Medium, High / Critical
    verdict = Column(String(100), nullable=False)
    confidence = Column(Float, default=0.0)
    flags_json = Column(Text, default="[]")  # JSON string of detected flags
    breakdown_json = Column(Text, default="{}")  # JSON breakdown of risk scores
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scans")

class CommunityReport(Base):
    __tablename__ = "community_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    scam_title = Column(String(255), nullable=False)
    company_claimed = Column(String(255), nullable=False)
    recruiter_contact = Column(String(255), nullable=False)
    scam_description = Column(Text, nullable=False)
    payment_demanded = Column(String(255), default="None")
    upvotes = Column(Integer, default=1)
    status = Column(String(50), default="verified")  # pending, verified, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")

class VerifiedCompany(Base):
    __tablename__ = "verified_companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=False)
    industry = Column(String(100), default="Information Technology")
    careers_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=True)

class BlacklistEntry(Base):
    __tablename__ = "blacklist_entries"

    id = Column(Integer, primary_key=True, index=True)
    entry_type = Column(String(50), nullable=False)  # domain, email, phone, keyword, upi
    value = Column(String(255), unique=True, index=True, nullable=False)
    reason = Column(String(500), nullable=False)
    added_by = Column(String(100), default="System")
    created_at = Column(DateTime, default=datetime.utcnow)
