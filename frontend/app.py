"""
app.py
AI Job Application Assistant v2.0 — Premium dark UI.
6 modules: Fit Score, Cover Letter, Resume Tips,
Interview Prep, LinkedIn Optimization, ATS Keywords.
"""
import os
import json
import re
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
.stApp { background: #08080f; font-family: 'DM Sans', sans-serif; color: #e8e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #111128 100%);
    border-bottom: 1px solid rgba(255,215,100,0.12);
    padding: 44px 60px 36px;
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -100px; right: -100px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,215,100,0.07) 0%, transparent 70%);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,215,100,0.08); border: 1px solid rgba(255,215,100,0.2);
    border-radius: 100px; padding: 5px 14px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #ffd764; margin-bottom: 16px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 4vw, 56px); font-weight: 900;
    line-height: 1.08; letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #ffd764 60%, #ffaa40 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 12px;
}
.hero-sub {
    font-size: 15px; font-weight: 300;
    color: rgba(232,232,240,0.5); max-width: 520px;
}
.hero-pills { display: flex; gap: 8px; margin-top: 24px; flex-wrap: wrap; }
.pill {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px; padding: 4px 12px;
    font-size: 11px; color: rgba(232,232,240,0.5); font-weight: 500;
}

/* Section label */
.panel-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #ffd764;
    margin-bottom: 24px; display: flex; align-items: center; gap: 10px;
}
.panel-label::after {
    content: ''; flex: 1; height: 1px; background: rgba(255,215,100,0.12);
}

/* Inputs */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important; color: #e8e8f0 !important;
    -webkit-text-fill-color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important; line-height: 1.7 !important;
    padding: 16px !important; caret-color: #ffd764 !important;
    opacity: 1 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(255,215,100,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,215,100,0.08) !important;
}
.stTextArea textarea::placeholder { color: rgba(232,232,240,0.25) !important; }
.stTextArea label { color: rgba(232,232,240,0.6) !important; font-size: 13px !important; }

.stFileUploader > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(255,215,100,0.25) !important;
    border-radius: 14px !important;
}

/* Analyze button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ffd764 0%, #ffaa40 100%) !important;
    color: #0a0a0f !important; border: none !important;
    border-radius: 14px !important; padding: 18px 32px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important; font-weight: 700 !important;
    box-shadow: 0 8px 32px rgba(255,215,100,0.2) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(255,215,100,0.35) !important;
}

/* Score card */
.score-card {
    background: linear-gradient(135deg, #111128, #16162e);
    border: 1px solid rgba(255,215,100,0.15);
    border-radius: 20px; padding: 32px; margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.score-card::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,215,100,0.07) 0%, transparent 70%);
}
.score-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.score-label { font-size: 10px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(232,232,240,0.4); margin-bottom: 8px; }
.score-num { font-family: 'Playfair Display', serif; font-size: 72px; font-weight: 900; line-height: 1; letter-spacing: -0.04em; }
.score-denom { font-family: 'Playfair Display', serif; font-size: 24px; color: rgba(232,232,240,0.25); }
.verdict-badge { font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 100px; }
.v-strong { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
.v-moderate { background: rgba(251,191,36,0.1); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
.v-weak { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
.bar-bg { height: 5px; background: rgba(255,255,255,0.06); border-radius: 100px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 100px; }

/* Module cards */
.mod-card {
    background: #0e0e1c; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px; overflow: hidden; margin-bottom: 16px;
}
.mod-header {
    padding: 18px 24px; background: rgba(255,255,255,0.02);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex; align-items: center; justify-content: space-between;
}
.mod-title {
    font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: rgba(232,232,240,0.6);
    display: flex; align-items: center; gap: 10px;
}
.mod-body { padding: 24px; }

/* Assessment text */
.assessment-text {
    font-size: 14px; line-height: 1.8; color: rgba(232,232,240,0.75);
    background: rgba(255,255,255,0.02); border-radius: 12px; padding: 18px;
    margin-bottom: 16px;
}

/* Tags */
.tags-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.tags-label { font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(232,232,240,0.35); margin-bottom: 8px; margin-top: 14px; }
.tag-match { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); color: #4ade80; border-radius: 8px; padding: 4px 12px; font-size: 12px; font-weight: 600; }
.tag-gap { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.2); color: #f87171; border-radius: 8px; padding: 4px 12px; font-size: 12px; font-weight: 600; }
.tag-present { background: rgba(74,222,128,0.08); border: 1px solid rgba(74,222,128,0.2); color: #4ade80; border-radius: 8px; padding: 4px 12px; font-size: 12px; font-weight: 600; }
.tag-missing { background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.2); color: #fbbf24; border-radius: 8px; padding: 4px 12px; font-size: 12px; font-weight: 600; }
.tag-critical { background: rgba(248,113,113,0.08); border: 1px solid rgba(248,113,113,0.2); color: #f87171; border-radius: 8px; padding: 4px 12px; font-size: 12px; font-weight: 700; }

/* Cover letter */
.cl-body {
    font-size: 14px; line-height: 1.9; color: rgba(232,232,240,0.8);
    border-left: 3px solid rgba(255,215,100,0.3);
    padding: 20px 24px; margin: 0;
    background: rgba(255,215,100,0.02);
    border-radius: 0 12px 12px 0;
    white-space: pre-line;
}

/* Resume tips */
.tip-row { display: flex; gap: 16px; padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.tip-row:last-child { border-bottom: none; }
.tip-num { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 900; color: rgba(255,215,100,0.25); min-width: 36px; line-height: 1.1; }
.tip-content { font-size: 14px; line-height: 1.7; color: rgba(232,232,240,0.75); }
.tip-cat { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #ffd764; margin-bottom: 4px; }

/* Interview questions */
.iq-section-label { font-size: 10px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; padding: 12px 0 8px; margin-top: 8px; }
.iq-section-technical { color: #60a5fa; }
.iq-section-behavioral { color: #a78bfa; }
.iq-section-gap { color: #fb923c; }
.iq-item { background: rgba(255,255,255,0.03); border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05); }
.iq-q { font-size: 14px; font-weight: 600; color: #e8e8f0; margin-bottom: 8px; line-height: 1.5; }
.iq-why { font-size: 12px; color: rgba(232,232,240,0.45); margin-bottom: 6px; }
.iq-tip { font-size: 13px; color: rgba(232,232,240,0.65); font-style: italic; padding: 8px 12px; background: rgba(255,215,100,0.04); border-radius: 8px; border-left: 2px solid rgba(255,215,100,0.2); }

/* LinkedIn */
.li-headline { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #ffd764; background: rgba(255,215,100,0.05); border: 1px solid rgba(255,215,100,0.15); border-radius: 12px; padding: 16px 20px; margin-bottom: 18px; }
.li-about { font-size: 14px; line-height: 1.85; color: rgba(232,232,240,0.78); white-space: pre-line; }

/* Empty state */
.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 380px; text-align: center; opacity: 0.4; }
.empty-icon { font-size: 52px; margin-bottom: 16px; }
.empty-title { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: rgba(232,232,240,0.6); margin-bottom: 8px; }
.empty-sub { font-size: 13px; color: rgba(232,232,240,0.35); max-width: 240px; }

/* Download buttons */
div[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.05) !important; color: #e8e8f0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important;
    font-size: 13px !important; font-weight: 600 !important;
    width: 100% !important; padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,215,100,0.07) !important;
    border-color: rgba(255,215,100,0.3) !important; color: #ffd764 !important;
}

/* Spinner override */
.stSpinner > div { border-top-color: #ffd764 !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI Career Intelligence Platform</div>
    <div class="hero-title">Land Your Dream Job<br>with Precision.</div>
    <div class="hero-sub">6-module AI pipeline — fit scoring, cover letter, resume tips, interview prep, LinkedIn optimization, and ATS keywords.</div>
    <div class="hero-pills">
        <span class="pill">⚡ LangGraph 8-Node Workflow</span>
        <span class="pill">🤖 6 CrewAI Agents</span>
        <span class="pill">🔍 RAG Context</span>
        <span class="pill">📊 ATS Keywords</span>
        <span class="pill">🎯 Interview Prep</span>
        <span class="pill">💼 LinkedIn Optimizer</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────
def parse_json_block(text):
    try:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            return json.loads(m.group())
    except Exception:
        pass
    return {}


def render_interview_questions(text):
    """Parse and render interview questions nicely."""
    sections = {"TECHNICAL": [], "BEHAVIORAL": [], "GAP-BASED": []}
    current = None
    current_q = {}

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current_q:
                sections.get(current, []).append(current_q)
                current_q = {}
            continue
        if line in ["TECHNICAL", "BEHAVIORAL", "GAP-BASED"]:
            if current_q:
                sections.get(current, []).append(current_q)
                current_q = {}
            current = line
        elif re.match(r'^Q\d+:', line):
            if current_q:
                sections.get(current, []).append(current_q)
            current_q = {"q": line.split(":", 1)[1].strip(), "why": "", "tip": ""}
        elif line.startswith("Why:"):
            current_q["why"] = line[4:].strip()
        elif line.startswith("Tip:"):
            current_q["tip"] = line[4:].strip()

    if current_q and current:
        sections[current].append(current_q)

    html = ""
    labels = {
        "TECHNICAL": ("🔵 Technical Questions", "iq-section-technical"),
        "BEHAVIORAL": ("🟣 Behavioral Questions", "iq-section-behavioral"),
        "GAP-BASED": ("🟠 Gap-Based Questions", "iq-section-gap")
    }

    for section, items in sections.items():
        if not items:
            continue
        label, cls = labels[section]
        html += f'<div class="iq-section-label {cls}">{label}</div>'
        for item in items:
            q = item.get("q", "")
            why = item.get("why", "")
            tip = item.get("tip", "")
            html += f"""
            <div class="iq-item">
                <div class="iq-q">❓ {q}</div>
                {"<div class='iq-why'>💡 " + why + "</div>" if why else ""}
                {"<div class='iq-tip'>✏️ " + tip + "</div>" if tip else ""}
            </div>"""

    if not html:
        html = f'<div style="font-size:14px;color:rgba(232,232,240,0.6);white-space:pre-line;">{text}</div>'

    return html


def render_linkedin(text):
    """Parse and render LinkedIn content."""
    headline = ""
    about = ""

    if "HEADLINE:" in text:
        parts = text.split("HEADLINE:", 1)[1]
        if "ABOUT:" in parts:
            headline = parts.split("ABOUT:")[0].strip()
            about = parts.split("ABOUT:")[1].strip()
        else:
            headline = parts.strip()
    else:
        about = text

    html = ""
    if headline:
        html += f'<div class="li-headline">"{headline}"</div>'
    if about:
        html += f'<div class="li-about">{about}</div>'
    if not html:
        html = f'<div style="font-size:14px;color:rgba(232,232,240,0.7);white-space:pre-line;">{text}</div>'
    return html


def render_resume_tips(text):
    """Parse and render numbered resume tips."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    tips = []
    for line in lines:
        match = re.match(r'^(\d+)[.)]\s*(?:\[(.+?)\]:?\s*)?(.+)', line)
        if match:
            num = match.group(1)
            cat = match.group(2) or ""
            content = match.group(3)
            tips.append((num, cat, content))

    if not tips:
        return f'<div style="font-size:14px;color:rgba(232,232,240,0.7);white-space:pre-line;">{text}</div>'

    html = ""
    for num, cat, content in tips[:6]:
        html += f"""
        <div class="tip-row">
            <div class="tip-num">0{num}</div>
            <div class="tip-content">
                {"<div class='tip-cat'>" + cat + "</div>" if cat else ""}
                {content}
            </div>
        </div>"""
    return html


# ── Layout ────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="small")

# ── LEFT: Inputs ──────────────────────────────────────────────────
with left:
    st.markdown('<div style="padding:40px 40px 0 56px"><div class="panel-label">01 — Your Profile</div></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="padding:0 40px 0 56px">', unsafe_allow_html=True)

        cv_file = st.file_uploader(
            "Upload CV — PDF or TXT",
            type=["pdf", "txt"]
        )
        if cv_file:
            size_kb = len(cv_file.getvalue()) / 1024
            st.success(f"✅ {cv_file.name} ({size_kb:.1f} KB) — Ready")

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-label" style="margin:0 0 12px">02 — Target Role</div>', unsafe_allow_html=True)

        jd_text = st.text_area(
            "Paste the full Job Description here",
            height=300,
            placeholder="Paste the complete job description — requirements, responsibilities, qualifications, and company info..."
        )
        if jd_text:
            wc = len(jd_text.split())
            st.caption(f"📝 {wc} words · Ready to analyze")

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        analyze_btn = st.button("⚡  Generate Full Career Intelligence Report", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── RIGHT: Results ────────────────────────────────────────────────
with right:
    st.markdown('<div style="padding:40px 56px 0 40px"><div class="panel-label">03 — Intelligence Report</div></div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 56px 40px 40px">', unsafe_allow_html=True)

        if not analyze_btn:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">✦</div>
                <div class="empty-title">Awaiting Analysis</div>
                <div class="empty-sub">Upload your CV and paste a job description to generate your 6-module intelligence report.</div>
            </div>""", unsafe_allow_html=True)

        elif not cv_file or not jd_text.strip():
            if not cv_file:
                st.error("⚠️ Please upload your CV.")
            if not jd_text.strip():
                st.error("⚠️ Please paste the job description.")
        else:
            with st.spinner("🤖 6 AI agents analyzing your profile — this takes 60–120 seconds..."):
                try:
                    response = requests.post(
                        f"{API_URL}/analyze",
                        files={"cv_file": (cv_file.name, cv_file.getvalue(), "application/octet-stream")},
                        data={"job_description": jd_text},
                        timeout=400
                    )

                    if response.status_code == 200:
                        data = response.json()
                        score = data["fit_score"]

                        # ── Score colors ───────────────────────
                        if score >= 70:
                            sc, vc, vt, grad = "#4ade80", "v-strong", "✦ Strong Match", "linear-gradient(90deg,#4ade80,#22c55e)"
                        elif score >= 50:
                            sc, vc, vt, grad = "#fbbf24", "v-moderate", "◈ Moderate Match", "linear-gradient(90deg,#fbbf24,#f59e0b)"
                        else:
                            sc, vc, vt, grad = "#f87171", "v-weak", "◇ Needs Work", "linear-gradient(90deg,#f87171,#ef4444)"

                        # ── 1. Score Card ──────────────────────
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-top">
                                <div>
                                    <div class="score-label">Candidate Fit Score</div>
                                    <div style="display:flex;align-items:baseline;gap:4px;margin-top:4px">
                                        <span class="score-num" style="color:{sc}">{score}</span>
                                        <span class="score-denom">/100</span>
                                    </div>
                                </div>
                                <div class="verdict-badge {vc}">{vt}</div>
                            </div>
                            <div class="bar-bg">
                                <div class="bar-fill" style="width:{score}%;background:{grad}"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── 2. Fit Analysis ────────────────────
                        fit_data = parse_json_block(data["fit_analysis"])
                        assessment = fit_data.get("assessment", data["fit_analysis"])
                        matching = fit_data.get("matching_skills", [])
                        gaps = fit_data.get("gaps", [])

                        match_tags = "".join(f'<span class="tag-match">✓ {s}</span>' for s in matching)
                        gap_tags = "".join(f'<span class="tag-gap">✗ {s}</span>' for s in gaps)

                        st.markdown(f"""
                        <div class="mod-card">
                            <div class="mod-header"><div class="mod-title">📊 Fit Analysis</div></div>
                            <div class="mod-body">
                                <div class="assessment-text">{assessment}</div>
                                {"<div class='tags-label'>Matching Skills</div><div class='tags-row'>" + match_tags + "</div>" if matching else ""}
                                {"<div class='tags-label'>Skill Gaps</div><div class='tags-row'>" + gap_tags + "</div>" if gaps else ""}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── 3. ATS Keywords ────────────────────
                        kw_data = parse_json_block(data["keywords"])
                        present = kw_data.get("present", [])
                        missing = kw_data.get("missing", [])
                        critical = kw_data.get("critical_missing", [])

                        if present or missing:
                            present_tags = "".join(f'<span class="tag-present">✓ {k}</span>' for k in present)
                            missing_tags = "".join(f'<span class="tag-missing">~ {k}</span>' for k in missing)
                            critical_tags = "".join(f'<span class="tag-critical">⚠ {k}</span>' for k in critical)
                            st.markdown(f"""
                            <div class="mod-card">
                                <div class="mod-header"><div class="mod-title">🔑 ATS Keywords</div></div>
                                <div class="mod-body">
                                    {"<div class='tags-label'>Found in CV</div><div class='tags-row'>" + present_tags + "</div>" if present else ""}
                                    {"<div class='tags-label'>Missing from CV</div><div class='tags-row'>" + missing_tags + "</div>" if missing else ""}
                                    {"<div class='tags-label'>Critical — Add These First</div><div class='tags-row'>" + critical_tags + "</div>" if critical else ""}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="mod-card">
                                <div class="mod-header"><div class="mod-title">🔑 ATS Keywords</div></div>
                                <div class="mod-body">
                                    <div style="font-size:14px;color:rgba(232,232,240,0.7);white-space:pre-line;">{data["keywords"]}</div>
                                </div>
                            </div>""", unsafe_allow_html=True)

                        # ── 4. Cover Letter ────────────────────
                        st.markdown(f"""
                        <div class="mod-card">
                            <div class="mod-header"><div class="mod-title">✉️ Tailored Cover Letter</div></div>
                            <div class="mod-body">
                                <div class="cl-body">{data["cover_letter"]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.download_button("⬇️ Download Cover Letter", data["cover_letter"], file_name="cover_letter.txt", use_container_width=True)

                        # ── 5. Resume Tips ─────────────────────
                        tips_html = render_resume_tips(data["resume_suggestions"])
                        st.markdown(f"""
                        <div class="mod-card">
                            <div class="mod-header"><div class="mod-title">🔧 Resume Improvements</div></div>
                            <div class="mod-body">{tips_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── 6. Interview Questions ─────────────
                        iq_html = render_interview_questions(data["interview_questions"])
                        st.markdown(f"""
                        <div class="mod-card">
                            <div class="mod-header"><div class="mod-title">🎯 Interview Preparation</div></div>
                            <div class="mod-body">{iq_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── 7. LinkedIn ────────────────────────
                        li_html = render_linkedin(data["linkedin_summary"])
                        st.markdown(f"""
                        <div class="mod-card">
                            <div class="mod-header"><div class="mod-title">💼 LinkedIn Optimization</div></div>
                            <div class="mod-body">{li_html}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.download_button("⬇️ Download LinkedIn Summary", data["linkedin_summary"], file_name="linkedin_summary.txt", use_container_width=True)

                        # ── 8. Full Report ─────────────────────
                        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
                        st.download_button("📥 Download Full Intelligence Report (.md)", data["final_report"], file_name="career_intelligence_report.md", mime="text/markdown", use_container_width=True)

                    else:
                        st.error(f"❌ {response.json().get('detail', response.text)}")

                except requests.exceptions.ConnectionError:
                    st.error(f"❌ Cannot connect to backend at `{API_URL}`")
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. The agents are taking too long — try again.")
                except Exception as e:
                    st.error(f"❌ {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)