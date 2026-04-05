"""
app.py
Streamlit frontend for the AI Job Application Assistant.
Sends CV + JD to FastAPI backend and renders results
as fit score, cover letter, and resume improvement tabs.
"""
import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="💼",
    layout="wide"
)

# ── Header ─────────────────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align:center;'>💼 AI Job Application Assistant</h1>
    <p style='text-align:center; color:gray;'>
        Powered by LangGraph &nbsp;·&nbsp; CrewAI &nbsp;·&nbsp;
        RAG &nbsp;·&nbsp; FastAPI
    </p>
    <hr>
""", unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📄 Upload Your CV")
    cv_file = st.file_uploader(
        "CV in PDF or TXT format",
        type=["pdf", "txt"],
        help="Upload your resume"
    )
    if cv_file:
        st.success(f"✅ {cv_file.name} uploaded")

with col2:
    st.subheader("📋 Job Description")
    jd_text = st.text_area(
        "Paste the full job description",
        height=250,
        placeholder="Copy and paste the entire job description here..."
    )
    if jd_text:
        st.caption(f"{len(jd_text.split())} words")

st.markdown("<br>", unsafe_allow_html=True)

# ── Analyze Button ─────────────────────────────────────────────────
analyze_btn = st.button(
    "🚀 Analyze My Application",
    use_container_width=True,
    type="primary"
)

if analyze_btn:
    if not cv_file:
        st.error("⚠️ Please upload your CV.")
    elif not jd_text.strip():
        st.error("⚠️ Please paste the job description.")
    else:
        with st.spinner("🤖 AI agents analyzing your application (~30–60 seconds)..."):
            try:
                response = requests.post(
                    f"{API_URL}/analyze",
                    files={
                        "cv_file": (
                            cv_file.name,
                            cv_file.getvalue(),
                            "application/octet-stream"
                        )
                    },
                    data={"job_description": jd_text},
                    timeout=180
                )

                if response.status_code == 200:
                    data = response.json()
                    score = data["fit_score"]

                    st.markdown("---")
                    st.subheader("📊 Analysis Results")

                    score_col, bar_col = st.columns([1, 3])

                    with score_col:
                        color = (
                            "green" if score >= 70
                            else "orange" if score >= 50
                            else "red"
                        )
                        st.markdown(
                            f"<div style='text-align:center; font-size:52px;"
                            f"font-weight:bold; color:{color}'>{score}</div>"
                            f"<div style='text-align:center; color:{color};"
                            f"font-size:14px'>out of 100</div>",
                            unsafe_allow_html=True
                        )

                    with bar_col:
                        verdict = (
                            "Strong Match ✅" if score >= 70
                            else "Moderate Match ⚠️" if score >= 50
                            else "Needs Work ❌"
                        )
                        st.markdown(f"**{verdict}**")
                        st.progress(score / 100)
                        st.caption(
                            "Based on skills alignment, "
                            "experience relevance, and keyword match"
                        )

                    st.markdown("<br>", unsafe_allow_html=True)

                    tab1, tab2, tab3 = st.tabs([
                        "📊 Fit Analysis",
                        "📝 Cover Letter",
                        "🔧 Resume Tips"
                    ])

                    with tab1:
                        st.markdown(data["fit_analysis"])

                    with tab2:
                        st.markdown(data["cover_letter"])
                        st.download_button(
                            "⬇️ Download Cover Letter",
                            data["cover_letter"],
                            file_name="cover_letter.txt",
                            mime="text/plain"
                        )

                    with tab3:
                        st.markdown(data["resume_suggestions"])

                    st.markdown("---")
                    st.download_button(
                        "📥 Download Full Report (.md)",
                        data["final_report"],
                        file_name="job_application_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                else:
                    error_detail = response.json().get("detail", response.text)
                    st.error(f"❌ Backend error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    f"❌ Cannot connect to backend at `{API_URL}`. "
                    "Is it running?"
                )
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")