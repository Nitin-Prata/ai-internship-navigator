import re
from typing import Dict, Set, List


SKILL_ALIASES = {
    "machine learning": {"ml", "machine-learning"},
    "deep learning": {"dl", "deep-learning"},
    "natural language processing": {"nlp"},
    "computer vision": {"cv"},
    "scikit-learn": {"sklearn", "scikit learn"},
    "pytorch": {"torch"},
    "tensorflow": {"tf"},
    "large language models": {"llm", "llms"},
}


ALIAS_TO_SKILL = {
    alias: canonical
    for canonical, aliases in SKILL_ALIASES.items()
    for alias in aliases
}



ROLE_SKILLS: Dict[str, Set[str]] = {
    "Data Scientist": {
        "python", "pandas", "numpy", "sql", "statistics",
        "machine learning", "data visualization",
        "matplotlib", "seaborn", "scikit-learn"
    },

    "Machine Learning Engineer": {
        "python", "machine learning", "scikit-learn",
        "deep learning", "tensorflow", "pytorch",
        "model deployment", "api", "fastapi"
    },

    "AI Engineer": {
        "python", "machine learning", "deep learning",
        "natural language processing", "computer vision",
        "large language models", "pytorch",
        "tensorflow", "transformers"
    },

    "Software Engineer": {
        "python", "java", "c++", "data structures",
        "algorithms", "git", "api", "fastapi", "sql"
    }
}




def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\+\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()



def extract_skills(text: str) -> Set[str]:
    """
    Extract skills from resume or skills text using
    canonical skill names and aliases.
    """
    text = normalize_text(text)
    found_skills: Set[str] = set()

    for skills in ROLE_SKILLS.values():
        for skill in skills:
            if re.search(rf"\b{re.escape(skill)}\b", text):
                found_skills.add(skill)

    for alias, canonical in ALIAS_TO_SKILL.items():
        if re.search(rf"\b{re.escape(alias)}\b", text):
            found_skills.add(canonical)

    return found_skills



def match_roles(user_skills: Set[str]) -> Dict[str, Dict]:
    role_analysis = {}

    for role, required_skills in ROLE_SKILLS.items():
        matched = user_skills & required_skills
        missing = required_skills - matched

        score = 0
        for skill in matched:
            score += 1

        match_percentage = round(
            (score / len(required_skills)) * 100, 2
        )

        role_analysis[role] = {
            "match_percentage": match_percentage,
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing)
        }

    return role_analysis


def analyze_profile(input_text: str) -> Dict:
    user_skills = extract_skills(input_text)
    role_matches = match_roles(user_skills)

    return {
        "extracted_skills": sorted(user_skills),
        "role_analysis": role_matches
    }
