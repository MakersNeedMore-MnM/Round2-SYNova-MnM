# Assumption Gap

A hackathon MVP for finding hidden prerequisites in real-world processes before a user submits an application.

The MVP supports OpenAI-powered process analysis and a deterministic mock mode when no API key is configured.

## Stack

- React + Vite
- Tailwind CSS
- React Flow
- Python FastAPI
- Local JSON data

## Run locally

Use two terminals from the project root.

### 1. Start the API

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Health check: `http://localhost:8000/api/health`.

### AI endpoints

`POST /api/analyze-process` finds explicit requirements, hidden prerequisites, document dependencies, warnings, and a confidence score.

```json
{
	"process": "University Scholarship Application",
	"documents": ["FAQ: income certificates must be current"],
	"rejection_reasons": ["Rejected because proof of income was missing"]
}
```

`POST /api/preflight` checks a user's inputs and returns `PASS`, `WARNING`, or `BLOCKED`, along with missing requirements, explanations, recommended actions, and a risk score.

```json
{
	"process": "University Scholarship Application",
	"user_inputs": {"applicant_type": "undergraduate", "documents": ["transcript"]}
}
```

To use OpenAI, set `OPENAI_API_KEY` before starting the API. Optionally set `OPENAI_MODEL` (defaults to `gpt-4o-mini`). Without the key, the deterministic demo mode is used automatically. Never put the key in the frontend.

### 2. Start the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## MVP structure

```text
AssumptionGap/
|-- backend/
|   |-- data/process-document.json   # stated process instructions
|   |-- data/rejection-history.json  # historical rejection evidence
|   |-- data/faqs.json               # FAQ and support evidence
|   |-- data/sample-submissions.json # demo user submissions
|   |-- data/process.json             # assembled requirements and graph
|   |-- ai_service.py       # OpenAI integration and deterministic fallback
|   |-- main.py             # FastAPI endpoints and request models
|   `-- requirements.txt
|-- frontend/
|   |-- src/App.jsx         # checklist and dependency map
|   |-- src/styles.css
|   |-- src/main.jsx
|   |-- package.json
|   `-- vite.config.js
`-- README.md
```

