import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
import streamlit as st
from backend.parser import parse_resume
from backend.parser import parse_jd
from backend.embeddings import get_cosine_similarity
from backend.genai_scorer import get_genai_match_score
from backend.skill_matcher import compare_skills
from backend.highlight_skills import generate_highlighted_text
from backend.rag_engine import create_faiss_index_from_text, save_faiss_index
from backend.chatbot_engine import chat_with_resume_and_jd

st.set_page_config(page_title="Job Description Matcher", layout="wide")

st.title("💼 Job Description Matcher")

tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload & Score", "🧠 Matched/Missing Skills", "✅ GenAI Match Score", "💬 Chatbot"])

# Upload PDFs and cosine similarity scores
with tab1:
    st.header("Upload Resume & Job Description")

    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""

    if "jd_text" not in st.session_state:
        st.session_state.jd_text = ""

    resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"], key="resume_main")
    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"], key="jd_main")

    if resume_file:
        resume_text = parse_resume(resume_file)
        st.session_state.resume_text = resume_text
        resume_index = create_faiss_index_from_text(resume_text, "resume")  
        save_faiss_index(resume_index, "resume")  # Save resume FAISS index


    if jd_file:
        jd_text = parse_jd(jd_file)
        st.session_state.jd_text = jd_text
        jd_index = create_faiss_index_from_text(jd_text, "resume")  
        save_faiss_index(jd_index, "jd")  # Save JD FAISS index


    resume_text = st.session_state.resume_text
    jd_text = st.session_state.jd_text

    if resume_file and jd_file:

        st.subheader("📄 Parsed Documents")
        with st.expander("Resume Preview"):
            st.write(resume_text)
        with st.expander("Job Description Preview"):
            st.write(jd_text)

        if resume_text and jd_text:
            similarity_score = get_cosine_similarity(resume_text, jd_text)
            st.markdown(f"### 🔍 Cosine Similarity Score: `{similarity_score:.2f}`")

# Matched/Missing Skills
with tab2:
    st.header("Skill Match Results")
    if resume_file and jd_file:
        resume_text = st.session_state.resume_text
        jd_text = st.session_state.jd_text

        skills_result = compare_skills(resume_text, jd_text)

        matched = sorted(skills_result["matched"])
        missing = sorted(skills_result["missing"])

        st.subheader(f"✅ Matched Skills ({len(matched)})")
        st.write(", ".join(matched) if matched else "None found.")
        
        st.subheader(f"❌ Missing Skills ({len(missing)})")
        st.write(", ".join(missing) if missing else "None found.")

        # Highlighted sections
        resume_highlighted, jd_highlighted = generate_highlighted_text(resume_text, jd_text, skills_result)

        with st.expander("📄 Resume with Highlighted Skills"):
            st.markdown(resume_highlighted, unsafe_allow_html=True)

        with st.expander("📝 Job Description with Highlighted Skills"):
            st.markdown(jd_highlighted, unsafe_allow_html=True)

# GenAI Score
with tab3:
    st.header("GenAI-Based Scoring")
    if resume_file and jd_file:
        resume_text = st.session_state.resume_text
        jd_text = st.session_state.jd_text

        
        with st.spinner("🤖 Analyzing with LLM..."):
            genai_result = get_genai_match_score(resume_text, jd_text)
                
            # Parse score and reasoning using regex
            match = re.search(r"Match Score:\s*(\d+)/100", genai_result)
            score = int(match.group(1)) if match else None

            reason_match = re.search(r"Reason:\s*(.*)", genai_result, re.DOTALL)
            reasoning = reason_match.group(1).strip() if reason_match else "No explanation provided."
        
        st.markdown("### 🤖 GenAI Match Score")
        if score is not None:
            st.metric("Match Score (LLM)", f"{score}/100")
        st.markdown("**Reasoning:**")
        st.info(reasoning)

# Chatbot
with tab4:
    st.header("💬 Chat with Your Resume & JD")
    st.markdown("Ask questions like: *'What skills are missing?'*, *'How does this resume fit the role?'*, *'Summarize this job description'*")

    if resume_file and jd_file:
        user_query = st.text_input("🗨️ Ask a question:")
        if user_query:
            with st.spinner("Thinking..."):
                response = chat_with_resume_and_jd(user_query)
            st.markdown(f"**Answer:** {response}")
    else:
        st.warning("Please upload both Resume and Job Description to chat.")