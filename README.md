# 🎓 AI Internship Navigator

AI Internship Navigator is an intelligent web application that helps students understand which internship roles suit them best, what skills they are missing, and how to prepare effectively over the next 30 days — using a combination of deterministic skill analysis and large language model–powered mentoring.

**Unlike simple resume parsers, this system behaves like a career mentor, not a keyword matcher.**

---

## 🚩 Problem Statement

Students often face these challenges when applying for internships:

- They don't know which roles truly match their current skill level
- Job descriptions feel overwhelming and unclear
- It's hard to identify what to learn next and in what order
- Generic roadmaps and courses don't feel personalized
- Resume feedback is often shallow or automated

As a result, many capable students either:
- Apply to the wrong roles, or
- Get stuck in endless learning without direction

---

## 💡 Solution Overview

AI Internship Navigator solves this by providing:

- **Skill-aware role matching**
- **Transparent skill gap analysis**
- **Mentor-style 30-day learning roadmaps**
- **Clear, human explanations powered by AI**

The system is designed to feel like guidance from a real mentor, not a checklist.

---

## 🧠 How It Works

### 1. Resume & Skill Analysis

- Users upload a resume (PDF/DOCX) or paste skills
- Text is normalized and analyzed deterministically
- Skills are matched against curated role profiles

### 2. Role Matching Engine

Each role (e.g., Data Scientist, ML Engineer, AI Engineer) has a defined skill set.

The system computes:
- Matched skills
- Missing skills
- Match percentage

This ensures explainability and avoids black-box decisions.

### 3. AI-Generated Learning Roadmap

Using a large language model:
- A realistic, human-style 30-day roadmap is generated
- Works whether 1 skill or 20 skills are missing
- Focuses on progression, practice, and confidence building

### 4. AI Mentor Explanations

The AI Mentor explains:
- Why a role fits (or doesn't)
- Why missing skills matter in real internships
- How to practically follow the roadmap

The output is concise, structured, and skimmable — not long essays.

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** – API layer
- **Python** – core logic
- **Groq API** – LLM inference
- **LLaMA-3.3-70B** – mentor-style reasoning

### Frontend
- **Streamlit** – interactive web UI

### AI & Logic
- Deterministic skill extraction & matching
- LLM-powered roadmap generation
- LLM-powered mentor explanations
- Graceful fallbacks for reliability

---

## 🧩 Project Structure

```
ai-internship-navigator/
│
├── backend/
│   ├── main.py              # FastAPI routes
│   ├── skill_mapper.py      # Skill extraction & role matching
│   ├── roadmap.py           # AI-powered roadmap generation
│   ├── ai_explainer.py      # AI mentor explanations
│
├── frontend/
│   └── app.py               # Streamlit UI
│
├── requirements.txt
└── README.md
```

---

## 🎯 Key Design Principles

- **Explainability first** – no opaque decisions
- **Human-centered output** – mentor tone, not robotic
- **User control** – AI explanations are opt-in
- **Scalable architecture** – easy to extend roles & skills
- **Real-world relevance** – mirrors how internships actually work

---

## 🔒 Security & Privacy

- No resume data is stored
- API keys are handled via environment variables
- No hardcoded credentials
- Stateless request handling

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-internship-navigator.git
cd ai-internship-navigator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

**Windows:**
```bash
setx GROQ_API_KEY "your_api_key_here"
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your_api_key_here"
```

Restart your terminal after setting the variable.

### 4. Start Backend

```bash
cd backend
uvicorn main:app --reload
```

### 5. Start Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 📌 Example Use Cases

- Students unsure whether they fit Data Science vs ML vs AI
- Learners transitioning from coursework to internships
- Self-taught developers wanting structured guidance
- Career mentors assisting multiple students

---

## 🌱 Future Improvements

- Internship recommendation links
- Portfolio project suggestions
- Interview question generation
- Skill confidence scoring
- Multi-language support

---

## 👤 Author

**Nitin Pratap Singh**  
B.Tech Computer Science (AI)  
Focused on building practical, human-centric AI systems

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/ai-internship-navigator/issues).

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!