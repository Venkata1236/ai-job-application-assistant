# 💼 AI Job Application Assistant

> End-to-end AI pipeline — LangGraph + CrewAI + RAG + FastAPI + Streamlit + Docker + AWS

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-yellow)
![CrewAI](https://img.shields.io/badge/CrewAI-Latest-purple)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![AWS](https://img.shields.io/badge/AWS-ECS%20Fargate-orange)

---

## 📌 What Is This?

An AI-powered job application assistant that analyzes your CV against any job description and generates a fit score, tailored cover letter, and resume improvement suggestions — all in one pipeline. Built using LangGraph for workflow orchestration, CrewAI with YAML-configured agents for role-based reasoning, FAISS for RAG-based context retrieval, and FastAPI + Streamlit for a fully deployable backend and UI.

---

## 🗺️ Simple Flow
```
User uploads CV + pastes Job Description
              ↓
     Streamlit calls POST /analyze
              ↓
     FastAPI triggers LangGraph workflow
              ↓
  Node 1: FAISS RAG — retrieve relevant chunks
              ↓
  Node 2: CrewAI HR Analyst — fit score + gaps
              ↓
  Node 3: CrewAI Writer — tailored cover letter
              ↓
  Node 4: CrewAI Coach — resume suggestions
              ↓
  Node 5: Compile final markdown report
              ↓
    Streamlit renders score + tabs + downloads
```

---

## 📁 Project Structure
```
ai-job-application-assistant/
├── backend/
│   ├── config/
│   │   ├── agents.yaml          ← CrewAI agent definitions (YAML)
│   │   └── tasks.yaml           ← CrewAI task definitions (YAML)
│   ├── main.py                  ← FastAPI — /health + /analyze endpoints
│   ├── workflow.py              ← LangGraph 5-node workflow
│   ├── agents.py                ← Loads agents + tasks from YAML
│   ├── rag_pipeline.py          ← FAISS vector store + retriever
│   ├── state.py                 ← LangGraph TypedDict state schema
│   ├── models.py                ← Pydantic response models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py                   ← Streamlit UI with tabs + downloads
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔗 API Endpoints

| Method | Endpoint | Type | Description |
|---|---|---|---|
| GET | `/health` | Normal | Health check |
| POST | `/analyze` | Normal | Full CV + JD analysis pipeline |

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| `LangGraph StateGraph` | Orchestrates 5-node workflow, manages shared state |
| `CrewAI YAML Config` | Agents and tasks defined in YAML, loaded at runtime |
| `FAISS RAG` | Indexes CV + JD, retrieves top-4 relevant chunks |
| `HR Analyst Agent` | Scores candidate fit 0–100, identifies skill gaps |
| `Cover Letter Agent` | Writes tailored 3-paragraph cover letter |
| `Resume Coach Agent` | Provides 6 ATS-optimized improvement suggestions |
| `pdfplumber` | Extracts text from uploaded PDF CVs |

---

## ⚙️ Local Setup
```bash
git clone https://github.com/Venkata1236/ai-job-application-assistant
cd ai-job-application-assistant
cp .env.example .env
```

Add `.env`:
```
OPENAI_API_KEY=your_key_here
```

Run with Docker Compose:
```bash
docker-compose up --build
```

Or run manually:
```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
pip install -r requirements.txt
python -m streamlit run app.py
```

- Frontend → http://localhost:8501
- Backend API docs → http://localhost:8000/docs

---

## ☁️ AWS Deployment (ECS Fargate)
```bash
# Push backend to ECR
aws ecr create-repository --repository-name job-assistant-backend
docker build -t job-assistant-backend ./backend
docker tag job-assistant-backend:latest .dkr.ecr..amazonaws.com/job-assistant-backend:latest
docker push .dkr.ecr..amazonaws.com/job-assistant-backend:latest

# Push frontend to ECR
aws ecr create-repository --repository-name job-assistant-frontend
docker build -t job-assistant-frontend ./frontend
docker tag job-assistant-frontend:latest .dkr.ecr..amazonaws.com/job-assistant-frontend:latest
docker push .dkr.ecr..amazonaws.com/job-assistant-frontend:latest

# Store secret
aws secretsmanager create-secret \
  --name job-assistant/openai-key \
  --secret-string '{"OPENAI_API_KEY":"your_key_here"}'

# Create ECS cluster
aws ecs create-cluster --cluster-name job-assistant-cluster
```

---

## 📦 Tech Stack

- **LangGraph** — 5-node workflow orchestration with shared TypedDict state
- **CrewAI** — YAML-configured multi-agent system (HR Analyst, Writer, Coach)
- **FAISS** — Vector store for RAG-based context retrieval
- **FastAPI** — REST API backend with PDF parsing
- **Streamlit** — Interactive UI with score bar, tabs, and file downloads
- **Docker** — Containerized backend + frontend with bridge network
- **AWS ECS Fargate** — Serverless cloud deployment with Secrets Manager

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)