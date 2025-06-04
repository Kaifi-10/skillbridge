import streamlit as st
import os
import requests
import json
from prompts import *
from io import BytesIO
import PyPDF2
from dotenv import load_dotenv
import random

load_dotenv()

st.set_page_config(page_title="SkillBridge", layout="centered")

st.title("🚀 SkillBridge - AI Career & Skill Coach")

OPENROUTER_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "google/gemini-2.0-flash-001"
SITE_URL = "https://your-site-url.com"  # Optional, update as needed
SITE_NAME = "SkillBridge"  # Optional, update as needed

INTERVIEWER_NAMES = ["Steve", "Natasha", "Tony", "Clint", "Bruce", "Chris", "Peter", "Nick", "Yelena", "Bucky"]

def get_openrouter_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
    }
    try:
        response = requests.post(
            url=OPENROUTER_BASE_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

# Session state for storing last suggestions
if 'last_career_path' not in st.session_state:
    st.session_state['last_career_path'] = None
if 'last_roadmap' not in st.session_state:
    st.session_state['last_roadmap'] = None

tab1, tab2, tab3, tab4 = st.tabs(["Career Path", "Learning Roadmap", "Resume Feedback", "Mock Interview"])

with tab1:
    st.header("Career Path Suggestions")
    skills = st.text_area("Your Skills")
    interests = st.text_input("Your Interests")
    education = st.text_input("Your Education")
    experience = st.text_area("Your Experience")
    if st.button("Suggest Careers"):
        prompt = get_career_path_prompt(skills, interests, education, experience)
        response = get_openrouter_response(prompt)
        st.session_state['last_career_path'] = response
        st.success(response)

with tab2:
    st.header("Learning Roadmap Generator")
    skills = st.text_area("Your Current Skills")
    goal = st.text_input("Your Career Goal (e.g. Data Scientist)")
    if st.button("Generate Roadmap"):
        prompt = get_roadmap_prompt(skills, goal)
        response = get_openrouter_response(prompt)
        st.session_state['last_roadmap'] = response
        st.info(response)

with tab3:
    st.header("Resume Feedback")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    resume_text = ""
    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""
        except Exception as e:
            st.error(f"Failed to read PDF: {e}")
    else:
        resume_text = st.text_area("Paste Your Resume Here")
    job_role = st.text_input("Target Job Role")
    if st.button("Get Feedback"):
        prompt = get_resume_feedback_prompt(resume_text, job_role)
        response = get_openrouter_response(prompt)
        st.warning(response)

with tab4:
    st.header("Mock Interview")
    option = st.radio("Choose an option:", [
        "Upload Resume + Position + Company",
        "Use Last Career Path Suggestion",
        "Use Last Learning Roadmap"
    ])
    interview_prompt = ""
    interviewer_name = random.choice(INTERVIEWER_NAMES)
    if option == "Upload Resume + Position + Company":
        uploaded_file = st.file_uploader("Upload your resume (PDF) for interview", type=["pdf"], key="mock_resume")
        resume_text = ""
        if uploaded_file is not None:
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    resume_text += page.extract_text() or ""
            except Exception as e:
                st.error(f"Failed to read PDF: {e}")
        else:
            resume_text = st.text_area("Paste Your Resume Here for Interview")
        position = st.text_input("Position for Mock Interview")
        company = st.text_input("Company for Mock Interview")
        if st.button("Start Mock Interview", key="mock1"):
            interview_prompt = f"Act as an interviewer for the position of {position} at {company}. Your name is {interviewer_name}. Use the following resume:\n{resume_text}\nStart the interview with an introduction using your name, then conduct a mock interview, ask 3-5 relevant questions, and finally provide a score out of 10 with feedback at the end."
    elif option == "Use Last Career Path Suggestion":
        if st.session_state['last_career_path']:
            if st.button("Start Mock Interview", key="mock2"):
                interview_prompt = f"Act as an interviewer for the following suggested career path. Your name is {interviewer_name}:\n{st.session_state['last_career_path']}\nStart the interview with an introduction using your name, then conduct a mock interview, ask 3-5 relevant questions, and finally provide a score out of 10 with feedback at the end."
        else:
            st.info("No career path suggestion found. Please use the 'Career Path Suggestions' tab first.")
    elif option == "Use Last Learning Roadmap":
        if st.session_state['last_roadmap']:
            if st.button("Start Mock Interview", key="mock3"):
                interview_prompt = f"Act as an interviewer for the following learning roadmap. Your name is {interviewer_name}:\n{st.session_state['last_roadmap']}\nStart the interview with an introduction using your name, then conduct a mock interview, ask 3-5 relevant questions, and finally provide a score out of 10 with feedback at the end."
        else:
            st.info("No learning roadmap found. Please use the 'Learning Roadmap Generator' tab first.")
    if interview_prompt:
        response = get_openrouter_response(interview_prompt)
        st.success(response)
