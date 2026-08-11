# WEB Calc

A web-based calculator — standard and scientific modes — built as a sample project
to exercise SDLC governance tooling (traceability across GUI, API, and DB layers).

## Structure

```
web-calc/
├── backend/     FastAPI service — arithmetic + scientific calculation endpoints, SQLite history
├── frontend/    Static HTML/CSS/JS calculator UI (standard + scientific modes)
├── tests/       Pytest unit/integration tests for the backend API
└── automation/  Standalone test automation framework (API + E2E + perf)
```

## Running locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `frontend/index.html` in a browser (or serve it with any static file server).

## Jira

Tracked under project `WEBCALC` — epics: Standard Calculator, Scientific Calculator, Test Automation.
