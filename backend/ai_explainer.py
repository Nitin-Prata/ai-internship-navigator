import requests
import os


HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

HF_HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}


def call_llm(prompt: str, max_tokens: int = 300) -> str:
    """
    Call Hugging Face Inference API
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.6,
            "return_full_text": False
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=HF_HEADERS,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        return "AI explanation is temporarily unavailable."

    output = response.json()

    if isinstance(output, list) and "generated_text" in output[0]:
        return output[0]["generated_text"].strip()

    return "AI explanation could not be generated."




def explain_role_fit(role: str, matched_skills: list, missing_skills: list) -> str:
    prompt = f"""
You are a career mentor for students.

Explain in simple, clear English why the role "{role}" is suitable
based on these matched skills: {matched_skills}.

Also gently explain what skills are missing: {missing_skills},
and why learning them matters.

Keep the explanation practical and encouraging.
"""
    return call_llm(prompt)


def explain_roadmap(role: str, roadmap: dict) -> str:
    prompt = f"""
You are an AI mentor.

Explain how a student should follow this 30-day learning roadmap
to prepare for a {role} internship.

Roadmap:
{roadmap}

Explain step-by-step, in a motivating and realistic tone.
"""
    return call_llm(prompt)
