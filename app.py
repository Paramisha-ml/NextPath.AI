# cd Documents
# cd NextPath_AI 
# streamlit run app.py 

import streamlit as st
import base64
from recommendation_engine import (
    get_recommendations,
    generate_explanation
)

import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NextPath AI",
    layout="wide"
)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "results" not in st.session_state:
    st.session_state.results = []

# ---------------- LOAD CSS ----------------
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 NextPath AI")

menu = st.sidebar.radio("", ["Home", "School Analysis", "Saved", "More"])

if menu == "Home":
    st.session_state.page = "home"

elif menu == "School Analysis":
    st.session_state.page = "school_analysis"

elif menu == "More":
    st.session_state.page = "more"

elif menu == "Saved":
    st.session_state.page = "saved"

# ---------------- IMAGE LOADER ----------------
def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo = get_base64_image("assets/logo.png")
school = get_base64_image("assets/school.png")
road = get_base64_image("assets/road.png")
college = get_base64_image("assets/college.png")

# ================= HOME PAGE =================
if st.session_state.page == "home":

    # st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Logo
    st.markdown(f'<img src="data:image/png;base64,{logo}" class="logo-img">', unsafe_allow_html=True)

    # Title
    st.markdown('<div class="app-title">NextPath AI</div>', unsafe_allow_html=True)

    # Tagline
    st.markdown('<div class="tagline">Smart Career Guidance Powered by AI</div>', unsafe_allow_html=True)

    # -------- Images Row --------

    st.markdown(f"""
    <div class="journey-container">
        <img src="data:image/png;base64,{school}">
        <img src="data:image/png;base64,{road}">
        <img src="data:image/png;base64,{college}">
    </div>
    """, unsafe_allow_html=True)

    # -------- Description --------
    st.markdown("""
    <div style='text-align:center; font-size:18px; color:#cccccc; margin-top:20px;'>
    Start your journey from school to a successful future 🚀<br>
    Discover the best career path based on your strengths, interests, and goals.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- Button --------
    if st.button("🚀 Start Career Analysis", key="home_btn"):
        st.session_state.page = "school_analysis"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= SCHOOL ANALYSIS =================
elif st.session_state.page == "school_analysis":

    st.markdown("<h1 style='text-align:center;'>🎓 School Career Analysis</h1>", unsafe_allow_html=True)

    # ---------------- STREAM ----------------
    stream = st.selectbox(
        "Select your Stream (Class 11–12)",
        ["Science (Biology)", "Science (Mathematics)", "Commerce", "Arts / Humanities"]
    )

    # ---------------- SUBJECTS BASED ON STREAM ----------------
    stream_subjects = {
        "Science (Biology)": ["Biology", "Physics", "Chemistry"],
        "Science (Mathematics)": ["Mathematics", "Physics", "Chemistry"],
        "Commerce": ["Accountancy", "Business Studies", "Economics"],
        "Arts / Humanities": ["History", "Political Science", "Geography", "Psychology"]
    }

    # ---------------- SUBJECTS ----------------
    st.markdown("### 📊 Subject Performance (0–100)")

    subject_scores = {}

    # -------- MAJOR SUBJECTS --------
    st.markdown("#### ✅ Major Subjects")

    major_subjects = {
        "Science (Biology)": ["Biology", "Physics", "Chemistry"],
        "Science (Mathematics)": ["Mathematics", "Physics", "Chemistry"],
        "Commerce": ["Accountancy", "Business Studies", "Economics"],
        "Arts / Humanities": ["History", "Political Science", "Geography", "Sociology", "Psychology", "Economics"]
    }

    for sub in major_subjects[stream]:
        subject_scores[sub] = st.slider(f"{sub}", 0, 100, 50)


    # -------- MINOR SUBJECTS --------
    st.markdown("#### 🔹 Minor / Optional Subjects")

    minor_subjects = {
        "Science (Biology)": [
            "English", "Physical Education", "Computer Science",
            "Informatics Practices", "Mathematics", "Hindi"
        ],
        "Science (Mathematics)": [
            "English", "Computer Science", "Informatics Practices",
            "Physical Education", "Engineering Graphics", "Hindi"
        ],
        "Commerce": [
            "English", "Mathematics", "Informatics Practices",
            "Computer Science", "Physical Education",
            "Entrepreneurship", "Hindi"
        ],
        "Arts / Humanities": [
            "English", "Hindi", "Fine Arts",
            "Physical Education", "Computer Science",
            "Informatics Practices", "Home Science"
        ]
    }

    # Optional: Ask only selected minor subjects
    selected_minors = st.multiselect(
        "Select your minor subjects",
        minor_subjects[stream]
    )

    for sub in selected_minors:
        subject_scores[sub] = st.slider(f"{sub}", 0, 100, 50)

    # ---------------- INTERESTS ----------------
    st.markdown("### 🎯 Personal Interests")

    selected_interests = []

    def interest_section(title, options):
        with st.expander(title):
            return st.multiselect("Select from below", options)

    # -------- ALL DOMAINS --------
    tech = interest_section("💻 Tech & Analytical Interests", [
        "Coding / Programming", "App Development", "Web Development",
        "Artificial Intelligence / Machine Learning", "Data Analysis",
        "Cybersecurity", "Robotics", "Problem Solving / Logical Puzzles"
    ])

    science = interest_section("🔬 Science & Research Interests", [
        "Biology / Life Sciences", "Medical Field / Healthcare",
        "Chemistry Experiments", "Physics Concepts",
        "Scientific Research", "Environmental Science"
    ])

    business = interest_section("💼 Business & Management Interests", [
        "Business / Startups", "Entrepreneurship",
        "Finance / Investment", "Marketing / Advertising",
        "Economics / Market Trends", "Management & Leadership"
    ])

    creative = interest_section("🎨 Creative & Design Interests", [
        "Graphic Designing", "UI/UX Design", "Drawing / Sketching",
        "Painting", "Animation / 3D Design",
        "Video Editing", "Photography"
    ])

    communication = interest_section("📢 Communication & Social Interests", [
        "Public Speaking", "Teaching / Mentoring",
        "Writing / Blogging", "Social Work",
        "Psychology / Understanding People", "Law / Debate"
    ])

    arts = interest_section("🎭 Arts & Humanities Interests", [
        "History", "Political Science", "Sociology",
        "Philosophy", "Literature"
    ])

    personality = interest_section("🧠 Personality-Based Interests", [
        "Leadership Roles", "Teamwork Activities",
        "Independent Work", "Helping Others",
        "Organizing Events"
    ])

    practical = interest_section("⚙️ Practical & Field Interests", [
        "Hands-on Work", "Mechanical Work",
        "Field Work", "Traveling-based Jobs",
        "Outdoor Activities"
    ])

    modern = interest_section("🎮 Modern & General Interests", [
        "Gaming", "Content Creation (YouTube, Instagram)",
        "Blogging / Influencing", "Technology Trends",
        "Learning New Tools"
    ])

    # -------- COMBINE ALL --------
    selected_interests = (
        tech + science + business + creative +
        communication + arts + personality +
        practical + modern
    )

    # Limit to 5
    if len(selected_interests) > 5:
        st.warning("⚠️ Select maximum 5 interests only.")
        selected_interests = selected_interests[:5]

    interests = selected_interests

    # ---------------- GOAL ----------------
    st.markdown("### 🎯 Long-Term Goal")

    goal = st.selectbox(
        "Select your goal",
        [
            "High Paying Job",
            "Research & Innovation",
            "Entrepreneurship",
            "Government Job",
            "Creative Career",
            "Helping Society",
            "Teaching"
        ]
    )

    # ---------------- COMPETITIVE EXAMS ----------------
    st.markdown("### 📝 Competitive Exam Readiness")

    exam_data = {
        "Science (Biology)": [
            "NEET", "AIIMS", "JIPMER",
            "CUET Life Sciences", "State Medical Exams", "Pharmacy Entrance"
        ],
        "Science (Mathematics)": [
            "JEE Main", "JEE Advanced", "BITSAT",
            "CUET Engineering", "State Engg Exams", "NDA"
        ],
        "Commerce": [
            "CA Foundation", "CSEET", "CMA Foundation",
            "CUET Commerce", "IPMAT", "NPAT", "SET"
        ],
        "Arts / Humanities": [
            "CUET Arts", "CLAT", "AILET",
            "NIFT", "NID", "Hotel Mgmt", "UPSC Awareness"
        ]
    }

    common_exams = [
        "CUET", "NDA", "SSC", "Banking Exams",
        "Not preparing", "Still deciding", "Other"
    ]

    # ✅ Combine + remove duplicates properly
    all_exams = list(set(exam_data[stream] + common_exams))

    # ✅ Clean sorted dropdown
    exams = st.multiselect(
        "Select exams you are preparing for",
        sorted(all_exams)
    )

   # ---------------- PROGRAMS ----------------
    st.markdown("### 🎓 Programs You Are Considering")

    program_data = {
        "Science (Biology)": [
            "MBBS","BDS","BAMS","BHMS","BPT",
            "B.Sc Nursing","B.Pharm",
            "B.Sc Biotechnology","B.Sc Microbiology",
            "B.Sc Genetics","B.Sc Agriculture","BMLT"
        ],
        "Science (Mathematics)": [
            "B.Tech","B.Tech AI & ML","B.Tech Data Science",
            "B.Sc Mathematics","BCA","B.Sc Computer Science","B.Sc IT",
            "B.Sc Data Science","B.Sc AI","B.Sc Statistics",
            "B.Sc Physics","B.Arch","B.Des","NDA"
        ],
        "Commerce": [
            "B.Com","BBA","BMS",
            "CA","CS","CMA",
            "B.Com + LLB","BBA + MBA",
            "BAF","BBI","BFM","BHM"
        ],
        "Arts / Humanities": [
            "BA","BA Psychology","BA Political Science",
            "BA History","BA Sociology","BA English",
            "BA + LLB","BJMC","BSW",
            "BFA","B.Des","Animation & Multimedia",
            "Travel & Tourism","Hotel Management"
        ]
    }

    common_programs = [
        "BCA","B.Sc IT","B.Sc Computer Science","B.Sc Data Science",
        "Diploma in Computer Applications",
        "BBA","BMS","BBM","Event Management",
        "Graphic Designing","UI/UX Design",
        "Digital Marketing","Content Creation",
        "Travel & Tourism","BSW"
    ]

    # ✅ Combine + remove duplicates
    all_programs = list(set(program_data[stream] + common_programs))

    # ✅ Clean dropdown
    programs = st.multiselect(
        "Select programs you are interested in",
        sorted(all_programs)
    )

    # ---------------- RUN ANALYSIS ----------------
    if st.button("🚀 Start AI Career Analysis", key="analysis_btn"):

        student_data = {
            "stream": stream,
            "subject_scores": subject_scores,
            "interests": interests,
            "strength": interests[0] if interests else "",
            "goal": goal,
            "program": ", ".join(programs),
            "exam": ", ".join(exams)
        }

        top1, top2, top3 = get_recommendations(student_data)

        # SAVE RESULTS IN SESSION
        st.session_state.results = [top1, top2, top3]
        st.session_state.student_data = student_data

        # SAVE HISTORY
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "results": [top1, top2, top3],
            "student": student_data
        })

# ---------------- SHOW RESULTS ----------------
if "results" in st.session_state and st.session_state.results:

    st.markdown("## 🎯 Your AI Recommendations")

    results = st.session_state.results

    for i, res in enumerate(results):

        with st.expander(f"🏆 Option {i+1}: {res['career']} (Score: {res['score']})"):

            st.progress(res['score'] / 100)

            # WHY
            explanation = generate_explanation(
                st.session_state.student_data,
                res
            )

            st.write("### 🤖 Why this was recommended")
            st.write(explanation)

            # ✅ NEW SECTION (ADD THIS)
            st.write("### 📊 Career Details")

            st.write(f"⏳ Duration: {res.get('duration', 'N/A')}")
            st.write(f"👨‍🎓 Students in India: {res.get('students', 'N/A')}")

            st.write(f"💼 Job Roles:")
            st.write(", ".join(res.get("jobs", [])))

            st.write(f"🎓 PG Options:")
            st.write(", ".join(res.get("pg", [])))

            st.write(f"📚 Specializations:")
            st.write(", ".join(res.get("specializations", [])))
            
elif st.session_state.page == "saved":

    st.title("📂 Saved Analysis")

    if "history" not in st.session_state or len(st.session_state.history) == 0:
        st.warning("No saved results yet.")
    else:
        for i, item in enumerate(st.session_state.history[::-1]):

            st.markdown(f"### 🔹 Analysis {i+1}")

            for res in item["results"]:
                st.write(f"{res['career']} (Score: {res['score']})")

            st.markdown("---")

elif st.session_state.page == "more":

    st.title("ℹ️ More About App")

    # ---------------- APP INFO ----------------
    st.markdown("## 📱 App Name & Version")
    st.write("NextPath AI")
    st.write("Version: 1.0.0")

    # ---------------- ABOUT ----------------
    st.markdown("## 📝 About the App")
    st.write("""
    NextPath AI helps school students (Class 11–12) choose the right college program 
    based on their interests, marks, and goals. It provides the top 3 program 
    recommendations with match score and insights to help students make better career decisions.
    """)

    # ---------------- DEVELOPER ----------------
    st.markdown("## 👨‍💻 Developer")
    st.write("Paramisha Malviya")

    # ---------------- CONTACT ----------------
    st.markdown("## 📧 Contact Details")
    st.write("Email: paramishamalviya@gmail.com")
    st.markdown("[LinkedIn Profile](https://linkedin.com/in/paramisha-malviya-162790358)")

    # ---------------- TERMS ----------------
    st.markdown("## 📜 Terms & Conditions")
    st.write("""
    - This app provides guidance only, not final decisions  
    - Results are based on user input and AI logic  
    - Users are advised to verify before making career decisions  
    """)

    # ---------------- FEEDBACK DISPLAY ----------------
    st.markdown("## ⭐ Feedback / Rate App")
    st.write("Rate this app ⭐⭐⭐⭐⭐")
    st.write("Give your feedback to improve the system")

    # ---------------- FEEDBACK INPUT ----------------
    st.markdown("### ✍️ Write Your Feedback")

    name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback")

    st.markdown("### ⭐ Rate the App")

    rating = st.radio(
        "Select Rating",
        ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
        horizontal=True
    )

    rating_value = len(rating)   # ⭐⭐⭐ → 3
    
    if st.button("Submit Feedback"):

        new_data = pd.DataFrame({
            "Name": [name],
            "Feedback": [feedback],
            "Rating": [rating_value],
            "Time": [datetime.now()]
        })

        try:
            old_data = pd.read_excel("feedback.xlsx")
            updated_data = pd.concat([old_data, new_data], ignore_index=True)
        except:
            updated_data = new_data

        updated_data.to_excel("feedback.xlsx", index=False)

        st.success("✅ Feedback saved successfully!")

    # ---------------- FAQ ----------------
    st.markdown("## ❓ Help / FAQ")

    with st.expander("Q1. How does this app work?"):
        st.write("It analyzes your inputs and suggests best programs")

    with st.expander("Q2. Is this 100% accurate?"):
        st.write("No, it is guidance-based")

    with st.expander("Q3. Can I change my inputs?"):
        st.write("Yes, you can re-run analysis anytime")
        