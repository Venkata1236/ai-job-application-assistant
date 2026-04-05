from typing import TypedDict, List


class JobAppState(TypedDict):
    cv_text: str
    jd_text: str
    retrieved_chunks: List[str]
    fit_score: int
    fit_analysis: str
    cover_letter: str
    resume_suggestions: str
    final_report: str