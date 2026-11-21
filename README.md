# ✦ AI Mock Interview Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/OpenRouter-6467F2?style=for-the-badge&logoColor=white" />
</p>

<p align="center">
  <b>Your personal AI-powered interview practice space.</b>
  <br />
  Practice. Improve. Perform with confidence.
</p>

---

## ◈ Overview

**AI Mock Interview Bot** is an interactive interview preparation platform designed to simulate technical interviews using Large Language Models (LLMs).

It allows candidates to practice role-specific interviews, respond to AI-generated questions, and receive structured feedback on their performance.

From answering technical questions to reviewing a detailed evaluation report, the platform creates a simple and accessible environment for interview preparation.

## ✧ Features

| Feature | Description |
|---|---|
| 🎯 Role-based Interviews | Practice interviews tailored to selected job roles |
| 🤖 AI Interviewer | Dynamic questions generated using an LLM |
| 🎙️ Voice Input | Answer questions using browser-supported speech recognition |
| ⏱️ Interview Timer | Track interview duration and progress |
| 📊 AI Evaluation | Receive an overall performance score and feedback |
| 📝 Detailed Report | Review strengths and areas for improvement |
| 📥 Transcript Export | Export your interview conversation |

## ◈ Preview

<p align="center">
  <i>Application screenshots coming soon.</i>
</p>

<!-- Add your screenshots here after uploading them to the screenshots folder.

<p align="center">
  <img src="screenshots/dashboard.png" width="85%" alt="AI Mock Interview Dashboard" />
  <br />
  <i>Dashboard</i>
</p>

<p align="center">
  <img src="screenshots/interview-report.png" width="85%" alt="Interview Evaluation Report" />
  <br />
  <i>AI Evaluation Report</i>
</p>
-->

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web application and API endpoints |
| HTML & CSS | User interface and styling |
| JavaScript | Frontend interactions |
| OpenRouter API | LLM integration |
| Speech Recognition API | Browser-based voice input |

## ◈ How It Works

```text
      Candidate
          │
          ▼
   Select Interview Role
          │
          ▼
     AI Interviewer
          │
          ▼
   Answer Questions
    (Text / Voice)
          │
          ▼
   LLM-based Evaluation
          │
          ▼
   Performance Report
          │
          ▼
  Feedback & Improvement
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd ai-mock-interview-bot
```

### 2. Navigate to the backend

```bash
cd backend
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using the provided `.env.example` template.

Add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openrouter/free
```

**Important:** Never upload your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
python app.py
```

### 6. Open in your browser

```text
http://127.0.0.1:5000
```

## ◈ Project Structure

```text
ai-mock-interview-bot/
│
├── app.py
├── index.html
├── requirements.txt
├── .env.example
├── .gitignore
├── screenshots/
└── README.md
```

## ✦ Future Enhancements

- Skill-wise performance analytics
- Interview history and progress tracking
- Enhanced speech-to-text and text-to-speech support
- More personalized interview question generation
- Improved evaluation consistency
- Additional interview categories and difficulty levels

## ◈ Purpose

The goal of this project is to make interview practice more accessible and interactive by combining conversational AI with structured performance feedback.

It is a personal learning project focused on exploring LLM integration, backend development, frontend interaction, and AI-powered evaluation.

---

<p align="center">
  <b>Built with curiosity and a little bit of code. ✦</b>
  <br /><br />
  <i>Practice smarter. Keep improving.</i>
</p>
