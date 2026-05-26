import sqlite3
import streamlit as st
from PyPDF2 import PdfReader
from skills import skills_list


st.title("AI Smart Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Enter Job Description"
)

def extract_text(pdf_file):

    pdf = PdfReader(pdf_file)

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

    return text

if uploaded_file is not None:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Content")
    st.write(resume_text)

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    job_skills = []

    for skill in skills_list:

        if skill.lower() in job_description:
            job_skills.append(skill)

    matched_skills = []

    for skill in job_skills:

        if skill.lower() in resume_text:
            matched_skills.append(skill)

    st.subheader("Job Required Skills")
    st.write(job_skills)

    st.subheader("Matched Skills")
    st.write(matched_skills)

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

    missing_skills = []

    for skill in job_skills:

        if skill not in matched_skills:
            missing_skills.append(skill)

    st.subheader("Missing Skills")
    st.write(missing_skills)

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