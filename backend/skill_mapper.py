
import re
from typing import List, Dict, Set




ROLE_SKILLS = {
    "Data Scientist": {
        "python", "pandas", "numpy", "sql", "statistics",
        "machine learning", "data visualization", "matplotlib",
        "seaborn", "scikit-learn"
    },

    "Machine Learning Engineer": {
        "python", "machine learning", "scikit-learn",
        "deep learning", "tensorflow", "pytorch",
        "model deployment", "api", "fastapi"
    },

    "AI Engineer": {
        "python", "machine learning", "deep learning",
        "nlp", "computer vision", "transformers",
        "llm", "pytorch", "tensorflow"
    },

    "Software Engineer": {
        "python", "java", "c++", "data structures",
        "algorithms", "git", "api", "fastapi",
        "sql"
    }
}




def normalize_text(text: str) -> str:
    """
    Lowercase and remove special characters
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def extract_skills(text: str) -> Set[str]:
    """
    Extract skills from resume or skill text
    """
    text = normalize_text(text)
    found_skills = set()

    for role, skills in ROLE_SKILLS.items():
        for skill in skills:
            if skill in text:
                found_skills.add(skill)

    return found_skills




def match_roles(user_skills: Set[str]) -> Dict[str, Dict]:
    """
    Match user skills with each role and calculate match score
    """
    role_analysis = {}

    for role, required_skills in ROLE_SKILLS.items():
        matched = user_skills.intersection(required_skills)
        missing = required_skills - matched

        match_percentage = round(
            (len(matched) / len(required_skills)) * 100, 2
        )

        role_analysis[role] = {
            "match_percentage": match_percentage,
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing))
        }

    return role_analysis




def analyze_profile(input_text: str) -> Dict:
    """
    Main function to analyze resume or skills text
    """
    user_skills = extract_skills(input_text)
    role_matches = match_roles(user_skills)

    return {
        "extracted_skills": sorted(list(user_skills)),
        "role_analysis": role_matches
    }
