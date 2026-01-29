import os
from groq import Groq




client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"




def call_llm(prompt: str, max_tokens: int = 350) -> str | None:
    """
    Calls Groq LLaMA-3 model with controlled verbosity.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior career mentor. "
                        "You give clear, structured, concise advice. "
                        "You avoid long paragraphs and unnecessary storytelling."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", str(e))
        return None




def fallback_role_explanation(role: str, matched_skills: list, missing_skills: list) -> str:
    return (
        f"**Why {role} fits you**\n\n"
        f"- You already have strong foundations in {', '.join(matched_skills[:4])}.\n"
        f"- These skills are commonly used in real internship tasks.\n"
        f"- Gaps like {', '.join(missing_skills[:3])} are learnable and expected at this stage."
    )


def fallback_roadmap_explanation(role: str) -> str:
    return (
        f"**How to follow this roadmap**\n\n"
        f"- Focus on fundamentals first, then practice.\n"
        f"- Build small projects as you learn.\n"
        f"- After 30 days, aim to be interview-ready, not perfect."
    )



def explain_role_fit(role: str, matched_skills: list, missing_skills: list) -> str:
    prompt = f"""
Explain why the role **{role}** fits the student.

Use EXACTLY this structure:

Section 1: Strengths (3 bullet points)
- Mention how existing skills are used in real internships

Section 2: Skill Gaps (3 bullet points)
- Explain why the missing skills matter in day-to-day work

Section 3: Recommendation (2 bullet points)
- Is this role a good choice right now?
- What to focus on first?

Rules:
- No long paragraphs
- No storytelling
- Clear, practical language

Student skills:
{matched_skills}

Missing skills:
{missing_skills}
"""
    result = call_llm(prompt)

    if result:
        return result

    return fallback_role_explanation(role, matched_skills, missing_skills)


def explain_roadmap(role: str, roadmap: dict) -> str:
    prompt = f"""
Explain how to follow a 30-day roadmap for a **{role} internship**.

Use EXACTLY this structure:

Section 1: First 15 Days (3 bullet points)
- What to focus on
- How to study
- How much practice

Section 2: Practice Strategy (3 bullet points)
- Projects
- Datasets
- Real-world simulation

Section 3: Outcome After 30 Days (3 bullet points)
- Skills
- Confidence
- Internship readiness

Rules:
- Bullet points only
- No long paragraphs
- Be realistic and motivating
"""
    result = call_llm(prompt)

    if result:
        return result

    return fallback_roadmap_explanation(role)
