# JOBSHIELD AI 🛡️
### AI-Powered Fake Job Offer & Internship Scam Detector
> **Tagline:** Detect Fake Offers. Protect Your Future.  
> **Developed for:** Final Year College Project & Student Recruitment Fraud Awareness Initiative.

---

## 📌 Executive Summary
**JobShield AI** is an enterprise-grade cybersecurity web application built primarily in Python to combat the escalating threat of recruitment fraud, fake internship postings, upfront fee extortion schemes, and corporate impersonation targeting university students and fresh graduates.

By unifying **Natural Language Processing (NLP)**, **Machine Learning (TF-IDF + Logistic Regression)**, **Computer Vision OCR**, **Heuristic Detection Rules**, **Enterprise Domain Verification**, and **Bilingual Tamil & English Support**, JobShield AI delivers instantaneous forensic risk audits with explainable threat signals and cryptographic PDF certification.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend UI** | Python Streamlit, Custom Cyber CSS Design System, Plotly Charts |
| **Backend REST API**| Python FastAPI, Uvicorn ASGI Server, Pydantic v2 |
| **AI / Machine Learning** | Scikit-Learn (`TfidfVectorizer`, `LogisticRegression`), NLTK, Feature Importance (XAI) |
| **Computer Vision / OCR** | EasyOCR, Pillow Image Filtering, Contrast Enhancement |
| **Database & ORM** | MySQL (Production) / SQLite (Zero-Setup Auto Fallback), SQLAlchemy 2.0 |
| **Security & Auth** | JWT Authentication (`python-jose`), PBKDF2-HMAC Salted Hashing |
| **Audit Reports** | ReportLab PDF Generation |
| **External Security** | VirusTotal API v3, Google Safe Browsing (with local heuristic engine fallback) |

---

## 🚀 Key Modules (14/14 Implemented)

1. **User Authentication & RBAC**: Student and Administrator roles, JWT token management, secure password hashing.
2. **Student Dashboard**: Live risk distribution doughnut chart, genuine database detection metrics, quick actions.
3. **AI Job Offer Text Scanner**: Dual evaluation (ML prediction + 10 heuristic rules) with dynamic risk gauge and token highlights.
4. **Screenshot OCR Scanner**: Image preprocessing, contrast enhancement, text extraction from offer letters, WhatsApp chats, and Telegram screenshots.
5. **URL Security & Phishing Scanner**: Analyzes suspicious TLDs (`.xyz`, `.top`), IP hosting, typo-squatting, and VirusTotal reputation.
6. **Company Verification**: Cross-references employers against verified tier-1 enterprise registries (TCS, Infosys, Google, etc.) and detects lookalike typo-squatted domains (e.g., `tcs-careers-interview.online`).
7. **Recruiter Identity Verification**: Flags generic public mailboxes (`@gmail.com`, `@yahoo.com`) used by purported corporate HRs and detects burner/disposable email services.
8. **Composite AI Risk Score Generator**: Multi-factor 0–100% scoring with automated risk categorization (Low, Medium, High/Critical).
9. **Analysis History**: Persists every scan with full parameters, enabling students to review findings and re-download forensic audits.
10. **Community Scam Reporting Feed**: Crowdsourced threat intelligence where students report new scam patterns and upvote active alerts.
11. **Admin Control Center**: Telemetry metrics, threat indicator blacklist management, registered user audit, and ML model status.
12. **Bilingual Localization (English & தமிழ்)**: Instant UI toggle across all 14 modules with detection of regional Tamil scam lures.
13. **Forensic PDF Audit Report Generator**: ReportLab compilation of branded PDF audit certificates with risk meters and helpline references.
14. **Dual Database Architecture**: Seamless MySQL integration with automatic SQLite fallback for zero-configuration execution.

---

## ⚙️ Installation & Quickstart

### 1. Prerequisites
- Python 3.10 - 3.12 (3.14 is NOT recommended: some packages have no wheels yet).
- Optional: MySQL Server (if using MySQL; otherwise SQLite runs out of the box).

### 2. Install Dependencies
```bash
cd jobshield_ai
pip install -r requirements-local.txt
```

### 3. Launch JobShield AI

#### Option A: Unified Launcher (Runs both Backend & Frontend)
```bash
python run.py
```
- **FastAPI Backend:** `http://127.0.0.1:8000` (API Docs: `http://127.0.0.1:8000/docs`)
- **Streamlit Frontend:** `http://localhost:8501`

#### Option B: Launch Frontend Only
```bash
streamlit run frontend/app.py
```

#### Option C: Launch Backend API Only
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🔑 Demo Access Credentials

The database automatically seeds test accounts on the first run:

| Role | Email | Password | Purpose |
|---|---|---|---|
| **Student** | `student@college.edu` | `Student@123456` | Student Dashboard, History, Scanners |
| **Administrator** | `admin@jobshield.ai` | `Admin@123456` | Admin Control Center, Blacklist Curation |

*(You can also register any new student account directly through the registration form)*

---

## 🗄️ Database Configuration (MySQL / SQLite)

In `.env`:
```env
# Default: Zero-setup SQLite
DATABASE_URL="sqlite:///./jobshield.db"

# Or configure MySQL:
# DATABASE_URL="mysql+pymysql://root:yourpassword@localhost:3306/jobshield_db"
```
*Note: If MySQL is configured but the MySQL server is unreachable, JobShield AI automatically falls back to local SQLite without crashing.*

---

## 🧪 Automated Test Suite
To verify all AI models, rules, verification services, and PDF generators:
```bash
python tests/test_jobshield.py
```

---

## 🛡️ National Cyber Crime Awareness
If you or someone you know has been targeted by recruitment fraud:
- **Toll-Free Helpline:** Dial **1930**
- **National Portal:** [https://cybercrime.gov.in](https://cybercrime.gov.in)

---

## ☁️ Deploying with GitHub + Vercel

Vercel runs **serverless functions only**, so Streamlit (a long-running websocket server) cannot run there.
Use this split:

| Part | Where | Entry |
|---|---|---|
| FastAPI backend | **Vercel** | `api/index.py` + `vercel.json` |
| Streamlit frontend | **Streamlit Community Cloud** (free, from the same GitHub repo) | `frontend/app.py` |
| Database | Hosted Postgres (Neon / Supabase) | `DATABASE_URL` |

1. Push this folder to GitHub (`.env` is git-ignored — never commit it).
2. Vercel → *Add New Project* → import the repo → Framework: **Other**. Add Environment Variables:
   `SECRET_KEY` (random), `DATABASE_URL` (Postgres URL; without it SQLite in `/tmp` is used and data resets), optional `VIRUSTOTAL_API_KEY`.
3. Deploy, then open `https://YOUR-PROJECT.vercel.app/api/health` — it should return `{"status":"healthy"...}`.
4. share.streamlit.io → New app → same repo, main file `frontend/app.py`. In *Secrets* add
   `API_BASE_URL = "https://YOUR-PROJECT.vercel.app"`.
