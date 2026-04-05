💼 AI Job Application Assistant

An end-to-end AI system that analyzes your CV against a job description and generates:
- **Fit Score** (0–100) with detailed gap analysis
- **Tailored Cover Letter**
- **Resume Improvement Suggestions**

## 🏗️ Architecture
Streamlit UI → FastAPI → LangGraph Workflow
├── Node 1: RAG (FAISS) — context retrieval
├── Node 2: CrewAI HR Analyst — fit scoring
├── Node 3: CrewAI Writer — cover letter
├── Node 4: CrewAI Coach — resume tips
└── Node 5: Compile final report

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Workflow Orchestration | LangGraph |
| AI Agents | CrewAI (YAML config) |
| Vector Store | FAISS |
| API | FastAPI |
| UI | Streamlit |
| Containerization | Docker |
| Cloud | AWS ECS Fargate |

## 📁 Project Structure
ai-job-application-assistant/
├── backend/
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── main.py
│   ├── workflow.py
│   ├── agents.py
│   ├── rag_pipeline.py
│   ├── state.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md

## 🚀 Local Setup

### 1. Clone and configure
```bash
git clone https://github.com/Venkata1236/ai-job-application-assistant
cd ai-job-application-assistant
cp .env.example .env
# Add your OPENAI_API_KEY inside .env
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```

- Frontend → http://localhost:8501
- Backend API docs → http://localhost:8000/docs

## ☁️ AWS Deployment

### Step 1 — Push images to ECR
```bash
aws ecr create-repository --repository-name job-assistant-backend
docker build -t job-assistant-backend ./backend
docker tag job-assistant-backend:latest <account_id>.dkr.ecr.<region>.amazonaws.com/job-assistant-backend:latest
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/job-assistant-backend:latest

aws ecr create-repository --repository-name job-assistant-frontend
docker build -t job-assistant-frontend ./frontend
docker tag job-assistant-frontend:latest <account_id>.dkr.ecr.<region>.amazonaws.com/job-assistant-frontend:latest
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/job-assistant-frontend:latest
```

### Step 2 — Store secret in Secrets Manager
```bash
aws secretsmanager create-secret \
  --name job-assistant/openai-key \
  --secret-string '{"OPENAI_API_KEY":"your_key_here"}'
```

### Step 3 — Create ECS cluster and services
```bash
aws ecs create-cluster --cluster-name job-assistant-cluster
```
- Backend task: ECR backend image, port 8000, env from Secrets Manager
- Frontend task: ECR frontend image, port 8501, API_URL = backend ALB DNS