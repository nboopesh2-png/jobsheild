"""
Configuration settings for JobShield AI.
Loads settings from environment variables with safe defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

PROJECT_NAME: str = os.getenv("PROJECT_NAME", "JobShield AI")
VERSION: str = os.getenv("VERSION", "1.0.0")
API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
API_PORT: int = int(os.getenv("API_PORT", "8000"))

SECRET_KEY: str = os.getenv("SECRET_KEY", "jobshield-cybersecurity-super-secret-jwt-key-2025")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Database URL
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./jobshield.db")

# External APIs
VIRUSTOTAL_API_KEY: str = os.getenv("VIRUSTOTAL_API_KEY", "")
GOOGLE_SAFE_BROWSING_KEY: str = os.getenv("GOOGLE_SAFE_BROWSING_KEY", "")
