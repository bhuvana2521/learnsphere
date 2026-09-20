# 🚀 LearnSphere AI

An AI-powered ML learning platform built with Streamlit and Google Gemini.

## Features

- 📚 AI-generated lessons on any ML topic
- 🗺️ Personalized learning roadmaps
- 🎧 Text-to-speech audio lessons
- 🧠 Auto-generated quizzes with scoring
- 🤖 AI mentor chatbot
- 📊 Progress tracker with certificate generation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your Gemini API key to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Utility Scripts

- `list_models.py` — lists all available Gemini models for your API key
- `run_models.py` — verifies model access
- `test_gemini.py` — quick connectivity test
