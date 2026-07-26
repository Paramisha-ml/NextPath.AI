import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import random


def load_program_info():
    with open("data/program_info.json", "r") as f:
        return json.load(f)
    
career_skill_map = {

    # ---------- TECH ----------
    "bca": ["html", "css", "javascript", "python", "databases"],
    "b.sc computer science": ["programming", "data structures", "python", "java"],
    "b.tech computer science": ["dsa", "java", "python", "system design"],
    "b.tech ai": ["python", "machine learning", "deep learning"],
    "b.tech data science": ["python", "statistics", "machine learning"],
    "b.sc data science": ["python", "data analysis", "statistics"],
    "b.tech cybersecurity": ["network security", "ethical hacking"],
    "b.tech software engineering": ["oop", "dsa", "software design"],
    "ui/ux design": ["figma", "wireframing", "design thinking"],
    "graphic designing": ["photoshop", "illustrator", "creativity"],
    "animation": ["3d tools", "animation", "creativity"],

    # ---------- BUSINESS ----------
    "bba": ["management", "communication", "marketing"],
    "bms": ["management", "leadership", "business strategy"],
    "bbm": ["management", "operations", "teamwork"],
    "digital marketing": ["seo", "social media", "analytics"],
    "event management": ["planning", "coordination", "communication"],

    # ---------- COMMERCE ----------
    "b.com": ["accounting", "finance", "excel"],
    "baf": ["finance", "accounting"],
    "bbi": ["banking", "finance"],
    "bfm": ["finance", "investment"],
    "ca": ["accounting", "taxation"],
    "cs": ["law", "corporate law"],
    "cma": ["cost accounting"],

    # ---------- MEDICAL ----------
    "mbbs": ["biology", "patient care"],
    "bds": ["dentistry", "biology"],
    "bams": ["ayurveda", "biology"],
    "bhms": ["homeopathy", "biology"],
    "bpt": ["physiotherapy"],
    "b.sc nursing": ["patient care"],
    "b.pharm": ["chemistry", "pharmacy"],
    "biotechnology": ["lab skills", "research"],
    "microbiology": ["lab work", "research"],

    # ---------- ARTS ----------
    "ba psychology": ["human behavior", "analysis"],
    "ba english": ["writing", "communication"],
    "ba history": ["research", "analysis"],
    "ba political science": ["analysis", "governance"],
    "ba sociology": ["social analysis"],
    "bjmc": ["journalism", "communication"],
    "bsw": ["social work", "empathy"],

    # ---------- CREATIVE ----------
    "bfa": ["drawing", "creativity"],
    "content creation": ["video editing", "creativity"],
    "travel & tourism": ["communication", "planning"],
    "hotel management": ["hospitality", "management"]
}

# ---------------- LOAD DATASET ----------------
def load_dataset():
    return pd.read_csv("data/logical_nextpath_dataset.csv")


# ---------------- WEIGHTS ----------------
WEIGHTS = {
    "interest": 0.25,
    "marks": 0.20,
    "goal": 0.15,
    "stream": 0.15,
    "activities": 0.10,
    "exam": 0.10,
    "program": 0.05
}


# ---------------- MARKS SCORE ----------------
def get_marks_score(marks):
    if marks >= 85:
        return 1
    elif marks >= 70:
        return 0.7
    elif marks >= 50:
        return 0.4
    else:
        return 0


def calculate_score(student, career):

    score = 0

    # ---------------- STREAM FILTER (STRICT) ----------------
    if (
    student["stream"].lower() not in str(career["preferred_stream"]).lower()
    and "all streams" not in str(career["preferred_stream"]).lower()
):  return 0
    
    score += 20  # strong base score

    # ---------------- SUBJECT MARKS (MOST IMPORTANT) ----------------
    subject_score = 0
    match_count = 0

    for subject, marks in student["subject_scores"].items():
        if subject.lower() in str(career["key_subjects"]).lower():

            match_count += 1

            if marks >= 85:
                subject_score += 20
            elif marks >= 70:
                subject_score += 15
            elif marks >= 50:
                subject_score += 8
            else:
                subject_score += 2

    if match_count > 0:
        subject_score = subject_score / match_count

    score += subject_score

    # ---------------- INTEREST MATCH (VERY IMPORTANT) ----------------
    career_interests = str(career["interests"]).lower().split(",")

    interest_matches = 0
    for interest in student["interests"]:
        if interest.lower() in career_interests:
            interest_matches += 1
            
    if len(student["interests"]) > 0:
        interest_score = (interest_matches / len(student["interests"])) * 25
        score += interest_score

    # ---------------- STRENGTH / DOMAIN ----------------
    if str(student["strength"]).lower() in str(career["strengths_required"]).lower():
        score += 15

    # ---------------- GOAL MATCH ----------------
    if str(student["goal"]).lower() in str(career["long_term_goals"]).lower():
        score += 15

    # ---------------- EXAM MATCH ----------------
    if "exam" in student:
        if student["exam"].lower() in str(career["competitive_exam"]).lower():
            score += 10

    # ---------------- PROGRAM BOOST ----------------
    if "program" in student:
        if student["program"].lower() in str(career["program_name"]).lower():
            score += 15

    return round(score, 2)

# ---------------- RECOMMENDATION ----------------
def get_recommendations(student_data):

    df = load_dataset()

    # -------- CREATE STUDENT TEXT --------
    student_text = create_student_text(student_data)

    # -------- CREATE CAREER TEXT --------
    career_texts = []

    for _, row in df.iterrows():

        text = (
            str(row["program_name"]) + " " +
            str(row["description"]) + " " +
            str(row["required_skills"]) + " " +
            str(row["interests"]) + " " +
            str(row["preferred_stream"])
        )

        career_texts.append(text.lower())

    # -------- TF-IDF --------
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([student_text] + career_texts)

    # -------- SIMILARITY --------
    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    # -------- STORE RESULTS --------
    results = []

    program_info = load_program_info() 

    def normalize(text):
        return text.lower().replace(".", "").replace(" ", "")

    # normalize JSON keys once
    normalized_programs = {
        normalize(k): v for k, v in program_info.items()
    }

    for i, score in enumerate(similarity):

        career_name = df.iloc[i]["program_name"]
        subjects = student_data.get("subjects", [])
        stream = student_data.get("stream", "")

        medical_fields = ["MBBS", "BDS", "BAMS", "BHMS", "BPT", "B.Sc Nursing"]

        if "Biology" not in subjects:
            if career_name in medical_fields:
                continue   # 🚫 completely skip invalid careers

        if "Biology" in subjects and career_name in medical_fields:
            score += 0.3

        if "Mathematics" in subjects and (
            "B.Tech" in career_name or
            "BCA" in career_name or
            "Data Science" in career_name
        ):
            score += 0.3
        extra = normalized_programs.get(normalize(career_name), {})

        results.append({
            "career": career_name,
            "score": round(score * 100, 2),
            "description": df.iloc[i]["description"],
            "duration": extra.get("duration", "N/A"),
            "students": extra.get("students_in_india", "N/A"),
            "jobs": extra.get("job_roles", []),
            "pg": extra.get("pg_options", []),
            "specializations": extra.get("specializations", [])
        })

    # -------- SORT --------
    
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # REMOVE DUPLICATES
    unique_results = []
    seen = set()

    for r in results:
        if r["career"] not in seen:
            unique_results.append(r)
            seen.add(r["career"])

        if len(unique_results) == 3:
            break

    return unique_results[0], unique_results[1], unique_results[2]

def generate_explanation(student_data, result):

    explanations = []

    stream = student_data.get("stream", "")
    subjects = student_data.get("subjects", [])
    goal = student_data.get("goal", "")
    interests = student_data.get("interests", [])

    # 🔹 Different sentence styles
    stream_lines = [
        f"This program aligns well with your academic background in {stream}.",
        f"Based on your stream ({stream}), this field is a strong match.",
        f"Your educational stream ({stream}) supports this career path."
    ]

    subject_lines = [
        f"Your strong subjects like {', '.join(subjects[:3])} make this a suitable option.",
        f"Performance in {', '.join(subjects[:3])} supports success in this field.",
        f"Your academic strengths in {', '.join(subjects[:3])} align with this program."
    ]

    interest_lines = [
        f"This also connects with your interests such as {', '.join(interests[:2])}.",
        f"Your interests like {', '.join(interests[:2])} further strengthen this recommendation.",
        f"This field matches your interest areas including {', '.join(interests[:2])}."
    ]

    goal_lines = [
        f"This path supports your goal of {goal}.",
        f"It helps you achieve your long-term goal of {goal}.",
        f"This career direction aligns with your future goal: {goal}."
    ]

    closing_lines = [
        "Overall, this is a strong and balanced career option for you.",
        "This makes it a highly suitable recommendation for your profile.",
        "This option fits your profile better than many alternatives."
    ]

    career = result.get("career", "")
    subjects = student_data.get("subjects", [])

    medical_fields = ["MBBS", "BDS", "BAMS", "BHMS", "BPT"]

    # ✅ CONDITIONAL EXPLANATION
    if career in medical_fields and "Biology" not in subjects:
        explanations.append("Note: This option typically requires a Biology background.")
    else:
        explanations.append(random.choice(stream_lines))
    
    if subjects:
        explanations.append(random.choice(subject_lines))
    
    if interests:
        explanations.append(random.choice(interest_lines))

    career = result.get("career", "")

    career_lines = [
        f"The career path of {career} offers strong growth opportunities.",
        f"{career} is a promising field with increasing demand.",
        f"This program leads to careers like {career}, which are highly valuable."
    ]

    explanations.append(random.choice(career_lines))   
    explanations.append(random.choice(goal_lines))
    explanations.append(random.choice(closing_lines))

    return " ".join(explanations)

def create_student_text(student):

    text = ""

    text += student["stream"] + " "
    text += " ".join(student["interests"]) + " "
    text += student["goal"] + " "

    # subjects with good marks
    for sub, marks in student["subject_scores"].items():
        if marks >= 70:
            text += sub + " "

    if "program" in student:
        text += student["program"] + " "

    if "exam" in student:
        text += student["exam"] + " "

    return text.lower()