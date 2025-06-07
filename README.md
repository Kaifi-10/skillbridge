# 🚀 SkillBridge - AI Career & Skill Coach

SkillBridge is an AI-powered web application designed to help users explore career paths, generate personalized learning roadmaps, receive resume feedback, and practice mock interviews. Built with Streamlit, it leverages Google Gemini (via OpenRouter), Supabase for authentication, and PDF parsing for resume analysis.

---

## 🌟 Features

- **User Authentication:** Secure sign-up and login using Supabase.
- **Career Path Suggestions:** Get AI-generated career suggestions based on your skills, interests, education, and experience.
- **Learning Roadmap Generator:** Receive a step-by-step learning plan tailored to your career goals.
- **Resume Feedback:** Upload your resume (PDF or text) and get instant, actionable feedback.
- **Mock Interview:** Practice interviews based on your resume, career path, or learning roadmap, with AI-generated questions and feedback.

---

## 🛠️ Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/) (Python)
- **AI Model:** [Google Gemini 2.0 Flash](https://openrouter.ai/) via OpenRouter API
- **Authentication & Database:** [Supabase](https://supabase.com/)
- **PDF Parsing:** [PyPDF2](https://pypi.org/project/PyPDF2/)
- **Environment Variables:** [python-dotenv](https://pypi.org/project/python-dotenv/)
- **HTTP Requests:** [requests](https://pypi.org/project/requests/)

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kaifi-10/skillbridge.git
   cd skillbridge
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the root directory with the following content:
   ```
   GEMINI_API_KEY=your_openrouter_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

   - Get your OpenRouter API key from [openrouter.ai](https://openrouter.ai/)
   - Set up a Supabase project and get your URL and anon key from [supabase.com](https://supabase.com/)

---

## 🚀 Running the App

```bash
streamlit run skillbridge/app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📝 Usage

1. **Sign Up / Login:**  
   Create an account or log in using your email and password.

2. **Career Path Suggestions:**  
   Enter your skills, interests, education, and experience to get AI-powered career suggestions.

3. **Learning Roadmap:**  
   Input your current skills and career goal to generate a personalized learning roadmap.

4. **Resume Feedback:**  
   Upload your resume as a PDF or paste the text to receive instant feedback.

5. **Mock Interview:**  
   Practice interviews based on your resume, last career path suggestion, or learning roadmap.

---

## 🔒 Environment Variables

| Variable            | Description                        |
|---------------------|------------------------------------|
| GEMINI_API_KEY      | OpenRouter API key for Gemini      |
| SUPABASE_URL        | Supabase project URL               |
| SUPABASE_ANON_KEY   | Supabase anon/public API key       |

---

## 📚 Dependencies

- streamlit
- requests
- python-dotenv
- PyPDF2
- supabase
- (plus any others in `requirements.txt`)

---

## 🏗️ Project Structure

```
skillbridge/
│
├── app.py                # Main Streamlit app
├── prompts.py            # Prompt templates for AI
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
└── ...
```

---

## 🤖 AI Model

- **Model:** Google Gemini 2.0 Flash (via OpenRouter)
- **API Endpoint:** https://openrouter.ai/api/v1/chat/completions

---

## 🛡️ License

[MIT License](LICENSE)

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenRouter](https://openrouter.ai/)
- [Supabase](https://supabase.com/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
