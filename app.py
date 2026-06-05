import streamlit as st
import sqlite3
from PyPDF2 import PdfReader
from skills import skills_list

# Load CSS
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# Database Connection
conn = sqlite3.connect("resume_data.db")
cursor = conn.cursor()

st.title("AI Smart Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description"
)

# Extract Text Function
def extract_text(pdf_file):

    pdf = PdfReader(pdf_file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


if uploaded_file is not None:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Content")
    st.write(resume_text)

    resume_text_lower = resume_text.lower()
    job_description_lower = job_description.lower()

    # Job Skills
    job_skills = []

    for skill in skills_list:

        if skill.lower() in job_description_lower:
            job_skills.append(skill)

    # Matched Skills
    matched_skills = []

    for skill in job_skills:

        if skill.lower() in resume_text_lower:
            matched_skills.append(skill)

    st.subheader("Job Required Skills")
    st.write(job_skills)

    st.subheader("Matched Skills")
    st.write(matched_skills)

    # Score Calculation
    if len(job_skills) > 0:

        score = int(
            (len(matched_skills) / len(job_skills)) * 100
        )

    else:
        score = 0

    st.subheader("Resume Score")

    st.progress(score)

    st.write(
        f"Your Resume Matches {score}% of the Job Description"
    )

    # Missing Skills
    missing_skills = []

    for skill in job_skills:

        if skill not in matched_skills:
            missing_skills.append(skill)

    st.subheader("Missing Skills")
    st.write(missing_skills)

    # Suggestions
    st.subheader("Suggestions")

    if score >= 80:
        st.success("Excellent Resume Match!")

    elif score >= 50:
        st.warning(
            "Good Resume but needs improvement."
        )

    else:
        st.error(
            "Add more technical skills and projects."
        )

    # Save Data in Database
    cursor.execute(
        """
        INSERT INTO resumes
        (resume_name, job_description, score)
        VALUES (?, ?, ?)
        """,
        (
            uploaded_file.name,
            job_description,
            score
        )
    )

    conn.commit()

conn.close()