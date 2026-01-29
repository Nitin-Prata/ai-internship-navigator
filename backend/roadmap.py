import os
from typing import Dict, List
from groq import Groq



client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"


def generate_ai_roadmap(role_name: str, missing_skills: List[str]) -> Dict[str, Dict]:
    """
    Generate a fully human, GPT-style 30-day roadmap using an LLM.
    This works regardless of how many skills are missing.
    """

    skills_text = (
        ", ".join(missing_skills)
        if missing_skills
        else "No major missing skills. Focus on strengthening fundamentals and projects."
    )

    prompt = f"""
You are an experienced industry mentor who has guided many interns.

A student wants to prepare for a **{role_name} internship** over the next 30 days.

The student’s current skill gaps or focus areas are:
{skills_text}

Create a **realistic, human, 4-week (30-day) roadmap** that:
- Feels like advice from a real mentor
- Explains *why* each week matters
- Shows progression and confidence building
- Includes learning, practice, and outcomes
- Does NOT sound like a syllabus or textbook

Format the roadmap clearly as:

Week 1:
- Focus
- What to learn
- What to practice
- Outcome

Week 2:
...

Week 3:
...

Week 4:
...

Use natural language. Be encouraging, honest, and practical.
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior AI and software mentor. "
                        "You give practical, realistic guidance and avoid generic advice."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=900
        )

        text = completion.choices[0].message.content.strip()

        return {
            "roadmap_text": text
        }

    except Exception as e:
        print("GROQ ROADMAP ERROR:", str(e))

        return {
            "roadmap_text": (
                "This 30-day roadmap focuses on building confidence through consistent learning "
                "and hands-on practice. Each week should strengthen your understanding, improve "
                "real-world application, and prepare you for internship-level expectations."
            )
        }


def build_role_roadmap(role_analysis: Dict[str, Dict], role_name: str) -> Dict:
    """
    Build a 30-day roadmap for a selected role using LLM logic.
    """

    if role_name not in role_analysis:
        return {"error": "Invalid role selected"}

    missing_skills = role_analysis[role_name].get("missing_skills", [])

    return generate_ai_roadmap(role_name, missing_skills)
