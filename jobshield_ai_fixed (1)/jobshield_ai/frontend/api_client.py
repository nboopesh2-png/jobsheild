"""
API Client for JobShield AI Frontend.
Connects to the FastAPI backend with seamless local service fallback.
Ensures zero disruption whether running as a full microservices stack or single-process Streamlit.
"""
import json
import requests
from typing import Dict, Any, List, Optional
import os
from backend.config import API_HOST, API_PORT

# Set API_BASE_URL (e.g. https://your-app.vercel.app) when the backend is deployed remotely.
# Works with or without a trailing slash / "/api" suffix.
_remote = os.getenv("API_BASE_URL", "").strip().rstrip("/")
if _remote.endswith("/api"):
    _remote = _remote[:-4]
BASE_URL = f"{_remote}/api" if _remote else f"http://{API_HOST}:{API_PORT}/api"

class JobShieldAPIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    # --- Authentication ---
    def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password},
                timeout=5
            )
            if resp.status_code == 200:
                return resp.json()
            return {"error": resp.json().get("detail", "Authentication failed.")}
        except Exception:
            # Local Direct Fallback
            from backend.database import SessionLocal
            from backend.models import User
            from backend.auth import verify_password, create_access_token
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.email == email.lower()).first()
                if user and verify_password(password, user.hashed_password):
                    token = create_access_token({"sub": user.email, "role": user.role, "name": user.full_name})
                    return {
                        "access_token": token,
                        "token_type": "bearer",
                        "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role, "is_active": user.is_active}
                    }
                return {"error": "Invalid email or password."}
            finally:
                db.close()

    def register(self, email: str, full_name: str, password: str, role: str = "student") -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/auth/register",
                json={"email": email, "full_name": full_name, "password": password, "role": role},
                timeout=5
            )
            if resp.status_code == 201:
                return resp.json()
            return {"error": resp.json().get("detail", "Registration failed.")}
        except Exception:
            from backend.database import SessionLocal
            from backend.models import User
            from backend.auth import hash_password
            db = SessionLocal()
            try:
                if db.query(User).filter(User.email == email.lower()).first():
                    return {"error": "An account with this email already exists."}
                u = User(
                    email=email.lower(),
                    full_name=full_name,
                    hashed_password=hash_password(password),
                    role=role
                )
                db.add(u)
                db.commit()
                db.refresh(u)
                return {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role}
            finally:
                db.close()

    # --- Scanning Operations ---
    def scan_text(self, text: str, company: Optional[str] = None, recruiter_email: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/scan/text",
                json={"text": text, "claimed_company": company, "recruiter_email": recruiter_email},
                headers=self._headers(token),
                timeout=10
            )
            if resp.status_code == 200:
                return resp.json()
            return {"error": resp.json().get("detail", "Scan failed.")}
        except Exception:
            # Fallback to in-process AI pipeline
            from backend.ai.model import get_classifier
            from backend.ai.rules_engine import evaluate_rules
            from backend.ai.risk_scorer import calculate_composite_risk
            from backend.services.company_verifier import verify_company
            from backend.services.recruiter_verifier import verify_recruiter_email
            from backend.database import SessionLocal
            from backend.models import ScanRecord

            clf = get_classifier()
            ml_res = clf.predict(text)
            heuristics = evaluate_rules(text)

            rec_risk = 0.0
            if recruiter_email:
                r_eval = verify_recruiter_email(recruiter_email, company)
                rec_risk = r_eval["risk_score"]
                if r_eval["risk_score"] > 40:
                    heuristics.append({
                        "rule": "Suspicious Recruiter Domain",
                        "severity": "high",
                        "description": "; ".join(r_eval["flags"]),
                        "match_text": recruiter_email,
                        "points": 20
                    })

            comp_risk = 0.0
            if company:
                c_eval = verify_company(company)
                if not c_eval["is_verified"]:
                    comp_risk = 25.0
                if c_eval.get("warning"):
                    heuristics.append({
                        "rule": "Unverified Employer Alert",
                        "severity": "medium",
                        "description": c_eval["warning"],
                        "match_text": company,
                        "points": 15
                    })

            risk_eval = calculate_composite_risk(
                ml_confidence_score=ml_res["scam_probability"],
                heuristic_flags=heuristics,
                recruiter_risk=rec_risk,
                company_risk=comp_risk
            )

            # Persist record
            db = SessionLocal()
            record_id = 1
            try:
                rec = ScanRecord(
                    scan_type="text",
                    input_preview=text[:300] + ("..." if len(text) > 300 else ""),
                    risk_score=risk_eval["composite_risk_score"],
                    risk_level=risk_eval["risk_level"],
                    verdict=risk_eval["verdict"],
                    confidence=ml_res["confidence"],
                    flags_json=json.dumps(heuristics),
                    breakdown_json=json.dumps(risk_eval["breakdown"])
                )
                db.add(rec)
                db.commit()
                db.refresh(rec)
                record_id = rec.id
            except Exception:
                pass
            finally:
                db.close()

            return {
                "id": record_id,
                "scan_type": "text",
                "risk_score": risk_eval["composite_risk_score"],
                "risk_level": risk_eval["risk_level"],
                "verdict": risk_eval["verdict"],
                "confidence": ml_res["confidence"],
                "flags": heuristics,
                "breakdown": risk_eval["breakdown"],
                "recommendations": risk_eval["recommendations"],
                "input_preview": text[:300]
            }

    def scan_ocr(self, file_bytes: bytes, filename: str, company: Optional[str] = None, recruiter_email: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
        try:
            files = {"file": (filename, file_bytes, "image/png")}
            data = {}
            if company:
                data["claimed_company"] = company
            if recruiter_email:
                data["recruiter_email"] = recruiter_email

            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            resp = requests.post(f"{self.base_url}/scan/ocr", files=files, data=data, headers=headers, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            return {"error": resp.json().get("detail", "OCR analysis failed.")}
        except Exception:
            from backend.ai.ocr_engine import extract_text_from_image
            extracted = extract_text_from_image(file_bytes)
            res = self.scan_text(extracted, company, recruiter_email, token)
            res["scan_type"] = "ocr"
            res["extracted_text"] = extracted
            return res

    def scan_url(self, url: str, token: Optional[str] = None) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{self.base_url}/scan/url", json={"url": url}, headers=self._headers(token), timeout=8)
            if resp.status_code == 200:
                return resp.json()
            return {"error": resp.json().get("detail", "URL inspection failed.")}
        except Exception:
            from backend.services.url_scanner import scan_url_security
            return scan_url_security(url)

    # --- Verification ---
    def verify_company(self, company_name: str, domain: Optional[str] = None) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{self.base_url}/company/verify", json={"company_name": company_name, "offered_domain": domain}, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.services.company_verifier import verify_company as direct_verify
        return direct_verify(company_name, domain)

    def verify_recruiter(self, email: str, company: Optional[str] = None) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{self.base_url}/recruiter/verify", json={"email": email, "claimed_company": company}, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.services.recruiter_verifier import verify_recruiter_email as direct_recruiter
        return direct_recruiter(email, company)

    # --- Community Intelligence ---
    def get_community_reports(self) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(f"{self.base_url}/community/reports", timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import CommunityReport
        db = SessionLocal()
        try:
            reps = db.query(CommunityReport).filter(CommunityReport.status == "verified").order_by(CommunityReport.upvotes.desc()).all()
            return [
                {
                    "id": r.id,
                    "scam_title": r.scam_title,
                    "company_claimed": r.company_claimed,
                    "recruiter_contact": r.recruiter_contact,
                    "scam_description": r.scam_description,
                    "payment_demanded": r.payment_demanded,
                    "upvotes": r.upvotes,
                    "created_at": str(r.created_at)
                }
                for r in reps
            ]
        finally:
            db.close()

    def submit_community_report(self, title: str, company: str, contact: str, desc: str, payment: str, token: Optional[str] = None) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/community/reports",
                json={
                    "scam_title": title,
                    "company_claimed": company,
                    "recruiter_contact": contact,
                    "scam_description": desc,
                    "payment_demanded": payment
                },
                headers=self._headers(token),
                timeout=5
            )
            if resp.status_code == 201:
                return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import CommunityReport
        db = SessionLocal()
        try:
            r = CommunityReport(
                scam_title=title,
                company_claimed=company,
                recruiter_contact=contact,
                scam_description=desc,
                payment_demanded=payment,
                upvotes=1,
                status="verified"
            )
            db.add(r)
            db.commit()
            return {"id": r.id, "scam_title": r.scam_title}
        finally:
            db.close()

    def upvote_report(self, report_id: int) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{self.base_url}/community/reports/{report_id}/upvote", timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import CommunityReport
        db = SessionLocal()
        try:
            r = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
            if r:
                r.upvotes += 1
                db.commit()
                return {"id": r.id, "upvotes": r.upvotes}
            return {"error": "Report not found"}
        finally:
            db.close()

    # --- History ---
    def get_user_history(self, token: Optional[str] = None, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            if token:
                resp = requests.get(f"{self.base_url}/scan/history", headers=self._headers(token), timeout=5)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import ScanRecord
        db = SessionLocal()
        try:
            q = db.query(ScanRecord)
            if user_id:
                q = q.filter(ScanRecord.user_id == user_id)
            recs = q.order_by(ScanRecord.created_at.desc()).limit(30).all()
            return [
                {
                    "id": r.id,
                    "scan_type": r.scan_type,
                    "input_preview": r.input_preview,
                    "risk_score": r.risk_score,
                    "risk_level": r.risk_level,
                    "verdict": r.verdict,
                    "confidence": r.confidence,
                    "flags": json.loads(r.flags_json) if r.flags_json else [],
                    "breakdown": json.loads(r.breakdown_json) if r.breakdown_json else {},
                    "created_at": str(r.created_at)
                }
                for r in recs
            ]
        finally:
            db.close()

    # --- Admin Telemetry ---
    def get_admin_stats(self, token: Optional[str] = None) -> Dict[str, Any]:
        try:
            if token:
                resp = requests.get(f"{self.base_url}/admin/stats", headers=self._headers(token), timeout=5)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import User, ScanRecord, CommunityReport, VerifiedCompany, BlacklistEntry
        db = SessionLocal()
        try:
            return {
                "total_users": db.query(User).count(),
                "total_scans": db.query(ScanRecord).count(),
                "high_risk_scans": db.query(ScanRecord).filter(ScanRecord.risk_level.ilike("%high%")).count(),
                "medium_risk_scans": db.query(ScanRecord).filter(ScanRecord.risk_level.ilike("%medium%")).count(),
                "low_risk_scans": db.query(ScanRecord).filter(ScanRecord.risk_level.ilike("%low%")).count(),
                "total_community_reports": db.query(CommunityReport).count(),
                "verified_companies_count": db.query(VerifiedCompany).count(),
                "blacklisted_entries_count": db.query(BlacklistEntry).count()
            }
        finally:
            db.close()

    def get_blacklist(self, token: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            if token:
                resp = requests.get(f"{self.base_url}/admin/blacklist", headers=self._headers(token), timeout=5)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import BlacklistEntry
        db = SessionLocal()
        try:
            entries = db.query(BlacklistEntry).order_by(BlacklistEntry.created_at.desc()).all()
            return [
                {
                    "id": e.id,
                    "entry_type": e.entry_type,
                    "value": e.value,
                    "reason": e.reason,
                    "added_by": e.added_by,
                    "created_at": str(e.created_at)
                }
                for e in entries
            ]
        finally:
            db.close()

    def add_blacklist(self, entry_type: str, value: str, reason: str, token: Optional[str] = None) -> Dict[str, Any]:
        try:
            if token:
                resp = requests.post(
                    f"{self.base_url}/admin/blacklist",
                    json={"entry_type": entry_type, "value": value, "reason": reason},
                    headers=self._headers(token),
                    timeout=5
                )
                if resp.status_code == 201:
                    return resp.json()
        except Exception:
            pass
        from backend.database import SessionLocal
        from backend.models import BlacklistEntry
        db = SessionLocal()
        try:
            entry = BlacklistEntry(entry_type=entry_type, value=value, reason=reason, added_by="Admin Portal")
            db.add(entry)
            db.commit()
            return {"id": entry.id, "value": entry.value}
        finally:
            db.close()

api_client = JobShieldAPIClient()
