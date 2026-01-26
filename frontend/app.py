import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Internship Navigator",
    layout="centered"
)

st.title("🎓 AI Internship Navigator")
st.write(
    "Paste your resume or list your skills. "
    "This tool analyzes your profile and suggests suitable internship roles "
    "along with a 30-day learning roadmap."
)



input_text = st.text_area(
    "Paste your resume text or skills here:",
    height=200
)

analyze_button = st.button("Analyze Profile")



if analyze_button and input_text.strip():
    with st.spinner("Analyzing your profile..."):
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"text": input_text}
        )

    if response.status_code == 200:
        analysis = response.json()
        st.session_state["analysis"] = analysis

        st.success("Profile analyzed successfully!")

        st.subheader("✅ Extracted Skills")
        st.write(analysis["extracted_skills"])

        st.subheader("📊 Role Match Analysis")
        for role, data in analysis["role_analysis"].items():
            st.markdown(f"**{role}** — {data['match_percentage']}% match")
            st.write("Matched skills:", data["matched_skills"])
            st.write("Missing skills:", data["missing_skills"])
            st.markdown("---")
    else:
        st.error("Failed to analyze profile.")



if "analysis" in st.session_state:
    st.subheader("🛣️ Generate 30-Day Roadmap")

    selected_role = st.selectbox(
        "Select a role:",
        list(st.session_state["analysis"]["role_analysis"].keys())
    )

    roadmap_button = st.button("Generate Roadmap")

    if roadmap_button:
        with st.spinner("Building roadmap..."):
            response = requests.post(
                f"{BACKEND_URL}/roadmap",
                json={
                    "role_name": selected_role,
                    "role_analysis": st.session_state["analysis"]["role_analysis"]
                }
            )

        if response.status_code == 200:
            roadmap = response.json()
            st.success(f"30-Day Roadmap for {selected_role}")

            if "message" in roadmap:
                st.info(roadmap["message"])
            else:
                for week, details in roadmap.items():
                    st.markdown(f"### {week}")
                    st.write("**Focus Skills:**", details["focus_skills"])
                    st.write("**Goals:**")
                    for g in details["goals"]:
                        st.write("-", g)
                    st.write("**Practice:**")
                    for p in details["practice"]:
                        st.write("-", p)
        else:
            st.error("Failed to generate roadmap.")
