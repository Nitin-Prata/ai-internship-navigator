
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
