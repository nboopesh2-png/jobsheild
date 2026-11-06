"""
Unified Application Launcher for JobShield AI.
Can launch FastAPI backend, Streamlit frontend, or both concurrently.

Usage:
    python run.py                # Launches both FastAPI (port 8000) and Streamlit (port 8501)
    python run.py --backend      # Launches only the FastAPI backend
    python run.py --frontend     # Launches only the Streamlit frontend
"""
import sys
import os
import subprocess
import argparse
import time

def run_backend():
    """Runs FastAPI backend using uvicorn."""
    import uvicorn
    from backend.config import API_HOST, API_PORT
    print(f"[*] Starting JobShield AI FastAPI Backend on http://{API_HOST}:{API_PORT} ...")
    uvicorn.run("backend.main:app", host=API_HOST, port=API_PORT, reload=True)

def run_frontend():
    """Runs Streamlit frontend."""
    from backend.config import API_PORT
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    print(f"[*] Starting JobShield AI Streamlit Frontend on http://localhost:8501 ...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", frontend_path, "--server.port=8501"])

def run_all():
    """Runs both backend and frontend concurrently."""
    import threading
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    time.sleep(2)  # Give backend 2 seconds to initialize DB and startup
    run_frontend()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JobShield AI Platform Launcher")
    parser.add_argument("--backend", action="store_true", help="Launch FastAPI backend only")
    parser.add_argument("--frontend", action="store_true", help="Launch Streamlit frontend only")
    args = parser.parse_args()

    if args.backend:
        run_backend()
    elif args.frontend:
        run_frontend()
    else:
        run_all()
