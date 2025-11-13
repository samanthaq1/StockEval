# Backend (FastAPI) — mock allocation endpoint

This folder contains a minimal FastAPI mock used by the frontend during development.

Endpoints:
- `POST /api/allocate` — accepts JSON `{ "amount": number, "risk": "conservative"|"balanced"|"aggressive" }` and returns mock allocations.

Run locally (PowerShell):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The CORS middleware allows requests from `http://localhost:5173` (Vite dev server).
