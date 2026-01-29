import streamlit as st
import requests

# -----------------------------
# Config
# -----------------------------

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Internship Navigator",
    layout="centered"
)

# -----------------------------
# UI Header
# -----------------------------

st.title("🎓 AI Internship Navigator")
st.caption("Built with FastAPI, Streamlit, and open-source AI models")

st.write(
    "Upload your resume or paste your skills to discover suitable internship roles, "
    "identify skill gaps, and get a 30-day personalized learning roadmap."
)

# -----------------------------
# Resume Input Section
# -----------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

input_text = st.text_area(
    "✍️ Or paste your resume text / skills here:",
    height=200
)

analyze_button = st.button("🔍 Analyze Profile")

# -----------------------------
# Analyze Profile
# -----------------------------

if analyze_button and (uploaded_file or input_text.strip()):
    with st.spinner("Analyzing your profile..."):

        if uploaded_file:
            response = requests.post(
                f"{BACKEND_URL}/analyze-resume",
                files={"file": uploaded_file}
            )
        else:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={"text": input_text}
            )

    if response.status_code == 200:
        analysis = response.json()
        st.session_state["analysis"] = analysis

        st.success("✅ Profile analyzed successfully!")

        st.subheader("🧠 Extracted Skills")
        st.write(analysis["extracted_skills"])

        st.subheader("📊 Role Match Analysis")

        for role, data in analysis["role_analysis"].items():
            st.markdown(f"### {role} — {data['match_percentage']}% match")
            st.write("**Matched skills:**", data["matched_skills"])
            st.write("**Missing skills:**", data["missing_skills"])
            st.divider()

    else:
        st.error("❌ Failed to analyze profile.")

# -----------------------------
# Roadmap Section
# -----------------------------

if "analysis" in st.session_state:
    st.subheader("🛣️ Generate 30-Day Learning Roadmap")

    selected_role = st.selectbox(
        "Select an internship role:",
        list(st.session_state["analysis"]["role_analysis"].keys())
    )

    roadmap_button = st.button("📅 Generate Roadmap")

    if roadmap_button:
        with st.spinner("Building your roadmap..."):
            response = requests.post(
                f"{BACKEND_URL}/roadmap",
                json={
                    "role_name": selected_role,
                    "role_analysis": st.session_state["analysis"]["role_analysis"]
                }
            )

        if response.status_code == 200:
            roadmap = response.json()
            st.success(f"📌 30-Day Roadmap for {selected_role}")

            if "message" in roadmap:
                st.info(roadmap["message"])
            else:
                for week, details in roadmap.items():
                    st.markdown(f"### {week}")
                    st.write("**Focus Skills:**", details["focus_skills"])

                    st.write("**Goals:**")
                    for g in details["goals"]:
                        st.write("- ", g)

                    st.write("**Practice:**")
                    for p in details["practice"]:
                        st.write("- ", p)

        else:
            st.error("❌ Failed to generate roadmap.")

# -----------------------------
# AI Explanation Section
# -----------------------------

if "analysis" in st.session_state:
    st.subheader("🤖 AI Mentor Explanation")

    explain_button = st.button("🧠 Explain with AI")

    if explain_button:
        with st.spinner("AI is explaining your results..."):
            response = requests.post(
                f"{BACKEND_URL}/explain",
                json={
                    "role_name": selected_role,
                    "role_analysis": st.session_state["analysis"]["role_analysis"]
                }
            )

        if response.status_code == 200:
            explanations = response.json()

            st.markdown("### 🎯 Why this role fits you")
            st.write(explanations["role_explanation"])

            st.markdown("### 🧭 How to follow this roadmap")
            st.write(explanations["roadmap_explanation"])

        else:
            st.error("❌ AI explanation could not be generated.")
