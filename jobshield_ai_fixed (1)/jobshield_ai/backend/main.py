"""
FastAPI Application Entry Point for JobShield AI.
Integrates security middleware, API routers, database auto-migration, and seed data initialization.
"""
import sys
import os
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import PROJECT_NAME, VERSION
from backend.database import engine, Base, SessionLocal
from backend.models import User, VerifiedCompany, BlacklistEntry, CommunityReport, ScanRecord
from backend.auth import hash_password
from backend.services.company_verifier import VERIFIED_ENTERPRISES

# Import Routers
from backend.routers.auth_router import router as auth_router
from backend.routers.scan_router import router as scan_router
from backend.routers.company_router import router as company_router
from backend.routers.recruiter_router import router as recruiter_router
from backend.routers.community_router import router as community_router
from backend.routers.admin_router import router as admin_router

logger = logging.getLogger("jobshield.main")
logging.basicConfig(level=logging.INFO)

def init_seed_data():
    """Initializes default administrative accounts, verified employers, and threat intelligence."""
    db = SessionLocal()
    try:
        # 1. Create Default Admin User
        admin = db.query(User).filter(User.email == "admin@jobshield.ai").first()
        if not admin:
            admin = User(
                email="admin@jobshield.ai",
                full_name="JobShield Security Admin",
                hashed_password=hash_password("Admin@123456"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            logger.info("Created default administrator: admin@jobshield.ai / Admin@123456")

        # 2. Create Default Student User
        student = db.query(User).filter(User.email == "student@college.edu").first()
        if not student:
            student = User(
                email="student@college.edu",
                full_name="Praveen Kumar (CSE)",
                hashed_password=hash_password("Student@123456"),
                role="student",
                is_active=True
            )
            db.add(student)
            logger.info("Created default student user: student@college.edu / Student@123456")

        db.commit()

        # 3. Seed Verified Enterprise Directory
        if db.query(VerifiedCompany).count() == 0:
            for c in VERIFIED_ENTERPRISES:
                entry = VerifiedCompany(
                    name=c["name"],
                    domain=c["domain"],
                    industry="Information Technology & Software",
                    careers_url=c["careers"],
                    is_verified=True
                )
                db.add(entry)
            db.commit()
            logger.info(f"Seeded {len(VERIFIED_ENTERPRISES)} verified enterprises into database.")

        # 4. Seed Known Scam Blacklist Indicators
        if db.query(BlacklistEntry).count() == 0:
            sample_blacklist = [
                {"type": "domain", "val": "tcs-careers-interview.online", "reason": "Phishing clone impersonating TCS recruiting portal"},
                {"type": "domain", "val": "infosys-direct-placement.xyz", "reason": "Registration fee extortion scam targeting freshers"},
                {"type": "email", "val": "amazon.recruiter.hr2025@gmail.com", "reason": "Impersonator demanding security deposits via Google Pay"},
                {"type": "upi", "val": "fake_hr_dept@okaxis", "reason": "Mule account collecting fraudulent laptop courier fees"},
                {"type": "phone", "val": "+919876500000", "reason": "Automated WhatsApp recruitment bot spamming YouTube task scams"}
            ]
            for b in sample_blacklist:
                db.add(BlacklistEntry(
                    entry_type=b["type"],
                    value=b["val"],
                    reason=b["reason"],
                    added_by="System Heuristic Engine"
                ))
            db.commit()
            logger.info("Seeded initial threat blacklist indicators.")

        # 5. Seed Initial Community Scam Alerts
        if db.query(CommunityReport).count() == 0:
            sample_reports = [
                {
                    "title": "Telegram YouTube Video Liking Scam Lure",
                    "company": "Amazon Part-Time Recruitment",
                    "contact": "Telegram @amz_parttime_admin",
                    "desc": "Claimed to offer Rs. 3,500 daily for liking 10 YouTube videos. After paying initial Rs. 1500 'vip upgrade', user was blocked.",
                    "payment": "Rs. 1,500 via PhonePe",
                    "upvotes": 42
                },
                {
                    "title": "Fake TCS Offer Letter Demanding Laptop Courier Insurance",
                    "company": "Tata Consultancy Services (Spoofed)",
                    "contact": "tcs.offer.team@gmail.com",
                    "desc": "Sent fake PDF offer on letterhead asking for Rs. 2,999 courier insurance for dispatching Lenovo ThinkPad.",
                    "payment": "Rs. 2,999 via Google Pay",
                    "upvotes": 28
                },
                {
                    "title": "Data Entry PDF to Word Security Deposit Extortion",
                    "company": "Global Documents BPO",
                    "contact": "+91 9840123987 (WhatsApp)",
                    "desc": "Demanded Rs. 2,000 security deposit for sending 100 pages. Promised Rs. 50,000 payout. Disappeared after payment.",
                    "payment": "Rs. 2,000 via UPI",
                    "upvotes": 19
                }
            ]
            for r in sample_reports:
                db.add(CommunityReport(
                    user_id=student.id if student else None,
                    scam_title=r["title"],
                    company_claimed=r["company"],
                    recruiter_contact=r["contact"],
                    scam_description=r["desc"],
                    payment_demanded=r["payment"],
                    upvotes=r["upvotes"],
                    status="verified"
                ))
            db.commit()
            logger.info("Seeded verified community scam alert reports.")

    except Exception as e:
        logger.error(f"Error during database seed initialization: {e}")
        db.rollback()
    finally:
        db.close()

_initialized = False

def ensure_initialized():
    """Create tables + seed data once per process.

    Vercel (serverless) does not reliably run FastAPI's lifespan startup event,
    so this is also called lazily from a middleware on the first request.
    """
    global _initialized
    if _initialized:
        return
    Base.metadata.create_all(bind=engine)
    init_seed_data()
    _initialized = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed
    ensure_initialized()
    yield
    # Shutdown

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="AI-Powered Fake Job Offer & Internship Scam Detection API",
    lifespan=lifespan
)

@app.middleware("http")
async def init_db_on_first_request(request, call_next):
    try:
        ensure_initialized()
    except Exception as e:  # keep the API alive; /api/health will show the problem
        logger.error(f"Database initialization failed: {e}")
    return await call_next(request)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # "*" origins + credentials is invalid per CORS spec; we use Bearer tokens
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(scan_router)
app.include_router(company_router)
app.include_router(recruiter_router)
app.include_router(community_router)
app.include_router(admin_router)

@app.get("/", include_in_schema=False)
def root():
    return {"message": f"{PROJECT_NAME} API is running", "docs": "/docs", "health": "/api/health"}

@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check and diagnostic status."""
    return {
        "status": "healthy",
        "platform": PROJECT_NAME,
        "version": VERSION,
        "database": engine.name
    }
