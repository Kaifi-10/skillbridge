import streamlit as st
import os
import requests
import json
from prompts import *
from io import BytesIO
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SkillBridge", layout="centered")

st.title("🚀 SkillBridge - AI Career & Skill Coach")

OPENROUTER_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "google/gemini-2.0-flash-001"
SITE_URL = "https://your-site-url.com"  # Optional, update as needed
SITE_NAME = "SkillBridge"  # Optional, update as needed
ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

# --- Helper functions ---
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

def transcribe_audio_assemblyai(audio_bytes):
    if not ASSEMBLYAI_API_KEY:
        return "AssemblyAI API key not set."
    upload_url = "https://api.assemblyai.com/v2/upload"
    transcript_url = "https://api.assemblyai.com/v2/transcript"
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    # Upload audio
    response = requests.post(upload_url, headers=headers, files={"file": audio_bytes})
    if response.status_code != 200:
        return "Failed to upload audio for transcription."
    audio_url = response.json()["upload_url"]
    # Request transcription
    transcript_request = {"audio_url": audio_url}
    response = requests.post(transcript_url, json=transcript_request, headers=headers)
    if response.status_code != 200:
        return "Failed to start transcription."
    transcript_id = response.json()["id"]
    # Poll for completion
    import time
    while True:
        poll = requests.get(f"{transcript_url}/{transcript_id}", headers=headers)
        status = poll.json()["status"]
        if status == "completed":
            return poll.json()["text"]
        elif status == "failed":
            return "Transcription failed."
        time.sleep(2)

# --- Session state for storing last suggestions and interview state ---
if 'last_career_path' not in st.session_state:
    st.session_state['last_career_path'] = None
if 'last_roadmap' not in st.session_state:
    st.session_state['last_roadmap'] = None
if 'interview_state' not in st.session_state:
    st.session_state['interview_state'] = None

# --- Tabs ---
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

    # --- Setup interview context based on option ---
    if st.session_state['interview_state'] is None or st.button("Reset Interview"):
        st.session_state['interview_state'] = {
            'messages': [],
            'step': 0,
            'score': None,
            'finished': False,
            'context': None
        }
    interview_state = st.session_state['interview_state']

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
            intro = f"Act as an interviewer for the position of {position} at {company}. Use the following resume:\n{resume_text}\nConduct a mock interview, ask one question at a time, and after each answer, analyze and ask the next question. After the interview, provide a score out of 10 with feedback. Say 'Interview finished' when done."
            interview_state['messages'] = [{"role": "user", "content": [{"type": "text", "text": intro}]}]
            interview_state['step'] = 0
            interview_state['score'] = None
            interview_state['finished'] = False
            interview_state['context'] = 'resume'
    elif option == "Use Last Career Path Suggestion":
        if st.session_state['last_career_path']:
            if st.button("Start Mock Interview", key="mock2"):
                intro = f"Act as an interviewer for the following suggested career path:\n{st.session_state['last_career_path']}\nConduct a mock interview, ask one question at a time, and after each answer, analyze and ask the next question. After the interview, provide a score out of 10 with feedback. Say 'Interview finished' when done."
                interview_state['messages'] = [{"role": "user", "content": [{"type": "text", "text": intro}]}]
                interview_state['step'] = 0
                interview_state['score'] = None
                interview_state['finished'] = False
                interview_state['context'] = 'career_path'
        else:
            st.info("No career path suggestion found. Please use the 'Career Path Suggestions' tab first.")
    elif option == "Use Last Learning Roadmap":
        if st.session_state['last_roadmap']:
            if st.button("Start Mock Interview", key="mock3"):
                intro = f"Act as an interviewer for the following learning roadmap:\n{st.session_state['last_roadmap']}\nConduct a mock interview, ask one question at a time, and after each answer, analyze and ask the next question. After the interview, provide a score out of 10 with feedback. Say 'Interview finished' when done."
                interview_state['messages'] = [{"role": "user", "content": [{"type": "text", "text": intro}]}]
                interview_state['step'] = 0
                interview_state['score'] = None
                interview_state['finished'] = False
                interview_state['context'] = 'roadmap'
        else:
            st.info("No learning roadmap found. Please use the 'Learning Roadmap Generator' tab first.")

    # --- Interview loop ---
    if interview_state['messages']:
        # Get the latest question from the model if not finished
        if not interview_state['finished']:
            if interview_state['step'] == 0 or st.button("Get Next Question", key=f"nextq{interview_state['step']}"):
                # Only get a new question if last message is not an answer
                if len(interview_state['messages']) == 1 or interview_state['messages'][-1]['role'] == 'user':
                    # Get model's question
                    headers = {
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": SITE_URL,
                        "X-Title": SITE_NAME,
                    }
                    payload = {
                        "model": OPENROUTER_MODEL,
                        "messages": interview_state['messages']
                    }
                    response = requests.post(
                        url=OPENROUTER_BASE_URL,
                        headers=headers,
                        data=json.dumps(payload)
                    )
                    response.raise_for_status()
                    data = response.json()
                    question = data["choices"][0]["message"]["content"]
                    st.session_state['interview_state']['messages'].append({"role": "assistant", "content": [{"type": "text", "text": question}]})
                    st.session_state['interview_state']['step'] += 1
        # Display the latest question
        if interview_state['messages'][-1]['role'] == 'assistant':
            st.markdown(f"**Interviewer:** {interview_state['messages'][-1]['content'][0]['text']}")
            # Use st.audio and file uploader for answer
            audio_file = st.file_uploader("Upload your answer (wav/mp3/m4a/ogg/webm)", type=["wav", "mp3", "m4a", "ogg", "webm"], key=f"audio{interview_state['step']}")
            transcript = ""
            if audio_file is not None:
                st.audio(audio_file)
                if st.button("Transcribe & Submit Answer", key=f"transcribe{interview_state['step']}"):
                    transcript = transcribe_audio_assemblyai(audio_file)
                    st.markdown(f"**Your Answer (transcribed):** {transcript}")
                    st.session_state['interview_state']['messages'].append({"role": "user", "content": [{"type": "text", "text": transcript}]})
        # Check for interview finish
        if interview_state['messages'][-1]['role'] == 'assistant' and 'interview finished' in interview_state['messages'][-1]['content'][0]['text'].lower():
            st.session_state['interview_state']['finished'] = True
            st.success("Interview finished! See the feedback and score above.")
