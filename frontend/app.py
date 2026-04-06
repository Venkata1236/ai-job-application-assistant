"""
app.py
AI Job Application Assistant — Premium Streamlit UI
Dark luxury theme with animated components and rich result display.
"""
import os
import time
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Premium CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
    color: #e8e8f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #111128 50%, #0a0a0f 100%);
    border-bottom: 1px solid rgba(255,215,100,0.15);
    padding: 52px 60px 40px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(255,215,100,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(120,100,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,215,100,0.08);
    border: 1px solid rgba(255,215,100,0.2);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ffd764;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #ffd764 60%, #ffaa40 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 14px;
}
.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: rgba(232,232,240,0.55);
    letter-spacing: 0.01em;
    max-width: 560px;
}
.hero-pills {
    display: flex;
    gap: 10px;
    margin-top: 28px;
    flex-wrap: wrap;
}
.pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 12px;
    color: rgba(232,232,240,0.6);
    font-weight: 500;
}

/* ── Main Layout ── */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    min-height: calc(100vh - 200px);
}

/* ── Input Panel ── */
.input-panel {
    padding: 48px 48px 48px 60px;
    border-right: 1px solid rgba(255,255,255,0.06);
    background: #0d0d1a;
}
.panel-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ffd764;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.panel-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,215,100,0.15);
}

/* ── Upload Zone ── */
.upload-zone {
    border: 1.5px dashed rgba(255,215,100,0.25);
    border-radius: 16px;
    padding: 36px 24px;
    text-align: center;
    background: rgba(255,215,100,0.02);
    transition: all 0.3s ease;
    margin-bottom: 32px;
    cursor: pointer;
}
.upload-zone:hover {
    border-color: rgba(255,215,100,0.5);
    background: rgba(255,215,100,0.04);
}
.upload-icon { font-size: 36px; margin-bottom: 12px; }
.upload-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 6px;
}
.upload-hint { font-size: 13px; color: rgba(232,232,240,0.4); }

/* ── File Success ── */
.file-success {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(74,222,128,0.06);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 32px;
}
.file-icon { font-size: 24px; }
.file-name { font-size: 14px; font-weight: 600; color: #4ade80; }
.file-size { font-size: 12px; color: rgba(74,222,128,0.6); margin-top: 2px; }

/* ── JD Box ── */
.jd-section { margin-bottom: 32px; }
.jd-label {
    font-size: 13px;
    font-weight: 600;
    color: rgba(232,232,240,0.7);
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.word-count {
    font-size: 11px;
    color: rgba(232,232,240,0.3);
    font-weight: 400;
}

/* ── Analyze Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ffd764 0%, #ffaa40 100%) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 18px 32px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 32px rgba(255,215,100,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(255,215,100,0.35) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Results Panel ── */
.results-panel {
    padding: 48px 60px 48px 48px;
    background: #0a0a0f;
}

/* ── Score Card ── */
.score-card {
    background: linear-gradient(135deg, #111128 0%, #16162e 100%);
    border: 1px solid rgba(255,215,100,0.15);
    border-radius: 20px;
    padding: 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.score-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,215,100,0.08) 0%, transparent 70%);
}
.score-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}
.score-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(232,232,240,0.4);
}
.score-number {
    font-family: 'Playfair Display', serif;
    font-size: 80px;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.04em;
}
.score-suffix {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 400;
    color: rgba(232,232,240,0.3);
    align-self: flex-end;
    margin-bottom: 12px;
    margin-left: 4px;
}
.score-verdict {
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 100px;
    display: inline-block;
}
.verdict-strong { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
.verdict-moderate { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
.verdict-weak { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }

/* ── Score Bar ── */
.score-bar-bg {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    margin-top: 20px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Result Sections ── */
.result-section {
    background: #111128;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 20px;
}
.result-section-header {
    padding: 20px 28px;
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.result-section-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(232,232,240,0.7);
    display: flex;
    align-items: center;
    gap: 10px;
}
.result-section-body {
    padding: 28px;
    font-size: 14px;
    line-height: 1.8;
    color: rgba(232,232,240,0.75);
}

/* ── Skills Tags ── */
.skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 16px 0;
}
.skill-tag {
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.2);
    color: #4ade80;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
}
.gap-tag {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.2);
    color: #f87171;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
}

/* ── Cover Letter ── */
.cover-letter-body {
    padding: 28px;
    font-size: 14px;
    line-height: 1.9;
    color: rgba(232,232,240,0.8);
    font-style: italic;
    border-left: 3px solid rgba(255,215,100,0.3);
    margin: 28px;
    background: rgba(255,215,100,0.02);
    border-radius: 0 12px 12px 0;
}

/* ── Resume Tips ── */
.tip-item {
    display: flex;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.tip-item:last-child { border-bottom: none; }
.tip-number {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 900;
    color: rgba(255,215,100,0.3);
    min-width: 32px;
    line-height: 1;
}
.tip-text { font-size: 14px; line-height: 1.7; color: rgba(232,232,240,0.75); }

/* ── Download Button ── */
.download-row {
    display: flex;
    gap: 12px;
    padding: 20px 28px;
    background: rgba(255,255,255,0.02);
    border-top: 1px solid rgba(255,255,255,0.05);
}

/* ── Empty State ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 400px;
    text-align: center;
    opacity: 0.4;
}
.empty-icon { font-size: 56px; margin-bottom: 20px; }
.empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    color: rgba(232,232,240,0.6);
    margin-bottom: 10px;
}
.empty-sub { font-size: 14px; color: rgba(232,232,240,0.35); max-width: 260px; }

/* ── Loading ── */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    text-align: center;
}
.loading-spinner {
    width: 56px; height: 56px;
    border: 3px solid rgba(255,215,100,0.1);
    border-top-color: #ffd764;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 24px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}
.loading-sub { font-size: 13px; color: rgba(232,232,240,0.4); }
.loading-steps {
    margin-top: 28px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 260px;
}
.loading-step {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 13px;
    color: rgba(232,232,240,0.35);
}
.step-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: rgba(255,215,100,0.3);
    flex-shrink: 0;
}
.step-dot.active {
    background: #ffd764;
    box-shadow: 0 0 8px rgba(255,215,100,0.6);
}

/* ── Streamlit overrides ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    padding: 16px !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: rgba(255,215,100,0.4) !important;
    box-shadow: 0 0 0 3px rgba(255,215,100,0.08) !important;
}
.stFileUploader {
    background: transparent !important;
}
.stFileUploader > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(255,215,100,0.25) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}
.stFileUploader label { color: #e8e8f0 !important; }
div[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.06) !important;
    color: #e8e8f0 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    width: 100% !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,215,100,0.08) !important;
    border-color: rgba(255,215,100,0.3) !important;
    color: #ffd764 !important;
}
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Career Intelligence</div>
    <div class="hero-title">Land Your Dream Job<br>with Precision.</div>
    <div class="hero-sub">Upload your CV, paste a job description — get a fit score, tailored cover letter, and resume improvements in seconds.</div>
    <div class="hero-pills">
        <span class="pill">⚡ LangGraph Orchestration</span>
        <span class="pill">🤖 CrewAI Agents</span>
        <span class="pill">🔍 RAG Context</span>
        <span class="pill">📊 ATS Scoring</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Two-column layout ─────────────────────────────────────────────
left, right = st.columns([1, 1], gap="small")

# ── LEFT: Inputs ──────────────────────────────────────────────────
with left:
    st.markdown("""
    <div style="padding: 48px 48px 0 60px;">
        <div class="panel-label">01 — Your Profile</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding: 0 48px 0 60px;">', unsafe_allow_html=True)

        cv_file = st.file_uploader(
            "Upload CV (PDF or TXT)",
            type=["pdf", "txt"],
            help="Your resume or CV"
        )

        if cv_file:
            size_kb = len(cv_file.getvalue()) / 1024
            st.markdown(f"""
            <div class="file-success">
                <div class="file-icon">✅</div>
                <div>
                    <div class="file-name">{cv_file.name}</div>
                    <div class="file-size">{size_kb:.1f} KB · Ready to analyze</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="height:24px"></div>
        <div class="panel-label">02 — Target Role</div>
        """, unsafe_allow_html=True)

        jd_text = st.text_area(
            "Paste Job Description",
            height=280,
            placeholder="Paste the full job description here — requirements, responsibilities, qualifications...",
            label_visibility="collapsed"
        )

        if jd_text:
            word_count = len(jd_text.split())
            st.markdown(f"""
            <div style="text-align:right; font-size:12px;
            color:rgba(232,232,240,0.3); margin-top:8px; margin-bottom:16px;">
            {word_count} words
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
        analyze_btn = st.button("⚡  Analyze My Application", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── RIGHT: Results ────────────────────────────────────────────────
with right:
    st.markdown("""
    <div style="padding: 48px 60px 0 48px;">
        <div class="panel-label">03 — Intelligence Report</div>
    </div>
    """, unsafe_allow_html=True)

    result_container = st.container()

    with result_container:
        if not analyze_btn:
            st.markdown("""
            <div style="padding: 0 60px 0 48px;">
            <div class="empty-state">
                <div class="empty-icon">✦</div>
                <div class="empty-title">Awaiting Analysis</div>
                <div class="empty-sub">Upload your CV and paste a job description to generate your intelligence report.</div>
            </div>
            </div>
            """, unsafe_allow_html=True)

        elif not cv_file or not jd_text.strip():
            if not cv_file:
                st.error("⚠️ Please upload your CV first.")
            if not jd_text.strip():
                st.error("⚠️ Please paste the job description.")

        else:
            loading_placeholder = st.empty()
            loading_placeholder.markdown("""
            <div style="padding: 0 60px 0 48px;">
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <div class="loading-title">Analyzing Your Profile</div>
                <div class="loading-sub">Our AI agents are working on your report</div>
                <div class="loading-steps">
                    <div class="loading-step">
                        <div class="step-dot active"></div>
                        <span>Indexing CV & job description</span>
                    </div>
                    <div class="loading-step">
                        <div class="step-dot active"></div>
                        <span>HR Analyst scoring your fit</span>
                    </div>
                    <div class="loading-step">
                        <div class="step-dot"></div>
                        <span>Writing tailored cover letter</span>
                    </div>
                    <div class="loading-step">
                        <div class="step-dot"></div>
                        <span>Generating resume improvements</span>
                    </div>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            try:
                response = requests.post(
                    f"{API_URL}/analyze",
                    files={"cv_file": (cv_file.name, cv_file.getvalue(), "application/octet-stream")},
                    data={"job_description": jd_text},
                    timeout=300
                )

                loading_placeholder.empty()

                if response.status_code == 200:
                    data = response.json()
                    score = data["fit_score"]

                    # ── Score color ────────────────────────────
                    if score >= 70:
                        score_color = "#4ade80"
                        verdict_class = "verdict-strong"
                        verdict_text = "Strong Match"
                        verdict_icon = "✦"
                        bar_gradient = "linear-gradient(90deg, #4ade80, #22c55e)"
                    elif score >= 50:
                        score_color = "#fbbf24"
                        verdict_class = "verdict-moderate"
                        verdict_text = "Moderate Match"
                        verdict_icon = "◈"
                        bar_gradient = "linear-gradient(90deg, #fbbf24, #f59e0b)"
                    else:
                        score_color = "#f87171"
                        verdict_class = "verdict-weak"
                        verdict_text = "Needs Work"
                        verdict_icon = "◇"
                        bar_gradient = "linear-gradient(90deg, #f87171, #ef4444)"

                    st.markdown(f"""
                    <div style="padding: 0 60px 0 48px;">

                    <!-- Score Card -->
                    <div class="score-card">
                        <div class="score-header">
                            <div>
                                <div class="score-label">Candidate Fit Score</div>
                                <div style="display:flex; align-items:baseline; margin-top:8px;">
                                    <div class="score-number" style="color:{score_color}">{score}</div>
                                    <div class="score-suffix">/100</div>
                                </div>
                            </div>
                            <div>
                                <div class="score-verdict {verdict_class}">{verdict_icon} {verdict_text}</div>
                            </div>
                        </div>
                        <div class="score-bar-bg">
                            <div class="score-bar-fill" style="width:{score}%; background:{bar_gradient};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Fit Analysis ───────────────────────────
                    st.markdown(f"""
                    <div class="result-section">
                        <div class="result-section-header">
                            <div class="result-section-title">📊 Fit Analysis</div>
                        </div>
                        <div class="result-section-body">
                            {data['fit_analysis'].replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Cover Letter ───────────────────────────
                    st.markdown(f"""
                    <div class="result-section">
                        <div class="result-section-header">
                            <div class="result-section-title">✉️ Tailored Cover Letter</div>
                        </div>
                        <div class="cover-letter-body">
                            {data['cover_letter'].replace(chr(10), '<br><br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.download_button(
                        "⬇️ Download Cover Letter",
                        data["cover_letter"],
                        file_name="cover_letter.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    # ── Resume Tips ────────────────────────────
                    tips = [t.strip() for t in data['resume_suggestions'].split('\n') if t.strip() and t.strip()[0].isdigit()]
                    tips_html = ""
                    for i, tip in enumerate(tips[:6], 1):
                        clean = tip[2:].strip() if len(tip) > 2 else tip
                        tips_html += f"""
                        <div class="tip-item">
                            <div class="tip-number">0{i}</div>
                            <div class="tip-text">{clean}</div>
                        </div>"""

                    st.markdown(f"""
                    <div class="result-section" style="margin-top:20px;">
                        <div class="result-section-header">
                            <div class="result-section-title">🔧 Resume Improvements</div>
                        </div>
                        <div style="padding: 8px 28px;">
                            {tips_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Full Report Download ───────────────────
                    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Download Full Intelligence Report",
                        data["final_report"],
                        file_name="job_application_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    error_detail = response.json().get("detail", response.text)
                    st.error(f"❌ Backend error: {error_detail}")

            except requests.exceptions.ConnectionError:
                loading_placeholder.empty()
                st.error(f"❌ Cannot connect to backend at `{API_URL}`")
            except requests.exceptions.Timeout:
                loading_placeholder.empty()
                st.error("⏱️ Request timed out. Please try again.")
            except Exception as e:
                loading_placeholder.empty()
                st.error(f"❌ Unexpected error: {str(e)}")