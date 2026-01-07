# PatchPilot (AI Code Reviewer)

Paste code and get a detailed review: bugs, security issues, performance concerns, readability improvements, and refactor suggestions — including "Before/After" snippets.

## Tech
- Frontend: React + TypeScript + Vite
- Backend: FastAPI (Python)
- AI: OpenAI SDK (configurable model)

## Quickstart (local)

### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="YOUR_KEY"
export OPENAI_MODEL="gpt-4o-mini"   # optional
export ALLOWED_ORIGINS="http://localhost:5173"  # optional

uvicorn app.main:app --reload --port 8000
