import streamlit as st
import os
import pdfplumber
import docx
from question_generate import generate_questions
from feedback_evalutor import evaluate_answer
from interview_report import generate_report

# -------------------- Page Config --------------------
st.set_page_config(page_title="Smart Interview Simulator", page_icon="🤖", layout="wide")

# -------------------- Custom CSS --------------------
st.markdown("""
<style>
.title { text-align: center; font-size: 42px !important; color: #1d4ed8; font-weight: bold; background-color: #e0f2fe; padding: 15px; border-radius: 12px; } .subtitle { text-align: center; font-size: 20px !important; color: #2563eb; margin-bottom: 20px; font-weight: 500; } .question { background-color: #eff6ff; padding: 12px; border-radius: 10px; margin: 8px 0; font-size: 16px; font-weight: 600; color: #1e3a8a; border-left: 5px solid #1d4ed8; } .report-success { font-size: 18px; color: #1d4ed8; font-weight: bold; } .stButton button { background-color: #1d4ed8; color: white; border-radius: 8px; padding: 8px 20px; border: none; font-weight: bold; transition: 0.3s; } .stButton button:hover { background-color: #2563eb; transform: scale(1.05); } .sidebar-banner { text-align: center; background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%); padding: 20px; border-radius: 12px; color: white; } .sidebar-banner h2 { margin-bottom: 10px; font-size: 26px; } .sidebar-banner p { font-size: 14px; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-banner">
        <h2>🤖 Smart Interview</h2>
        <p>AI-powered interview tool.<br>Upload your resume, answer questions, get instant feedback!</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### ℹ️ Instructions")
    st.write( 
        "1️⃣ Upload or paste your resume text\n\n" 
             
        "2️⃣ Select a job domain\n\n"

        "3️⃣ Generate AI-based questions\n\n"

        "4️⃣ Answer & receive instant feedback\n\n"

        "5️⃣ Download a final performance report"
        
             )

# -------------------- Title --------------------
st.markdown('<p class="title">Smart Interview Simulator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your resume, get AI-generated questions, answer them, and receive instant feedback!</p>', unsafe_allow_html=True)

# -------------------- Session State --------------------
for key in ["questions", "answers", "feedback", "resume_text"]:
    if key not in st.session_state:
        if key in ["questions","answers","feedback"]:
            st.session_state[key] = []
        else:
    
            st.session_state[key] = ""

# -------------------- Step 1: Upload Resume --------------------
st.header("📂 Step 1: Upload Resume")
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf","docx","txt"])
resume_text = ""

if uploaded_file:
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            resume_text = "\n".join([p.text for p in doc.paragraphs])
        st.success("✅ Resume Uploaded Successfully!")
    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")

manual_resume_text = st.text_area("OR Paste Your Resume Text", height=200)
final_resume_text = resume_text if resume_text else manual_resume_text

domain = st.selectbox("Select Job Domain", ["Software Engineer","Data Scientist","AI/ML Engineer"])

if st.button("🚀 Generate Questions"):
    if final_resume_text.strip():
        try:
            prompt = f"Generate 5 interview questions for {domain} based on resume:\n{final_resume_text}"
            st.session_state.questions = generate_questions(prompt,5)
            st.session_state.answers = []
            st.session_state.feedback = []
            st.session_state.resume_text = final_resume_text
            st.success("✅ 5 Questions Generated Successfully!")
        except Exception as e:
            st.error(f"Error generating questions: {e}")
    else:
        st.warning("⚠️ Upload or paste resume text first.")
# -------------------- Step 2: Answer All Questions --------------------
if st.session_state.questions:
    st.header("📝 Step 2: Answer Questions")
    
    # Create/initialize answers list if empty
    if len(st.session_state.answers) < len(st.session_state.questions):
        st.session_state.answers = [""] * len(st.session_state.questions)
    
    # Show all questions with text areas
    for i, question in enumerate(st.session_state.questions):
        st.markdown(f'<div class="question">Q{i+1}: {question}</div>', unsafe_allow_html=True)
        st.session_state.answers[i] = st.text_area(f"Your Answer for Q{i+1}", value=st.session_state.answers[i], key=f"ans_{i}")
    
    # Submit all answers button
    if st.button("Submit All Answers"):
        all_filled = all(ans.strip() != "" for ans in st.session_state.answers)
        if all_filled:
            # Generate feedback for all questions
            st.session_state.feedback = []
            for i, question in enumerate(st.session_state.questions):
                fb = evaluate_answer(question, st.session_state.answers[i])
                st.session_state.feedback.append(fb)
            st.success("✅ Feedback generated for all questions!")
        else:
            st.warning("⚠️ Please answer all questions before submitting.")

# -------------------- Step 3: Feedback Summary --------------------
if st.session_state.feedback:
    st.header("💡 Feedback Summary")
    for i, fb in enumerate(st.session_state.feedback):
        st.markdown(f"**Q{i+1} Feedback:** {fb}")


# -------------------- Step 4: Generate Report --------------------
if st.session_state.questions and st.session_state.answers and st.session_state.feedback:
    st.header("📊 Step 3: Generate Interview Report")
    if st.button("📑 Generate PDF Report"):
        try:
            report_path = generate_report(st.session_state.questions,
                                          st.session_state.answers,
                                          st.session_state.feedback)
            if os.path.exists(report_path):
                st.success("✅ Report Generated Successfully!")
                with open(report_path,"rb") as f:
                    st.download_button("📥 Download Report", f, file_name="interview_report.pdf")
            else:
                st.error("⚠️ Report file not found.")
        except Exception as e:
            st.error(f"Error generating report: {e}")
