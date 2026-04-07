"""
state.py
LangGraph TypedDict state schema — all workflow node outputs.
"""
from typing import TypedDict, List


class JobAppState(TypedDict):
    cv_text: str
    jd_text: str
    retrieved_chunks: List[str]
    fit_score: int
    fit_analysis: str
    cover_letter: str
    resume_suggestions: str
    interview_questions: str
    linkedin_summary: str
    keywords: str
    final_report: str