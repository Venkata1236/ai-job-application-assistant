"""
agents.py
Loads CrewAI agent and task definitions from YAML config files.
Each function is called by a LangGraph workflow node.
"""
import os
import re
import json
import yaml
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# ── Load YAML configs ──────────────────────────────────────────────
CONFIG_DIR = Path(__file__).parent / "config"

with open(CONFIG_DIR / "agents.yaml", "r") as f:
    AGENTS_CONFIG = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r") as f:
    TASKS_CONFIG = yaml.safe_load(f)


# ── Helpers ────────────────────────────────────────────────────────
def _get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def _build_agent(agent_key: str) -> Agent:
    cfg = AGENTS_CONFIG[agent_key]
    return Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        llm=_get_llm(),
        verbose=cfg.get("verbose", False),
        allow_delegation=cfg.get("allow_delegation", False)
    )


def _build_task(task_key: str, agent: Agent, **kwargs) -> Task:
    cfg = TASKS_CONFIG[task_key]
    description = cfg["description"].format(**kwargs)
    return Task(
        description=description,
        agent=agent,
        expected_output=cfg["expected_output"]
    )


def _run_crew(agent_key: str, task_key: str, **kwargs) -> str:
    agent = _build_agent(agent_key)
    task = _build_task(task_key, agent, **kwargs)
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    return str(crew.kickoff())


# ── Agent Functions ────────────────────────────────────────────────
def run_fit_analysis(cv_text: str, jd_text: str, context: str) -> tuple:
    """CrewAI HR Analyst — returns (score, analysis_text)"""
    result = _run_crew(
        "hr_analyst", "fit_analysis_task",
        cv_text=cv_text[:3000],
        jd_text=jd_text[:2000],
        context=context
    )
    score = 0
    try:
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            score = int(data.get("score", 0))
    except Exception:
        pass
    return score, result


def run_cover_letter(cv_text: str, jd_text: str, fit_analysis: str) -> str:
    """CrewAI Cover Letter Writer"""
    return _run_crew(
        "cover_letter_writer", "cover_letter_task",
        cv_text=cv_text[:2000],
        jd_text=jd_text[:2000],
        fit_analysis=fit_analysis[:600]
    )


def run_resume_suggestions(cv_text: str, jd_text: str, gaps: str) -> str:
    """CrewAI Resume Coach"""
    return _run_crew(
        "resume_coach", "resume_suggestions_task",
        cv_text=cv_text[:2000],
        jd_text=jd_text[:1500],
        gaps=gaps
    )


def run_interview_questions(cv_text: str, jd_text: str, fit_analysis: str) -> str:
    """CrewAI Interview Coach — generates 7 likely interview questions"""
    return _run_crew(
        "interview_coach", "interview_questions_task",
        cv_text=cv_text[:2000],
        jd_text=jd_text[:2000],
        fit_analysis=fit_analysis[:600]
    )


def run_linkedin_summary(cv_text: str, jd_text: str) -> str:
    """CrewAI LinkedIn Writer — headline + about section"""
    return _run_crew(
        "linkedin_writer", "linkedin_summary_task",
        cv_text=cv_text[:2000],
        jd_text=jd_text[:1500]
    )


def run_keywords(cv_text: str, jd_text: str) -> str:
    """CrewAI Keywords Extractor — ATS keyword analysis"""
    return _run_crew(
        "keywords_extractor", "keywords_task",
        cv_text=cv_text[:2000],
        jd_text=jd_text[:1500]
    )