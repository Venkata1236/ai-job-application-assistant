"""
workflow.py
Defines the 5-node LangGraph workflow.
Each node either runs pure Python logic or
hands off to a CrewAI crew and stores results in state.
"""
import re
import json
from langgraph.graph import StateGraph, END
from state import JobAppState
from rag_pipeline import build_retriever
from agents import run_fit_analysis, run_cover_letter, run_resume_suggestions


# ── Node 1 ─────────────────────────────────────────────────────────
def retrieve_context(state: JobAppState) -> JobAppState:
    """Build FAISS index and retrieve top-4 relevant chunks."""
    retriever = build_retriever(state["jd_text"], state["cv_text"])
    docs = retriever.invoke(state["jd_text"])
    state["retrieved_chunks"] = [doc.page_content for doc in docs]
    return state


# ── Node 2 ─────────────────────────────────────────────────────────
def analyze_fit(state: JobAppState) -> JobAppState:
    """Hand off to CrewAI HR Analyst — stores fit_score and fit_analysis."""
    context = "\n\n".join(state["retrieved_chunks"])
    score, analysis = run_fit_analysis(
        state["cv_text"],
        state["jd_text"],
        context
    )
    state["fit_score"] = score
    state["fit_analysis"] = analysis
    return state


# ── Node 3 ─────────────────────────────────────────────────────────
def generate_cover_letter(state: JobAppState) -> JobAppState:
    """Hand off to CrewAI Writer — stores cover_letter."""
    letter = run_cover_letter(
        state["cv_text"],
        state["jd_text"],
        state["fit_analysis"]
    )
    state["cover_letter"] = letter
    return state


# ── Node 4 ─────────────────────────────────────────────────────────
def suggest_improvements(state: JobAppState) -> JobAppState:
    """Hand off to CrewAI Resume Coach — stores resume_suggestions."""
    gaps = ""
    try:
        json_match = re.search(r'\{.*\}', state["fit_analysis"], re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            gaps = ", ".join(data.get("gaps", []))
    except Exception:
        gaps = state["fit_analysis"][:300]

    suggestions = run_resume_suggestions(
        state["cv_text"],
        state["jd_text"],
        gaps
    )
    state["resume_suggestions"] = suggestions
    return state


# ── Node 5 ─────────────────────────────────────────────────────────
def compile_report(state: JobAppState) -> JobAppState:
    """Pure Python — combines all outputs into a markdown report."""
    score = state.get("fit_score", 0)

    if score >= 70:
        verdict = "Strong Match ✅"
    elif score >= 50:
        verdict = "Moderate Match ⚠️"
    else:
        verdict = "Needs Work ❌"

    state["final_report"] = f"""# AI Job Application Report

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
"""
    return state


# ── Graph Builder ──────────────────────────────────────────────────
def build_workflow():
    """
    Compile the full LangGraph workflow:
    retrieve_context → analyze_fit → generate_cover_letter
    → suggest_improvements → compile_report → END
    """
    graph = StateGraph(JobAppState)

    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("analyze_fit", analyze_fit)
    graph.add_node("generate_cover_letter", generate_cover_letter)
    graph.add_node("suggest_improvements", suggest_improvements)
    graph.add_node("compile_report", compile_report)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "analyze_fit")
    graph.add_edge("analyze_fit", "generate_cover_letter")
    graph.add_edge("generate_cover_letter", "suggest_improvements")
    graph.add_edge("suggest_improvements", "compile_report")
    graph.add_edge("compile_report", END)

    return graph.compile()