"""
main.py
FastAPI entry point — /health and /analyze endpoints.
"""
import io
import os
import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AnalysisResponse
from workflow import build_workflow

load_dotenv()
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

app = FastAPI(
    title="AI Job Application Assistant",
    description="LangGraph + CrewAI + RAG — 6-module career intelligence pipeline",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Job Application Assistant", "version": "2.0.0"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_application(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await cv_file.read()
    cv_text = ""

    if cv_file.filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                cv_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")
    else:
        try:
            cv_text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Unsupported encoding. Use PDF or UTF-8 TXT.")

    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in CV.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    try:
        workflow = build_workflow()
        result = workflow.invoke({
            "cv_text": cv_text,
            "jd_text": job_description,
            "retrieved_chunks": [],
            "fit_score": 0,
            "fit_analysis": "",
            "cover_letter": "",
            "resume_suggestions": "",
            "interview_questions": "",
            "linkedin_summary": "",
            "keywords": "",
            "final_report": ""
        })

        return AnalysisResponse(
            fit_score=result["fit_score"],
            fit_analysis=result["fit_analysis"],
            cover_letter=result["cover_letter"],
            resume_suggestions=result["resume_suggestions"],
            interview_questions=result["interview_questions"],
            linkedin_summary=result["linkedin_summary"],
            keywords=result["keywords"],
            final_report=result["final_report"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {str(e)}")