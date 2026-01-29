from ai_explainer import explain_role_fit, explain_roadmap
from fastapi import UploadFile, File
from resume_parser import parse_resume
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from skill_mapper import analyze_profile
from roadmap import build_role_roadmap


app = FastAPI(
    title="AI Internship Navigator",
    description="Analyze student skills and generate internship roadmaps",
    version="1.0.0"
)




class AnalyzeRequest(BaseModel):
    text: str


class RoadmapRequest(BaseModel):
    role_name: str
    role_analysis: Dict




@app.post("/analyze")
def analyze_skills(request: AnalyzeRequest):
    """
    Analyze resume or skill text
    """
    result = analyze_profile(request.text)
    return result


@app.post("/roadmap")
def generate_roadmap(request: RoadmapRequest):
    """
    Generate 30-day roadmap for a selected role
    """
    roadmap = build_role_roadmap(
        role_analysis=request.role_analysis,
        role_name=request.role_name
    )
    return roadmap


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze uploaded resume (PDF or DOCX)
    """
    file_bytes = await file.read()
    extracted_text = parse_resume(file_bytes, file.filename)
    result = analyze_profile(extracted_text)
    return result


@app.post("/explain")
def explain_results(request: RoadmapRequest):
    """
    Generate AI explanation for role fit and roadmap
    """
    role = request.role_name
    role_data = request.role_analysis[role]

    role_explanation = explain_role_fit(
        role=role,
        matched_skills=role_data["matched_skills"],
        missing_skills=role_data["missing_skills"]
    )

    roadmap = build_role_roadmap(
        role_analysis=request.role_analysis,
        role_name=role
    )

    roadmap_explanation = explain_roadmap(role, roadmap)

    return {
        "role_explanation": role_explanation,
        "roadmap_explanation": roadmap_explanation
    }
