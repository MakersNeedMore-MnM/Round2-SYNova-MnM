# Round2-SYNova-MnM

Repository for team SYNova MnM for Round 2.

# Assumption Gap

AI that uncovers hidden prerequisites inside real-world processes before users discover them by failing.

Assumption Gap is a process-intelligence MVP that identifies hidden prerequisites in real-world application processes. It uses past failures, rejection records, FAQs, and process documents to identify requirements, understand their dependencies, and check whether a user is ready before submitting an application.

The goal is to help users identify missing requirements early and avoid preventable rejection, rework, and delays.

# Problem Statement

Real-world processes are often documented, but their dependencies are not always clear.

A user may follow the visible instructions and still get rejected because the process requires an additional document, approval, endorsement, verification, or other prerequisite.

These hidden requirements can lead to failed submissions, repeated applications, delays, and increased support requests.

Assumption Gap identifies these hidden prerequisites before submission and helps the user understand what needs to be completed first.

# Key Features

## Pre-Flight Check

Users can check their current application status against the discovered prerequisites before submitting.

The system provides three possible results:

PASS: Ready to submit

WARNING: Review before submitting

BLOCKED: Fix the missing prerequisite first

## AI Process Assessment

The system identifies explicit requirements, hidden prerequisites, document dependencies, potential blockers, confidence levels, and supporting evidence.

## Dependency Graph

The dependency graph shows how prerequisites are connected and what downstream steps may be affected when a requirement is missing.

## Explainable Results

The system provides an explanation for discovered requirements along with confidence and evidence information.

## Risk Assessment

The pre-flight check provides a risk score based on the current application state and identified missing requirements.

## Multiple Processes

The prototype can demonstrate the same process intelligence pattern across different workflows such as university scholarship applications, internship applications, and student loan applications.

# How It Works

Past failures, rejection records, FAQs, and process documents are used as input.

The system extracts requirements and relevant information.

Related information is reconciled to identify dependencies and possible conflicts.

A dependency graph is created from the discovered requirements.

The user's current application state is compared against the identified prerequisites.

The system provides a final pre-flight result showing whether the application can proceed or whether something needs to be fixed first.

# Demo

The main demonstration uses a university scholarship application.

In the example, the income certificate is not available.

The system identifies the missing document as a prerequisite and returns a BLOCKED result.

The demonstration shows a 94% confidence level and a risk score of 28 out of 100.

The user can then understand the missing prerequisite and its impact before submitting the application.

# Tech Stack

Frontend

React

Vite

Tailwind CSS

React Flow

Backend

Python

FastAPI

AI

OpenAI API

A deterministic demo mode is also available when an API key is not configured.

Data

Local JSON data

Process documents

Rejection history

FAQs

Sample submissions

# How to Run

## Backend

Open a terminal from the project root and run:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at:

http://localhost:8000

Health check:

http://localhost:8000/api/health

## Frontend

Open a second terminal and run:

```powershell
cd frontend
npm install
npm run dev
```

The frontend will be available at:

http://localhost:5173

## AI Configuration

To enable OpenAI-powered analysis, configure the OPENAI_API_KEY environment variable before starting the backend.

OPENAI_MODEL can also be configured if required.

The application can run in deterministic demo mode when an API key is not configured.

# Project Structure

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
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── styles.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
└── README.md
```

# Team

Team Lead

Yashwini Priya Prabhu

Team Members

Neya Ramanan Raja

R Shrinidhi

Team

SYNova MnM

# Demo Details

The project demonstration includes the pre-flight check, application assessment, missing prerequisite detection, dependency graph, confidence information, evidence source, and risk assessment.

The main objective of the demo is to identify the hidden requirement before the user reaches the point of rejection.

# Core Principle

Don't predict failure. Explain the prerequisite that prevents it.

Assumption Gap

From Failure to Foresight
