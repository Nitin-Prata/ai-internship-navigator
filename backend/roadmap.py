# backend/roadmap.py

from typing import List, Dict




def chunk_skills(skills: List[str], chunks: int) -> List[List[str]]:
    """
    Split skills into roughly equal chunks
    """
    if not skills:
        return []

    avg = max(1, len(skills) // chunks)
    return [skills[i:i + avg] for i in range(0, len(skills), avg)]




def generate_30_day_roadmap(missing_skills: List[str]) -> Dict[str, Dict]:
    """
    Generate a simple 30-day roadmap based on missing skills
    """
    roadmap = {}

    if not missing_skills:
        return {
            "message": "You already meet most requirements for this role. Focus on projects and internships."
        }

    weekly_chunks = chunk_skills(missing_skills, 4)

    for week_index, skills in enumerate(weekly_chunks, start=1):
        roadmap[f"Week {week_index}"] = {
            "focus_skills": skills,
            "goals": [
                f"Understand basics of {skill}" for skill in skills
            ],
            "practice": [
                f"Build a small exercise or mini-project using {skill}"
                for skill in skills
            ]
        }

    return roadmap




def build_role_roadmap(role_analysis: Dict[str, Dict], role_name: str) -> Dict:
    """
    Build roadmap for a selected role
    """
    if role_name not in role_analysis:
        return {"error": "Invalid role selected"}

    missing_skills = role_analysis[role_name]["missing_skills"]
    return generate_30_day_roadmap(missing_skills)
