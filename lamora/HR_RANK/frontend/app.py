import streamlit as st
import requests

st.set_page_config(page_title="Resume Ranker", layout="wide")

st.title("📄 Resume Screening Assistant")

job_desc = st.text_area("📝 Enter Job Description", height=200)

uploaded_files = st.file_uploader("📎 Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True)

if st.button("🔍 Analyze Resumes"):
    if not uploaded_files or not job_desc:
        st.warning("Please upload resumes and enter a job description.")
    else:
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                files = {'file': (file.name, file, 'application/pdf')}
                response = requests.post(
                    "http://localhost:8000/parse_resume/",
                    files=files,
                    data={'job_description': job_desc}
                )
                if response.status_code == 200:
                    result = response.json()['result']
                    st.subheader(f"Result for {file.name}")
                    st.markdown(result)
                else:
                    st.error("Error processing the resume.")
