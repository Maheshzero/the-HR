import streamlit as st
import requests

st.set_page_config(page_title="Resume Ranker", layout="wide")
st.title("📄 Resume Screening Assistant")

# --- Initialize session state ---
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""
if "mail_sent" not in st.session_state:
    st.session_state.mail_sent = {}
if "meeting_scheduled" not in st.session_state:
    st.session_state.meeting_scheduled = {}

# --- Job Description Input ---
st.session_state.job_desc = st.text_area(
    "📝 Enter Job Description",
    height=200,
    value=st.session_state.job_desc
)

# --- File Upload ---
uploaded_files_input = st.file_uploader(
    "📎 Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files_input:
    st.session_state.uploaded_files = uploaded_files_input

# --- Analyze Resumes Button ---
if st.button("🔍 Analyze Resumes"):
    if not st.session_state.uploaded_files or not st.session_state.job_desc:
        st.warning("Please upload resumes and enter a job description.")
    else:
        all_results = []

        for file in st.session_state.uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                files = {'file': (file.name, file, 'application/pdf')}
                response = requests.post(
                    "http://localhost:8000/parse_resume/",
                    files=files,
                    data={'job_description': st.session_state.job_desc}
                )

                if response.status_code == 200:
                    try:
                        result = response.json().get("result", [])
                        all_results.extend(result)
                    except Exception:
                        st.error(f"❌ Failed to parse result from {file.name}")
                else:
                    st.error(f"❌ Error processing {file.name}: {response.json().get('error')}")
                    st.text_area("Raw response", value=response.json().get("raw", ""), height=200)

        if all_results:
            st.subheader("🏆 Top Candidates")
            sorted_results = sorted(all_results, key=lambda x: x.get("ranking", 99))

            for idx, candidate in enumerate(sorted_results):
                candidate_id = f"{candidate.get('email')}_{idx}"

                with st.container():
                    st.markdown(f"### 🧑 {candidate.get('name', 'N/A')} (Rank {candidate.get('ranking', '?')})")
                    st.write("📧", candidate.get("email", "N/A"))
                    st.write("📝 Why Top:", candidate.get("why_top", "Not provided"))

                    with st.form(key=f"candidate_form_{idx}"):
                        col1, col2 = st.columns(2)

                        with col1:
                            schedule_meeting = st.form_submit_button(f"📅 Schedule Meeting")
                        with col2:
                            send_mail = st.form_submit_button(f"✉️ Send Mail")

                        if schedule_meeting and not st.session_state.meeting_scheduled.get(candidate_id):
                            response = requests.post("http://localhost:8000/schedule_meeting/", json={
                                "name": candidate.get("name"),
                                "email": candidate.get("email")
                            })
                            if response.status_code == 200:
                                st.session_state.meeting_scheduled[candidate_id] = True
                                st.success(f"✅ Meeting scheduled for {candidate['name']}.")
                            else:
                                st.error("❌ Failed to schedule meeting.")

                        if send_mail and not st.session_state.mail_sent.get(candidate_id):
                            response = requests.post("http://localhost:8000/send_mail/", json={
                                "name": candidate.get("name"),
                                "email": candidate.get("email")
                            })
                            if response.status_code == 200:
                                st.session_state.mail_sent[candidate_id] = True
                                st.success(f"✅ Mail sent to {candidate['email']}.")
                            else:
                                st.error("❌ Failed to send mail.")

                    st.markdown("---")
