"""Vercel entrypoint: exposes the FastAPI app as `app`."""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.main import app  # noqa: E402,F401
