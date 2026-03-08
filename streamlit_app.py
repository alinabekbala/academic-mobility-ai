import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml
from pathlib import Path
from datetime import datetime

from src.latest_ai_development.crew import MobilityCrew
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Academic Mobility Planner AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LANGUAGE ----------------

language = st.sidebar.selectbox(
    "Language / Язык",
    ["English", "Русский"]
)

def t(en, ru):
    return en if language == "English" else ru


# ---------------- TRANSLATIONS ----------------

T = {
    "title": t("Academic Mobility Planner AI", "AI Планировщик Академической Мобильности"),
    "subtitle": t(
        "Multi-Agent System for Academic Exchange Planning",
        "Мультиагентная система для планирования академического обмена"
    ),
    "home": t("Home", "Главная"),
    "agents": t("Agents Config", "Конфигурация агентов"),
    "tasks": t("Tasks Config", "Конфигурация задач"),
    "run": t("Run Mobility Planner", "Запуск планировщика"),
    "overview": t("Project Overview", "Описание проекта"),
    "upload_info": t(
        "Upload transcript and course catalog to generate mobility recommendations.",
        "Загрузите transcript и каталог курсов для генерации рекомендаций."
    ),
    "upload_transcript": t("Upload Transcript CSV", "Загрузить Transcript CSV"),
    "course_catalog": t("Course Catalog from Partner University", "Каталог курсов университета"),
    "generate": t("Generate Mobility Plan", "Сгенерировать план мобильности"),
    "preview": t("Transcript Preview", "Предпросмотр транскрипции"),
    "visualization": t("Grades Visualization", "Визуализация оценок"),
    "plan": t("Recommended Academic Mobility Plan", "Рекомендованный план мобильности"),
    "download": t("Download Plan", "Скачать план"),
    "error": t(
        "Please upload transcript and paste course catalog.",
        "Пожалуйста загрузите transcript и вставьте каталог курсов."
    ),
}

# ---------------- GPA CALCULATION ----------------

grade_map = {
    "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0
}

def calculate_gpa(df):

    grades = []

    for g in df["grade"]:
        if g in grade_map:
            grades.append(grade_map[g])

    if len(grades) == 0:
        return 0

    return round(sum(grades) / len(grades), 2)


# ---------------- SPECIALIZATION DETECTION ----------------

def detect_specialization(courses):

    text = " ".join(courses).lower()

    if any(x in text for x in ["algorithm", "data structure", "operating system", "network"]):
        return "Computer Engineering"

    if any(x in text for x in ["machine learning", "ai", "neural"]):
        return "Artificial Intelligence"

    if any(x in text for x in ["database", "data mining", "statistics"]):
        return "Data Science"

    return "General Computer Science"


# ---------------- COURSE RECOMMENDATION ----------------

def recommend_courses(spec):

    data = {

        "Computer Engineering": [
            "Advanced Algorithms",
            "Distributed Systems",
            "Computer Architecture"
        ],

        "Artificial Intelligence": [
            "Deep Learning",
            "Natural Language Processing",
            "Computer Vision"
        ],

        "Data Science": [
            "Big Data Analytics",
            "Data Mining",
            "Statistical Modeling"
        ]

    }

    return data.get(spec, ["Software Engineering", "Cloud Computing"])


# ---------------- FILE PATHS ----------------

AGENTS_PATH = Path("src/latest_ai_development/config/agents.yaml")
TASKS_PATH = Path("src/latest_ai_development/config/tasks.yaml")


# ---------------- LOAD SAVE FUNCTIONS ----------------

def load_agents():
    with open(AGENTS_PATH) as f:
        return yaml.safe_load(f)

def save_agents(data):
    with open(AGENTS_PATH, "w") as f:
        yaml.dump(data, f)

def load_tasks():
    with open(TASKS_PATH) as f:
        return yaml.safe_load(f)

def save_tasks(data):
    with open(TASKS_PATH, "w") as f:
        yaml.dump(data, f)


# ---------------- TITLE ----------------

st.title("🎓 " + T["title"])
st.subheader(T["subtitle"])
st.markdown("---")


# ---------------- NAVIGATION ----------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        T["home"],
        T["agents"],
        T["tasks"],
        T["run"]
    ]
)


# ---------------- HOME PAGE ----------------

if page == T["home"]:

    st.header(T["overview"])

    st.write(
        t(
            """
This application uses a CrewAI multi-agent system to automatically generate academic mobility plans.

The system analyzes a student's transcript, detects specialization,
and compares it with a partner university's course catalog
to recommend suitable exchange courses.
""",
            """
Это приложение использует мультиагентную систему CrewAI для автоматической генерации плана академической мобильности.

Система анализирует транскрипт студента, определяет специализацию
и сравнивает её с каталогом курсов университета-партнёра,
чтобы предложить подходящие курсы для академического обмена.
"""
        )
    )

    st.info(T["upload_info"])


# ---------------- AGENTS PAGE ----------------

elif page == T["agents"]:

    st.header("Agents")

    agents = load_agents()

    mode = st.radio("Mode", ["View", "Edit"])

    for name, agent in agents.items():

        st.subheader(name)

        if mode == "View":

            st.markdown("**Role**")
            st.info(agent["role"])

            st.markdown("**Goal**")
            st.success(agent["goal"])

            st.markdown("**Backstory**")
            st.warning(agent["backstory"])

        else:

            role = st.text_input(f"{name} role", agent["role"])
            goal = st.text_area(f"{name} goal", agent["goal"])
            backstory = st.text_area(f"{name} backstory", agent["backstory"])

            agents[name]["role"] = role
            agents[name]["goal"] = goal
            agents[name]["backstory"] = backstory

    if mode == "Edit":

        if st.button("Save Agents"):

            save_agents(agents)

            st.success("Agents updated")


# ---------------- TASKS PAGE ----------------

elif page == T["tasks"]:

    st.header("Tasks")

    tasks = load_tasks()

    mode = st.radio("Mode", ["View", "Edit"], key="task_mode")

    for name, task in tasks.items():

        st.subheader(name)

        if mode == "View":

            st.markdown("**Description**")
            st.info(task["description"])

            st.markdown("**Expected Output**")
            st.success(task["expected_output"])

        else:

            description = st.text_area(f"{name} description", task["description"])
            output = st.text_area(f"{name} expected output", task["expected_output"])

            tasks[name]["description"] = description
            tasks[name]["expected_output"] = output

    if mode == "Edit":

        if st.button("Save Tasks"):

            save_tasks(tasks)

            st.success("Tasks updated")


# ---------------- RUN PAGE ----------------

elif page == T["run"]:

    st.header(T["run"])

    transcript_file = st.file_uploader(
        T["upload_transcript"],
        type=["csv"]
    )

    course_catalog = st.text_area(
        T["course_catalog"],
        height=200
    )

    if transcript_file is not None:

        df = pd.read_csv(transcript_file)

        st.subheader(T["preview"])
        st.dataframe(df)

        gpa = calculate_gpa(df)
        specialization = detect_specialization(df["course"].tolist())
        credits = df["credits"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("GPA", gpa)
        col2.metric("Courses", len(df))
        col3.metric("Credits", credits)

        st.divider()

        st.subheader("Detected Specialization")
        st.success(specialization)

        st.subheader("Recommended Courses")

        rec = recommend_courses(specialization)

        for r in rec:
            st.write("•", r)

        st.subheader(T["visualization"])

        grade_counts = df["grade"].value_counts()

        fig, ax = plt.subplots()

        grade_counts.plot(kind="bar", ax=ax)

        st.pyplot(fig)

    if st.button("🚀 " + T["generate"]):

        if transcript_file is None or course_catalog == "":

            st.error(T["error"])

        else:

            transcript_text = df.to_string(index=False)

            inputs = {

                "transcript": transcript_text,
                "course_catalog": course_catalog,
                "date": datetime.today().strftime("%B %d, %Y")

            }

            with st.spinner("Running AI agents..."):

                result = MobilityCrew().crew().kickoff(inputs=inputs)

            st.success("Mobility Plan Generated!")

            st.subheader(T["plan"])

            st.write(result)

            st.download_button(
                label="📄 " + T["download"],
                data=str(result),
                file_name="mobility_plan.md"
            )