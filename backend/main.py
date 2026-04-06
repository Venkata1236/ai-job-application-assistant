"""
main.py
FastAPI application entry point.
"""
import io
import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AnalysisResponse
from workflow import build_workflow

# ── Load environment variables ─────────────────────────────────────
load_dotenv()

app = FastAPI(
    title="AI Job Application Assistant",
    description="LangGraph + CrewAI + RAG powered job application analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ───────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Job Application Assistant",
        "version": "1.0.0"
    }


# ── Main Endpoint ──────────────────────────────────────────────────
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_application(
    cv_file: UploadFile = File(..., description="CV in PDF or TXT format"),
    job_description: str = Form(..., description="Full job description text")
):
    """
    Full pipeline:
    1. Extract text from uploaded CV (PDF or TXT)
    2. RAG — index CV + JD, retrieve relevant chunks
    3. CrewAI HR Analyst — fit score + gap analysis
    4. CrewAI Writer — tailored cover letter
    5. CrewAI Resume Coach — improvement suggestions
    6. Compile and return structured markdown report
    """

    # ── Step 1: Extract CV text ────────────────────────────────────
    content = await cv_file.read()
    cv_text = ""

    if cv_file.filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                cv_text = "\n".join(
                    page.extract_text() or "" for page in pdf.pages
                )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse PDF: {str(e)}"
            )
    else:
        try:
            cv_text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file encoding. Please use PDF or UTF-8 TXT."
            )

    # ── Step 2: Validate inputs ────────────────────────────────────
    if not cv_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in CV."
        )
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    # ── Step 3: Run LangGraph workflow ─────────────────────────────
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
            "final_report": ""
        })

        return AnalysisResponse(
            fit_score=result["fit_score"],
            fit_analysis=result["fit_analysis"],
            cover_letter=result["cover_letter"],
            resume_suggestions=result["resume_suggestions"],
            final_report=result["final_report"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Workflow execution failed: {str(e)}"
        )