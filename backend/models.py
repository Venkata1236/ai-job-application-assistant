"""
models.py
Pydantic response models for FastAPI endpoints.
"""
from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    fit_score: int
    fit_analysis: str
    cover_letter: str
    resume_suggestions: str
    final_report: str