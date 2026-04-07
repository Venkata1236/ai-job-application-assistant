"""
workflow.py
LangGraph 8-node workflow — each node calls a CrewAI agent or pure Python.
"""
import re
import json
from langgraph.graph import StateGraph, END
from state import JobAppState
from rag_pipeline import build_retriever
from agents import (
    run_fit_analysis, run_cover_letter, run_resume_suggestions,
    run_interview_questions, run_linkedin_summary, run_keywords
)


def retrieve_context(state: JobAppState) -> JobAppState:
    """Node 1: FAISS RAG — retrieve top-4 relevant chunks."""
    retriever = build_retriever(state["jd_text"], state["cv_text"])
    docs = retriever.invoke(state["jd_text"])
    state["retrieved_chunks"] = [doc.page_content for doc in docs]
    return state


def analyze_fit(state: JobAppState) -> JobAppState:
    """Node 2: CrewAI HR Analyst — fit score + gap analysis."""
    context = "\n\n".join(state["retrieved_chunks"])
    score, analysis = run_fit_analysis(state["cv_text"], state["jd_text"], context)
    state["fit_score"] = score
    state["fit_analysis"] = analysis
    return state


def generate_cover_letter(state: JobAppState) -> JobAppState:
    """Node 3: CrewAI Writer — tailored cover letter."""
    state["cover_letter"] = run_cover_letter(
        state["cv_text"], state["jd_text"], state["fit_analysis"]
    )
    return state


def suggest_improvements(state: JobAppState) -> JobAppState:
    """Node 4: CrewAI Resume Coach — improvement suggestions."""
    gaps = ""
    try:
        json_match = re.search(r'\{.*\}', state["fit_analysis"], re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            gaps = ", ".join(data.get("gaps", []))
    except Exception:
        gaps = state["fit_analysis"][:300]
    state["resume_suggestions"] = run_resume_suggestions(
        state["cv_text"], state["jd_text"], gaps
    )
    return state


def generate_interview_questions(state: JobAppState) -> JobAppState:
    """Node 5: CrewAI Interview Coach — 7 interview questions."""
    state["interview_questions"] = run_interview_questions(
        state["cv_text"], state["jd_text"], state["fit_analysis"]
    )
    return state


def generate_linkedin_summary(state: JobAppState) -> JobAppState:
    """Node 6: CrewAI LinkedIn Writer — headline + about section."""
    state["linkedin_summary"] = run_linkedin_summary(
        state["cv_text"], state["jd_text"]
    )
    return state


def extract_keywords(state: JobAppState) -> JobAppState:
    """Node 7: CrewAI Keywords Extractor — ATS keyword analysis."""
    state["keywords"] = run_keywords(state["cv_text"], state["jd_text"])
    return state


def compile_report(state: JobAppState) -> JobAppState:
    """Node 8: Pure Python — compile final markdown report."""
    score = state.get("fit_score", 0)
    verdict = (
        "Strong Match ✅" if score >= 70
        else "Moderate Match ⚠️" if score >= 50
        else "Needs Work ❌"
    )
    state["final_report"] = f"""# AI Job Application Intelligence Report

## Fit Score: {score}/100 — {verdict}

---

## 📊 Fit Analysis
{state.get("fit_analysis", "")}

---

## 📝 Tailored Cover Letter
{state.get("cover_letter", "")}

---

## 🔧 Resume Improvements
{state.get("resume_suggestions", "")}

---

## 🎯 Interview Preparation
{state.get("interview_questions", "")}

---

## 💼 LinkedIn Optimization
{state.get("linkedin_summary", "")}

---

## 🔑 ATS Keywords
{state.get("keywords", "")}
"""
    return state


def build_workflow():
    """Compile the full 8-node LangGraph workflow."""
    graph = StateGraph(JobAppState)

    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("analyze_fit", analyze_fit)
    graph.add_node("generate_cover_letter", generate_cover_letter)
    graph.add_node("suggest_improvements", suggest_improvements)
    graph.add_node("generate_interview_questions", generate_interview_questions)
    graph.add_node("generate_linkedin_summary", generate_linkedin_summary)
    graph.add_node("extract_keywords", extract_keywords)
    graph.add_node("compile_report", compile_report)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "analyze_fit")
    graph.add_edge("analyze_fit", "generate_cover_letter")
    graph.add_edge("generate_cover_letter", "suggest_improvements")
    graph.add_edge("suggest_improvements", "generate_interview_questions")
    graph.add_edge("generate_interview_questions", "generate_linkedin_summary")
    graph.add_edge("generate_linkedin_summary", "extract_keywords")
    graph.add_edge("extract_keywords", "compile_report")
    graph.add_edge("compile_report", END)

    return graph.compile()