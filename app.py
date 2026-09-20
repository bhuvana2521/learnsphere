import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import json
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import re
import os

st.set_page_config(page_title="LearnSphere AI", page_icon="", layout="wide")

def set_bg():
    try:
        with open("assets/bg.jpg", "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{
            backdrop-filter: blur(8px);
            background: rgba(255,255,255,0.85);
            padding: 2rem;
            border-radius: 18px;
        }}
        .stButton>button {{
            background: linear-gradient(135deg,#0072ff,#00c6ff);
            color:white;
            border-radius:10px;
            border:none;
            font-weight:600;
        }}
        </style>""", unsafe_allow_html=True)
    except Exception:
        pass

set_bg()
st.title(" LearnSphere AI")
st.caption("AI Powered ML Learning Platform")

api_key = None
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass
if not api_key:
    api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("Add GROQ_API_KEY in .streamlit/secrets.toml")
    st.stop()

client = Groq(api_key=api_key)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI error: {e}")
        return ""

defaults = {
    "current_topic": "Linear Regression",
    "quiz_data": None,
    "submitted": False,
    "score": 0,
    "mentor_history": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def generate_certificate(name, topic, score):
    file_name = "certificate.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 700, "Certificate of Achievement")
    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 650, f"This certifies that {name}")
    c.drawCentredString(300, 620, f"completed learning {topic}")
    c.drawCentredString(300, 590, f"Quiz Score: {score}/3")
    c.drawCentredString(300, 550, f"Date: {datetime.date.today()}")
    c.save()
    return file_name

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [" Lesson", " Roadmap", " Audio", " Quiz", " Mentor", " Progress"]
)

with tab1:
    topic = st.text_input("Topic", st.session_state.current_topic)
    if st.button("Generate Lesson"):
        st.session_state.current_topic = topic
        with st.spinner("Generating lesson..."):
            st.write(ask_ai(f"Explain {topic} for students with clear examples."))

with tab2:
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    if st.button("Generate Roadmap"):
        with st.spinner("Generating roadmap..."):
            st.write(ask_ai(f"Create a learning roadmap for {st.session_state.current_topic} for a {level} level student."))

with tab3:
    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            text = ask_ai(f"Explain {st.session_state.current_topic} in detail.")
            if text:
                tts = gTTS(text)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes)

with tab4:
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            response = ask_ai(f"""Create 3 multiple choice questions on {st.session_state.current_topic}.
Return ONLY a JSON array, no extra text:
[{{"question":"...","options":["A","B","C","D"],"answer":0}}]""")
            quiz = None
            if response:
                try:
                    quiz = json.loads(response)
                except Exception:
                    match = re.search(r"\[.*\]", response, re.DOTALL)
                    if match:
                        try:
                            quiz = json.loads(match.group(0))
                        except Exception:
                            pass
            if quiz:
                st.session_state.quiz_data = quiz
                st.session_state.submitted = False
            else:
                st.error("Could not generate quiz. Try again.")

    if st.session_state.quiz_data:
        score = 0
        for i, q in enumerate(st.session_state.quiz_data):
            selected = st.radio(q["question"], q["options"], key=f"q{i}")
            if st.session_state.submitted:
                correct = q["options"][q["answer"]]
                if selected == correct:
                    score += 1
                st.write(f"Correct Answer: {correct}")
        if not st.session_state.submitted:
            if st.button("Submit Quiz"):
                st.session_state.submitted = True
                st.session_state.score = score
                st.rerun()

    if st.session_state.submitted:
        st.success(f"Final Score: {st.session_state.score}/3")
        name = st.text_input("Enter your name for certificate")
        if name and st.button("Generate Certificate"):
            file = generate_certificate(name, st.session_state.current_topic, st.session_state.score)
            with open(file, "rb") as f:
                st.download_button("Download Certificate", f, "LearnSphere_Certificate.pdf")

with tab5:
    question = st.text_input("Ask your mentor anything...")
    if st.button("Ask"):
        if question:
            with st.spinner("Thinking..."):
                reply = ask_ai(question)
            st.session_state.mentor_history.append(("You", question))
            st.session_state.mentor_history.append(("Mentor", reply))
    for role, msg in reversed(st.session_state.mentor_history):
        if role == "You":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Mentor:** {msg}")

with tab6:
    st.metric("Current Topic", st.session_state.current_topic)
    if st.session_state.submitted:
        st.metric("Last Quiz Score", f"{st.session_state.score}/3")
    else:
        st.info("Complete a quiz to see your score here.")
