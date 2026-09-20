# Round2-SYNova-MnM

Repository for team SYNova MnM for Round 2.

## Assumption Gap

A hackathon MVP for finding hidden prerequisites in real-world processes before a user submits an application.

The MVP supports OpenAI-powered process analysis and a deterministic mock mode when no API key is configured.

## Stack

* React + Vite
* Tailwind CSS
* React Flow
* Python FastAPI
* Local JSON data

## Run Locally

Use two terminals from the project root.

### 1. Start the API

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API is available at `http://localhost:8000`.

Health check:

`http://localhost:8000/api/health`

### AI Endpoints

`POST /api/analyze-process` finds explicit requirements, hidden prerequisites, document dependencies, warnings, and a confidence score.

`POST /api/preflight` checks a user's inputs and returns `PASS`, `WARNING`, or `BLOCKED`, along with missing requirements, explanations, recommended actions, and a risk score.

To use OpenAI, set `OPENAI_API_KEY` before starting the API. Optionally set `OPENAI_MODEL`. Without the key, deterministic demo mode is used automatically.

Never put the API key in the frontend.

### 2. Start the Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open:

`http://localhost:5173`

## MVP Structure

```text
AssumptionGap/
├── backend/
│   ├── data/
│   │   ├── process-document.json
│   │   ├── rejection-history.json
│   │   ├── faqs.json
│   │   ├── sample-submissions.json
│   │   └── process.json
│   ├── ai_service.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── styles.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
└── README.md
```
