"""
agents.py
Loads CrewAI agent and task definitions from YAML config files.
Each function is called by a LangGraph workflow node.
"""
import re
import json
import yaml
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

load_dotenv()

# ── Load YAML configs ──────────────────────────────────────────────
CONFIG_DIR = Path(__file__).parent / "config"

with open(CONFIG_DIR / "agents.yaml", "r") as f:
    AGENTS_CONFIG = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r") as f:
    TASKS_CONFIG = yaml.safe_load(f)


# ── Helpers ────────────────────────────────────────────────────────
def _get_llm():
    """Lazy load LLM — only created when first called."""
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def _build_agent(agent_key: str) -> Agent:
    """Instantiate a CrewAI Agent from YAML config."""
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
    """Instantiate a CrewAI Task from YAML config with runtime variables."""
    cfg = TASKS_CONFIG[task_key]
    description = cfg["description"].format(**kwargs)
    return Task(
        description=description,
        agent=agent,
        expected_output=cfg["expected_output"]
    )


# ── Agent Functions (called by LangGraph nodes) ────────────────────
def run_fit_analysis(cv_text: str, jd_text: str, context: str) -> tuple:
    """
    CrewAI Crew 1 — HR Analyst
    Returns: (fit_score: int, analysis_text: str)
    """
    agent = _build_agent("hr_analyst")
    task = _build_task(
        "fit_analysis_task",
        agent,
        cv_text=cv_text[:3000],
        jd_text=jd_text[:2000],
        context=context
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )
    result = str(crew.kickoff())

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
    """
    CrewAI Crew 2 — Cover Letter Writer
    Returns: cover_letter_text: str
    """
    agent = _build_agent("cover_letter_writer")
    task = _build_task(
        "cover_letter_task",
        agent,
        cv_text=cv_text[:2000],
        jd_text=jd_text[:2000],
        fit_analysis=fit_analysis[:600]
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )
    return str(crew.kickoff())


def run_resume_suggestions(cv_text: str, jd_text: str, gaps: str) -> str:
    """
    CrewAI Crew 3 — Resume Coach
    Returns: suggestions_text: str
    """
    agent = _build_agent("resume_coach")
    task = _build_task(
        "resume_suggestions_task",
        agent,
        cv_text=cv_text[:2000],
        jd_text=jd_text[:1500],
        gaps=gaps
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )
    return str(crew.kickoff())