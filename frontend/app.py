import streamlit as st
import requests

BACKEND_URL = "https://ai-internship-navigator-1.onrender.com"

st.set_page_config(
    page_title="AI Internship Navigator",
    layout="centered"
)



st.title("🎓 AI Internship Navigator")
st.caption("Built with FastAPI, Streamlit, and open-source AI models")

st.write(
    "Upload your resume or paste your skills to discover suitable internship roles, "
    "identify skill gaps, and get a **mentor-style 30-day learning roadmap**."
)



uploaded_file = st.file_uploader(
    "📄 Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

resume_text = st.text_area(
    "✍️ Or paste your resume text / skills here:",
    height=200
)



if st.button("Analyze Profile"):
    if not resume_text.strip() and not uploaded_file:
        st.warning("Please upload a resume or paste your skills.")
    else:
        with st.spinner("Analyzing your profile..."):
            response = requests.post(
                f"{BACKEND_URL}/analyze-resume",
                files={"file": uploaded_file} if uploaded_file else None,
                data={"text": resume_text} if resume_text else None
            )

        if response.status_code == 200:
            analysis = response.json()
            st.session_state["analysis"] = analysis
            st.session_state.pop("roadmap", None)
            st.session_state.pop("explanation", None)

            st.success("Profile analyzed successfully!")

            st.subheader("🧠 Extracted Skills")
            st.write(analysis["extracted_skills"])

            st.subheader("📊 Role Match Analysis")
            for role, data in analysis["role_analysis"].items():
                st.markdown(f"**{role}** — {data['match_percentage']}% match")
                st.write("Matched skills:", data["matched_skills"])
                st.write("Missing skills:", data["missing_skills"])
                st.divider()
        else:
            st.error("Failed to analyze profile.")



if "analysis" in st.session_state:
    st.subheader("🛣️ Generate 30-Day Learning Roadmap")

    selected_role = st.selectbox(
        "Select an internship role:",
        list(st.session_state["analysis"]["role_analysis"].keys())
    )

    if st.button("Generate Roadmap"):
        with st.spinner("Creating your personalized roadmap..."):
            response = requests.post(
                f"{BACKEND_URL}/roadmap",
                json={
                    "role_name": selected_role,
                    "role_analysis": st.session_state["analysis"]["role_analysis"]
                }
            )

        if response.status_code == 200:
            roadmap = response.json()
            st.session_state["roadmap"] = roadmap
            st.session_state["selected_role"] = selected_role
            st.session_state.pop("explanation", None)

        else:
            st.error("Failed to generate roadmap.")



if "roadmap" in st.session_state:
    st.markdown(f"### 📌 30-Day Roadmap for {st.session_state['selected_role']}")

    roadmap = st.session_state["roadmap"]

    if "roadmap_text" in roadmap:
        st.markdown(roadmap["roadmap_text"])
    else:
        st.warning("Roadmap could not be generated.")



if "roadmap" in st.session_state:
    st.subheader("🤖 AI Mentor Explanation")

    if st.button("Explain with AI Mentor 🤖"):
        with st.spinner("AI mentor is explaining your path..."):
            explain_response = requests.post(
                f"{BACKEND_URL}/explain",
                json={
                    "role_name": st.session_state["selected_role"],
                    "role_analysis": st.session_state["analysis"]["role_analysis"]
                }
            )

        if explain_response.status_code == 200:
            st.session_state["explanation"] = explain_response.json()
        else:
            st.error("AI explanation could not be generated.")


if "explanation" in st.session_state:
    explanations = st.session_state["explanation"]

    st.markdown("### 🎯 Why this role fits you")
    st.write(explanations["role_explanation"])

    st.markdown("### 🧭 How to follow this roadmap")
    st.write(explanations["roadmap_explanation"])
