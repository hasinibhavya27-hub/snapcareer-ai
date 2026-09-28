import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SnapCareer AI",
    page_icon="🚀",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_text" not in st.session_state:
    st.session_state.job_text = ""

if "matched_skills" not in st.session_state:
    st.session_state.matched_skills = []

if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []

if "match_percent" not in st.session_state:
    st.session_state.match_percent = 0

if "similarity_percent" not in st.session_state:
    st.session_state.similarity_percent = 0


# =========================================================
# THEME
# =========================================================

dark_mode = st.toggle("🌙 Dark Mode")


if dark_mode:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0e1117;
            color: white;
        }

        .stMarkdown,
        .stText,
        p,
        label,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: white !important;
        }

        textarea,
        input {
            color: white !important;
            background-color: #262730 !important;
        }

        textarea::placeholder,
        input::placeholder {
            color: #aaaaaa !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #ffffff;
            color: #222222;
        }

        .stMarkdown,
        .stText,
        p,
        label,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: #222222 !important;
        }

        textarea,
        input {
            color: #222222 !important;
            background-color: #ffffff !important;
        }

        textarea::placeholder,
        input::placeholder {
            color: #777777 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

st.title("🚀 SnapCareer AI")

st.caption(
    "Your AI-powered career assistant for resume analysis, "
    "skill-gap detection and interview preparation."
)

st.divider()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Analyze Career",
        "🗺️ Career Roadmap",
        "🎤 Interview Coach"
    ]
)


# =========================================================
# SKILL DATABASE
# =========================================================

skills = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Deep Learning",
    "Communication",
    "Git",
    "GitHub",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Django",
    "Flask",
    "C",
    "C++",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "AWS",
    "Azure",
    "Docker",
    "Statistics",
    "Data Visualization"
]


# =========================================================
# FUNCTIONS
# =========================================================

def extract_pdf_text(uploaded_file):

    text = ""

    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        st.error("Could not read the PDF.")

    return text


def extract_skills(text):

    found = []

    text_lower = text.lower()

    for skill in skills:

        if skill.lower() in text_lower:
            found.append(skill)

    return found


def calculate_similarity(resume, job):

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            [resume, job]
        )

        score = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(score * 100, 2)

    except Exception:
        return 0


def create_report(
    resume,
    job,
    matched,
    missing,
    match_percent,
    similarity
):

    report = ""

    report += "SNAPCAREER AI - CAREER ANALYSIS REPORT\n"
    report += "=" * 50 + "\n\n"

    report += "SKILL MATCH\n"
    report += "-" * 30 + "\n"
    report += f"Skill Match: {match_percent}%\n"
    report += f"Text Similarity: {similarity}%\n\n"

    report += "MATCHING SKILLS\n"
    report += "-" * 30 + "\n"

    if matched:

        for skill in matched:
            report += f"- {skill}\n"

    else:
        report += "No matching skills detected.\n"

    report += "\n"

    report += "SKILL GAPS\n"
    report += "-" * 30 + "\n"

    if missing:

        for skill in missing:
            report += f"- {skill}\n"

    else:
        report += "No major skill gaps detected.\n"

    report += "\n"

    report += "CAREER RECOMMENDATIONS\n"
    report += "-" * 30 + "\n"

    if missing:

        for skill in missing:
            report += f"- Learn and practice {skill}\n"

    else:

        report += "- Continue strengthening your existing skills.\n"

    report += "\n"

    report += "INTERVIEW PREPARATION\n"
    report += "-" * 30 + "\n"

    report += "1. Tell me about yourself.\n"
    report += "2. Explain your strongest technical skill.\n"
    report += "3. Describe a project you worked on.\n"
    report += "4. How do you solve a difficult problem?\n"
    report += "5. Why are you interested in this role?\n"

    return report


# =========================================================
# TAB 1 - ANALYZE CAREER
# =========================================================

with tab1:

    st.header("📄 Resume & Job Analysis")

    st.write(
        "Upload your resume and enter the job description "
        "to discover matching skills and skill gaps."
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # RESUME
    # -----------------------------------------------------

    with col1:

        st.subheader("📄 Your Resume")

        uploaded_resume = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"]
        )

        resume_input = st.text_area(
            "Or paste your resume text",
            height=250,
            placeholder="Paste your resume here..."
        )

    # -----------------------------------------------------
    # JOB DESCRIPTION
    # -----------------------------------------------------

    with col2:

        st.subheader("💼 Target Job")

        job_input = st.text_area(
            "Paste Job Description",
            height=250,
            placeholder=(
                "Example:\n\n"
                "We are looking for a Data Analyst Intern.\n\n"
                "Required skills:\n"
                "Python, SQL, Excel, Power BI, Tableau, "
                "Data Analysis, Pandas, Machine Learning, "
                "Communication and Git."
            )
        )

    st.write("")

    analyze_button = st.button(
        "🔍 Analyze My Career",
        type="primary",
        use_container_width=True
    )


    # =====================================================
    # ANALYSIS
    # =====================================================

    if analyze_button:

        resume_text = ""

        if uploaded_resume is not None:

            resume_text = extract_pdf_text(
                uploaded_resume
            )

        elif resume_input.strip():

            resume_text = resume_input

        else:

            st.warning(
                "⚠️ Please upload your resume or paste your resume text."
            )
            st.stop()


        if not job_input.strip():

            st.warning(
                "⚠️ Please enter the target job description."
            )
            st.stop()


        job_text = job_input


        # Extract skills

        resume_skills = extract_skills(
            resume_text
        )

        job_skills = extract_skills(
            job_text
        )


        # Matching skills

        matched = []

        for skill in job_skills:

            if skill.lower() in [
                x.lower() for x in resume_skills
            ]:

                matched.append(skill)


        # Missing skills

        missing = []

        for skill in job_skills:

            if skill.lower() not in [
                x.lower() for x in resume_skills
            ]:

                missing.append(skill)


        # Match percentage

        if len(job_skills) > 0:

            match_percent = round(
                (len(matched) / len(job_skills)) * 100,
                2
            )

        else:

            match_percent = 0


        # Text similarity

        similarity = calculate_similarity(
            resume_text,
            job_text
        )


        # Save results

        st.session_state.analysis_done = True

        st.session_state.resume_text = resume_text

        st.session_state.job_text = job_text

        st.session_state.matched_skills = matched

        st.session_state.missing_skills = missing

        st.session_state.match_percent = match_percent

        st.session_state.similarity_percent = similarity


    # =====================================================
    # RESULTS
    # =====================================================

    if st.session_state.analysis_done:

        st.divider()

        st.header("📊 Career Analysis Results")

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "🎯 Skill Match",
                f"{st.session_state.match_percent}%"
            )

        with m2:

            st.metric(
                "🧠 Text Similarity",
                f"{st.session_state.similarity_percent}%"
            )

        with m3:

            st.metric(
                "📌 Skill Gaps",
                len(st.session_state.missing_skills)
            )


        st.write("")


        # -------------------------------------------------
        # MATCHING SKILLS
        # -------------------------------------------------

        st.subheader("✅ Matching Skills")

        matched = st.session_state.matched_skills

        if matched:

            for skill in matched:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No matching skills detected."
            )


        # -------------------------------------------------
        # SKILL GAPS
        # -------------------------------------------------

        st.subheader("❌ Skills to Improve")

        missing = st.session_state.missing_skills

        if missing:

            for skill in missing:

                st.error(
                    f"• {skill}"
                )

        else:

            st.success(
                "🎉 No major skill gaps detected!"
            )


        # -------------------------------------------------
        # RESUME SUGGESTIONS
        # -------------------------------------------------

        st.subheader("📝 Resume Improvement Suggestions")

        if missing:

            st.info(
                "Consider adding relevant projects, "
                "certifications or practical experience "
                "for the missing skills."
            )

            for skill in missing:

                st.write(
                    f"💡 Add evidence of **{skill}** "
                    "through a project, course or experience."
                )

        else:

            st.success(
                "Your resume contains the main skills "
                "detected in the job description."
            )


        # -------------------------------------------------
        # REPORT
        # -------------------------------------------------

        st.subheader("📥 Download Your Report")

        report = create_report(
            st.session_state.resume_text,
            st.session_state.job_text,
            st.session_state.matched_skills,
            st.session_state.missing_skills,
            st.session_state.match_percent,
            st.session_state.similarity_percent
        )

        st.download_button(
            label="📄 Download Career Report",
            data=report,
            file_name="SnapCareer_AI_Report.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# TAB 2 - CAREER ROADMAP
# =========================================================

with tab2:

    st.header("🗺️ Personalized Career Roadmap")

    if not st.session_state.analysis_done:

        st.info(
            "👆 First analyze your resume in the "
            "'Analyze Career' tab."
        )

    else:

        missing = st.session_state.missing_skills

        st.write(
            "Based on your detected skill gaps, "
            "here is a simple learning roadmap."
        )

        if missing:

            for index, skill in enumerate(
                missing,
                start=1
            ):

                st.info(
                    f"""
**Step {index} — Learn {skill}**

Start with the fundamentals of {skill}.

**Practice:**
- Learn the basic concepts
- Follow beginner tutorials
- Solve small exercises
- Build one mini project
- Add the project to your portfolio
"""
                )

        else:

            st.success(
                """
🎉 Your resume already covers the main skills
detected from the target job.

Next steps:

- Build real-world projects
- Improve your portfolio
- Practice interviews
- Apply for internships
"""
            )


        st.divider()

        st.subheader("🚀 Suggested Career Actions")

        actions = [
            "Build 2–3 practical projects",
            "Improve your GitHub profile",
            "Create a strong LinkedIn profile",
            "Practice technical interviews",
            "Practice explaining your projects",
            "Apply for internships and entry-level roles"
        ]

        for action in actions:

            st.checkbox(
                action,
                key=f"action_{action}"
            )


# =========================================================
# TAB 3 - INTERVIEW COACH
# =========================================================

with tab3:

    st.header("🎤 Interview Coach")

    if not st.session_state.analysis_done:

        st.info(
            "👆 Analyze your resume first to unlock "
            "interview preparation."
        )

    else:

        st.write(
            "Practice these questions before your interview."
        )


        questions = [

            (
                "Tell me about yourself.",
                "Keep your answer around 60–90 seconds. "
                "Mention your education, skills, projects "
                "and career interest."
            ),

            (
                "Explain your strongest technical skill.",
                "Choose one skill from your resume and "
                "explain where you used it."
            ),

            (
                "Tell me about one project you worked on.",
                "Explain the problem, your solution, "
                "technologies used and result."
            ),

            (
                "What are your current skill gaps?",
                "Be honest and explain how you are "
                "working to improve them."
            ),

            (
                "Why are you interested in this role?",
                "Connect your skills, projects and career "
                "interest with the role."
            ),

            (
                "How do you solve a difficult problem?",
                "Explain your approach step-by-step and "
                "give a practical example."
            ),

            (
                "Where do you see yourself in the future?",
                "Talk about your learning goals and "
                "professional growth."
            )

        ]


        for number, item in enumerate(
            questions,
            start=1
        ):

            question = item[0]
            tip = item[1]

            with st.expander(
                f"Question {number}: {question}"
            ):

                st.write(
                    f"💡 **Tip:** {tip}"
                )

                st.text_area(
                    "Your answer",
                    height=120,
                    key=f"answer_{number}",
                    placeholder="Type your answer here..."
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🚀 SnapCareer AI | On-Device AI Career Assistant | "
    "Privacy-first career preparation"
)
