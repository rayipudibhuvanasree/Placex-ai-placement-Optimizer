# ============================================================
# PLACEX AI
# AI-POWERED PLACEMENT INTELLIGENCE & OPTIMIZATION
# COMPLETE LEVEL 1 - LEVEL 9
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import random

from datetime import date, time, datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import IsolationForest


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PLACEX AI",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "placex.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # STUDENTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE,
            name TEXT,
            branch TEXT,
            year INTEGER,
            cgpa REAL
        )
    """)

    # --------------------------------------------------------
    # COMPANIES
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            students_required INTEGER,
            drive_date TEXT
        )
    """)

    # --------------------------------------------------------
    # ROOMS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT,
            capacity INTEGER
        )
    """)

    # Add new room columns if they don't already exist
    cursor.execute("PRAGMA table_info(rooms)")
    room_columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "room_type" not in room_columns:
        cursor.execute("""
            ALTER TABLE rooms
            ADD COLUMN room_type TEXT DEFAULT 'Computer Lab'
        """)

    if "available_from" not in room_columns:
        cursor.execute("""
            ALTER TABLE rooms
            ADD COLUMN available_from TEXT DEFAULT '09:00'
        """)

    if "available_until" not in room_columns:
        cursor.execute("""
            ALTER TABLE rooms
            ADD COLUMN available_until TEXT DEFAULT '17:00'
        """)

    # --------------------------------------------------------
    # PLACEMENT DRIVES
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            round_name TEXT,
            drive_date TEXT,
            start_time TEXT,
            duration INTEGER
        )
    """)

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student TEXT,
            company TEXT,
            round_name TEXT,
            topic TEXT,
            score REAL,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# SAMPLE DATA
# ============================================================

def add_sample_data():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # STUDENTS
    # --------------------------------------------------------

    students = [
        ("PX001", "Rahul", "BCA Data Science", 2, 8.4),
        ("PX002", "Anjali", "BCA Data Science", 2, 8.8),
        ("PX003", "Kiran", "BCA", 2, 7.9),
        ("PX004", "Priya", "BCA Data Science", 2, 9.1),
        ("PX005", "Arjun", "BCA", 3, 8.6),
        ("PX006", "Sneha", "BCA", 3, 8.9),
        ("PX007", "Vishal", "BCA", 3, 7.7),
        ("PX008", "Meghana", "BCA Data Science", 3, 9.0)
    ]

    for student in students:

        cursor.execute("""
            INSERT OR IGNORE INTO students
            (roll_no, name, branch, year, cgpa)
            VALUES (?, ?, ?, ?, ?)
        """, student)

    # --------------------------------------------------------
    # COMPANIES
    # --------------------------------------------------------

    companies = [
        ("TechNova", "Python Developer", 5, "2026-10-10"),
        ("DataSphere", "Data Analyst", 4, "2026-10-12"),
        ("CloudCore", "Cloud Engineer", 3, "2026-10-15")
    ]

    for company in companies:

        cursor.execute("""
            SELECT COUNT(*)
            FROM companies
            WHERE name = ?
            AND role = ?
        """, (
            company[0],
            company[1]
        ))

        if cursor.fetchone()[0] == 0:

            cursor.execute("""
                INSERT INTO companies
                (name, role, students_required, drive_date)
                VALUES (?, ?, ?, ?)
            """, company)

    # --------------------------------------------------------
    # ROOMS
    # --------------------------------------------------------

    rooms = [
        (
            "Computer Lab A",
            40,
            "Computer Lab",
            "09:00",
            "17:00"
        ),
        (
            "Computer Lab B",
            50,
            "Computer Lab",
            "09:00",
            "17:00"
        ),
        (
            "Computer Lab C",
            35,
            "Computer Lab",
            "09:00",
            "17:00"
        ),
        (
            "Seminar Hall",
            100,
            "Seminar Hall",
            "09:00",
            "18:00"
        )
    ]

    for room in rooms:

        cursor.execute("""
            SELECT COUNT(*)
            FROM rooms
            WHERE room_name = ?
        """, (room[0],))

        if cursor.fetchone()[0] == 0:

            cursor.execute("""
                INSERT INTO rooms
                (
                    room_name,
                    capacity,
                    room_type,
                    available_from,
                    available_until
                )
                VALUES (?, ?, ?, ?, ?)
            """, room)

    # --------------------------------------------------------
    # SAMPLE RESULTS
    # --------------------------------------------------------

    results = [
        ("Rahul", "TechNova", "Aptitude", "Quantitative", 82, "Passed"),
        ("Rahul", "TechNova", "Technical", "Python", 76, "Passed"),
        ("Rahul", "TechNova", "Technical", "SQL", 65, "Passed"),

        ("Anjali", "TechNova", "Aptitude", "Quantitative", 91, "Passed"),
        ("Anjali", "TechNova", "Technical", "Python", 88, "Passed"),
        ("Anjali", "TechNova", "Technical", "SQL", 79, "Passed"),

        ("Kiran", "TechNova", "Aptitude", "Quantitative", 63, "Passed"),
        ("Kiran", "TechNova", "Technical", "Python", 48, "Failed"),
        ("Kiran", "TechNova", "Technical", "SQL", 51, "Failed"),

        ("Priya", "DataSphere", "Aptitude", "Logical Reasoning", 94, "Passed"),
        ("Priya", "DataSphere", "Technical", "Python", 92, "Passed"),
        ("Priya", "DataSphere", "Technical", "SQL", 87, "Passed"),

        ("Arjun", "CloudCore", "Aptitude", "Logical Reasoning", 80, "Passed"),
        ("Arjun", "CloudCore", "Technical", "Cloud", 72, "Passed"),

        ("Sneha", "CloudCore", "Aptitude", "Logical Reasoning", 86, "Passed"),
        ("Sneha", "CloudCore", "Technical", "Cloud", 91, "Passed"),

        ("Vishal", "DataSphere", "Aptitude", "Quantitative", 55, "Failed"),
        ("Vishal", "DataSphere", "Technical", "Python", 49, "Failed"),

        ("Meghana", "DataSphere", "Aptitude", "Logical Reasoning", 90, "Passed"),
        ("Meghana", "DataSphere", "Technical", "Python", 85, "Passed")
    ]

    cursor.execute("""
        SELECT COUNT(*)
        FROM results
    """)

    if cursor.fetchone()[0] == 0:

        cursor.executemany("""
            INSERT INTO results
            (
                student,
                company,
                round_name,
                topic,
                score,
                result
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, results)

    conn.commit()
    conn.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

create_tables()
add_sample_data()


# ============================================================
# PROFESSIONAL DASHBOARD CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background:
        linear-gradient(
            135deg,
            #050b16 0%,
            #071525 45%,
            #081827 100%
        );
}

/* Main container */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Titles */

h1 {
    color: #38bdf8 !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px;
}

h2 {
    color: #e0f2fe !important;
}

h3 {
    color: #bae6fd !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #050b16,
            #081525
        );
    border-right: 1px solid #1e3a5f;
}

section[data-testid="stSidebar"] h1 {
    color: #38bdf8 !important;
}

/* Metric cards */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #0c1a2d,
            #10233a
        );

    border: 1px solid #1e4970;
    border-radius: 16px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

div[data-testid="stMetricValue"] {
    color: #e0f2fe !important;
}

/* Buttons */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #2385b8;
    background: linear-gradient(
        135deg,
        #0e7490,
        #0369a1
    );
    color: white;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #67e8f9;
    color: white;
}

/* Inputs */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background-color: #0b1728 !important;
    border-color: #294765 !important;
}

input {
    color: #f8fafc !important;
}

textarea {
    color: #f8fafc !important;
}

/* Forms */

div[data-testid="stForm"] {
    background:
        linear-gradient(
            145deg,
            #0a1626,
            #0d1c2e
        );

    padding: 25px;
    border-radius: 18px;
    border: 1px solid #1e3a5f;
}

/* Info boxes */

.ai-box {
    background:
        linear-gradient(
            135deg,
            #0b223b,
            #0d2944
        );

    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1d5b82;
    border-left: 5px solid #38bdf8;
    color: #e2e8f0;
    margin-top: 12px;
}

.alert-box {
    background:
        linear-gradient(
            135deg,
            #30131a,
            #40151d
        );

    padding: 20px;
    border-radius: 15px;
    border: 1px solid #7f1d1d;
    border-left: 5px solid #ef4444;
    color: #fecaca;
    margin-top: 12px;
}

.success-box {
    background:
        linear-gradient(
            135deg,
            #0b281b,
            #10351f
        );

    padding: 20px;
    border-radius: 15px;
    border: 1px solid #166534;
    border-left: 5px solid #22c55e;
    color: #bbf7d0;
    margin-top: 12px;
}

.level-box {
    background:
        linear-gradient(
            135deg,
            #0b1728,
            #10243b
        );

    padding: 20px;
    border-radius: 16px;
    border: 1px solid #1e4970;
    margin-bottom: 20px;
}

/* Dataframe */

div[data-testid="stDataFrame"] {
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    overflow: hidden;
}

/* Tabs */

button[data-baseweb="tab"] {
    color: #94a3b8 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #38bdf8 !important;
}

/* Divider */

hr {
    border-color: #1e3a5f !important;
}

/* File uploader */

section[data-testid="stFileUploaderDropzone"] {
    background-color: #0b1728;
    border: 1px dashed #2874a6;
}

/* Captions */

.stCaption {
    color: #94a3b8 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GRAPH STYLE FUNCTION
# ============================================================

def professional_graph(fig, height=430):

    fig.update_layout(

        height=height,

        paper_bgcolor="#071525",

        plot_bgcolor="#0c1b2e",

        font=dict(
            color="#e2e8f0",
            size=13
        ),

        title=dict(
            font=dict(
                color="#38bdf8",
                size=20
            )
        ),

        xaxis=dict(
            color="#cbd5e1",
            gridcolor="#263b52",
            linecolor="#3b526b",
            zerolinecolor="#3b526b"
        ),

        yaxis=dict(
            color="#cbd5e1",
            gridcolor="#263b52",
            linecolor="#3b526b",
            zerolinecolor="#3b526b"
        ),

        legend=dict(
            font=dict(
                color="#e2e8f0"
            ),
            bgcolor="#0c1b2e"
        ),

        margin=dict(
            l=50,
            r=30,
            t=70,
            b=50
        )
    )

    return fig


# ============================================================
# LOAD TABLE
# ============================================================

def load_table(table_name):

    conn = get_connection()

    df = pd.read_sql(
        f"SELECT * FROM {table_name}",
        conn
    )

    conn.close()

    return df


# ============================================================
# ADD STUDENT
# ============================================================

def add_student(
    roll_no,
    name,
    branch,
    year,
    cgpa
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (
                roll_no,
                name,
                branch,
                year,
                cgpa
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            roll_no,
            name,
            branch,
            year,
            cgpa
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ============================================================
# VALIDATE INTEGER TEXT
# ============================================================

def get_integer(
    value,
    field_name,
    minimum=1,
    maximum=10000
):

    value = value.strip()

    if value == "":
        return None, f"{field_name} is required."

    try:

        number = int(value)

    except ValueError:

        return None, f"{field_name} must be a whole number."

    if number < minimum or number > maximum:

        return None, (
            f"{field_name} must be between "
            f"{minimum} and {maximum}."
        )

    return number, None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# PLACEX AI")

st.sidebar.caption(
    "AI-Powered Placement Intelligence & Optimization"
)

st.sidebar.divider()

# ORIGINAL NAVIGATION IS PRESERVED

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Command Center",
        "Students",
        "Companies",
        "Rooms",
        "Placement Drives",
        "AI Scheduler",
        "Results",
        "Analytics",
        "AI Insights"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    "### PLACEX LEVELS"
)

st.sidebar.caption(
    "LEVEL 1  →  Command Center"
)

st.sidebar.caption(
    "LEVEL 2  →  Students"
)

st.sidebar.caption(
    "LEVEL 3  →  Companies"
)

st.sidebar.caption(
    "LEVEL 4  →  Rooms"
)

st.sidebar.caption(
    "LEVEL 5  →  Placement Drives"
)

st.sidebar.caption(
    "LEVEL 6  →  AI Scheduler"
)

st.sidebar.caption(
    "LEVEL 7  →  Results"
)

st.sidebar.caption(
    "LEVEL 8  →  Analytics"
)

st.sidebar.caption(
    "LEVEL 9  →  AI Insights"
)


# ============================================================
# LEVEL 1 — COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.title(
        "PLACEX AI — Command Center"
    )

    st.caption(
        "LEVEL 1 | Central Placement Monitoring"
    )

    students = load_table("students")
    companies = load_table("companies")
    rooms = load_table("rooms")
    drives = load_table("drives")
    results = load_table("results")

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    total_students = len(students)
    total_companies = len(companies)
    total_rooms = len(rooms)
    total_drives = len(drives)

    passed = 0

    if not results.empty:

        passed = len(
            results[
                results["result"] == "Passed"
            ]
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Students",
        total_students
    )

    col2.metric(
        "Companies",
        total_companies
    )

    col3.metric(
        "Rooms",
        total_rooms
    )

    col4.metric(
        "Placement Drives",
        total_drives
    )

    st.divider()

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.subheader(
        "PLACEX System Status"
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.success("Student Database Online")

    with s2:
        st.success("Company Database Online")

    with s3:
        st.success("Room Database Online")

    with s4:
        st.success("AI Analytics Online")

    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    st.subheader(
        "Coordinator Workflow"
    )

    st.markdown(
        """
        <div class="level-box">

        <b>Coordinator</b>
        &nbsp;&nbsp; ↓ &nbsp;&nbsp;

        <b>Web Application</b>
        &nbsp;&nbsp; ↓ &nbsp;&nbsp;

        <b>Input Forms</b>
        &nbsp;&nbsp; ↓ &nbsp;&nbsp;

        <b>Validation</b>
        &nbsp;&nbsp; ↓ &nbsp;&nbsp;

        <b>SQLite Database</b>

        <br><br>

        The coordinator enters information through
        simple forms. PLACEX validates the information
        before saving it into the SQLite database.

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader(
        "Placement Pipeline"
    )

    registered = total_students

    aptitude_passed = 0
    technical_passed = 0

    if not results.empty:

        aptitude_passed = results[
            (
                results["round_name"]
                == "Aptitude"
            )
            &
            (
                results["result"]
                == "Passed"
            )
        ]["student"].nunique()

        technical_passed = results[
            (
                results["round_name"]
                == "Technical"
            )
            &
            (
                results["result"]
                == "Passed"
            )
        ]["student"].nunique()

    pipeline = pd.DataFrame({

        "Stage": [
            "Registered",
            "Aptitude",
            "Technical",
            "Successful"
        ],

        "Students": [
            registered,
            aptitude_passed,
            technical_passed,
            passed
        ]
    })

    fig = px.funnel(
        pipeline,
        x="Students",
        y="Stage",
        title="Placement Pipeline"
    )

    fig = professional_graph(
        fig,
        450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # QUICK INTELLIGENCE
    # --------------------------------------------------------

    st.subheader(
        "Quick Intelligence"
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        st.markdown(
            f"""
            <div class="ai-box">

            <b>Student Pool</b>

            <br><br>

            {total_students} students are
            currently registered.

            </div>
            """,
            unsafe_allow_html=True
        )

    with q2:

        total_demand = 0

        if not companies.empty:

            total_demand = int(
                companies[
                    "students_required"
                ].sum()
            )

        st.markdown(
            f"""
            <div class="ai-box">

            <b>Recruitment Demand</b>

            <br><br>

            {total_demand} total hiring
            positions are recorded.

            </div>
            """,
            unsafe_allow_html=True
        )

    with q3:

        st.markdown(
            f"""
            <div class="ai-box">

            <b>Successful Results</b>

            <br><br>

            {passed} successful
            result records.

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# LEVEL 2 — STUDENTS
# ============================================================

elif page == "Students":

    st.title(
        "Students"
    )

    st.caption(
        "LEVEL 2 | Student Intelligence & Bulk Registration"
    )

    students = load_table("students")

    total_students = len(students)

    if not students.empty:

        average_cgpa = students["cgpa"].mean()

        high_cgpa = len(
            students[
                students["cgpa"] >= 8.5
            ]
        )

        year_3 = len(
            students[
                students["year"] == 3
            ]
        )

    else:

        average_cgpa = 0
        high_cgpa = 0
        year_3 = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Students",
        total_students
    )

    col2.metric(
        "Average CGPA",
        f"{average_cgpa:.2f}"
    )

    col3.metric(
        "CGPA 8.5+",
        high_cgpa
    )

    col4.metric(
        "Final Year Students",
        year_3
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Student Database",
            "Add Student",
            "Upload Students",
            "Student Analytics"
        ]
    )

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Student Database"
        )

        if students.empty:

            st.info(
                "No students are available."
            )

        else:

            search = st.text_input(
                "Search Student",
                placeholder="Search by name or roll number..."
            )

            filtered_students = students.copy()

            if search:

                search = search.lower()

                filtered_students = filtered_students[
                    filtered_students["name"]
                    .str.lower()
                    .str.contains(
                        search,
                        na=False
                    )
                    |
                    filtered_students["roll_no"]
                    .str.lower()
                    .str.contains(
                        search,
                        na=False
                    )
                ]

            col1, col2 = st.columns(2)

            with col1:

                branches = [
                    "All"
                ] + sorted(
                    students[
                        "branch"
                    ]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_branch = st.selectbox(
                    "Filter by Branch",
                    branches
                )

            with col2:

                selected_year = st.selectbox(
                    "Filter by Year",
                    [
                        "All",
                        1,
                        2,
                        3
                    ]
                )

            if selected_branch != "All":

                filtered_students = filtered_students[
                    filtered_students["branch"]
                    == selected_branch
                ]

            if selected_year != "All":

                filtered_students = filtered_students[
                    filtered_students["year"]
                    == selected_year
                ]

            st.write(
                f"Showing {len(filtered_students)} student(s)"
            )

            st.dataframe(
                filtered_students,
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # ADD STUDENT
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "ADD STUDENT"
        )

        with st.form(
            "student_manual_form"
        ):

            col1, col2 = st.columns(2)

            with col1:

                roll_no = st.text_input(
                    "Roll Number",
                    placeholder="PX009"
                )

                name = st.text_input(
                    "Student Name",
                    placeholder="Enter student name"
                )

                branch = st.selectbox(
                    "Branch",
                    [
                        "BCA",
                        "BCA Data Science",
                        "BSc Computer Science",
                        "BSc Data Science",
                        "BSc AI"
                    ]
                )

            with col2:

                year_text = st.text_input(
                    "Year",
                    value="2",
                    placeholder="1, 2 or 3"
                )

                cgpa_text = st.text_input(
                    "CGPA",
                    value="8.0",
                    placeholder="Example: 8.5"
                )

            submitted = st.form_submit_button(
                "ADD STUDENT",
                type="primary"
            )

            if submitted:

                year_value, year_error = get_integer(
                    year_text,
                    "Year",
                    1,
                    3
                )

                try:

                    cgpa_value = float(
                        cgpa_text.strip()
                    )

                except ValueError:

                    cgpa_value = None

                if not roll_no.strip():

                    st.error(
                        "Roll Number is required."
                    )

                elif not name.strip():

                    st.error(
                        "Student Name is required."
                    )

                elif year_error:

                    st.error(
                        year_error
                    )

                elif cgpa_value is None:

                    st.error(
                        "CGPA must be a valid number."
                    )

                elif cgpa_value < 0 or cgpa_value > 10:

                    st.error(
                        "CGPA must be between 0 and 10."
                    )

                else:

                    added = add_student(
                        roll_no.strip(),
                        name.strip(),
                        branch,
                        year_value,
                        cgpa_value
                    )

                    if added:

                        st.success(
                            "Student added successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "This Roll Number already exists."
                        )

    # --------------------------------------------------------
    # UPLOAD STUDENTS
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "UPLOAD STUDENTS"
        )

        st.write(
            "For small batches, use Add Student. "
            "For large batches such as 500–2000 students, "
            "upload an Excel or CSV file."
        )

        st.markdown(
            """
            <div class="level-box">

            <b>Required columns</b>

            <br><br>

            roll_no &nbsp;&nbsp; name &nbsp;&nbsp; branch
            &nbsp;&nbsp; year &nbsp;&nbsp; cgpa

            <br><br>

            Example:

            <br>

            PX009 | Ravi | BCA Data Science | 2 | 8.4

            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            "Upload Student Excel / CSV",
            type=[
                "csv",
                "xlsx",
                "xls"
            ]
        )

        if uploaded_file is not None:

            try:

                if uploaded_file.name.lower().endswith(
                    ".csv"
                ):

                    uploaded_df = pd.read_csv(
                        uploaded_file
                    )

                else:

                    uploaded_df = pd.read_excel(
                        uploaded_file
                    )

                st.subheader(
                    "Preview"
                )

                st.dataframe(
                    uploaded_df.head(10),
                    use_container_width=True,
                    hide_index=True
                )

                required_columns = [
                    "roll_no",
                    "name",
                    "branch",
                    "year",
                    "cgpa"
                ]

                missing_columns = [
                    col
                    for col in required_columns
                    if col not in uploaded_df.columns
                ]

                if missing_columns:

                    st.error(
                        "Missing columns: "
                        +
                        ", ".join(
                            missing_columns
                        )
                    )

                else:

                    if st.button(
                        "VALIDATE AND IMPORT STUDENTS",
                        type="primary"
                    ):

                        valid_rows = []
                        errors = []

                        existing_students = load_table(
                            "students"
                        )

                        existing_rolls = set(
                            existing_students[
                                "roll_no"
                            ]
                            .astype(str)
                            .tolist()
                        )

                        for index, row in uploaded_df.iterrows():

                            roll = str(
                                row["roll_no"]
                            ).strip()

                            student_name = str(
                                row["name"]
                            ).strip()

                            branch_value = str(
                                row["branch"]
                            ).strip()

                            try:

                                year_value = int(
                                    row["year"]
                                )

                                cgpa_value = float(
                                    row["cgpa"]
                                )

                            except:

                                errors.append(
                                    f"Row {index + 2}: "
                                    "Invalid year or CGPA."
                                )

                                continue

                            if not roll:

                                errors.append(
                                    f"Row {index + 2}: "
                                    "Roll number missing."
                                )

                                continue

                            if not student_name:

                                errors.append(
                                    f"Row {index + 2}: "
                                    "Student name missing."
                                )

                                continue

                            if roll in existing_rolls:

                                errors.append(
                                    f"Row {index + 2}: "
                                    f"{roll} already exists."
                                )

                                continue

                            if year_value not in [
                                1,
                                2,
                                3
                            ]:

                                errors.append(
                                    f"Row {index + 2}: "
                                    "Year must be 1, 2 or 3."
                                )

                                continue

                            if cgpa_value < 0 or cgpa_value > 10:

                                errors.append(
                                    f"Row {index + 2}: "
                                    "CGPA must be 0–10."
                                )

                                continue

                            valid_rows.append(
                                (
                                    roll,
                                    student_name,
                                    branch_value,
                                    year_value,
                                    cgpa_value
                                )
                            )

                            existing_rolls.add(
                                roll
                            )

                        # ------------------------------------
                        # SAVE VALID RECORDS
                        # ------------------------------------

                        if valid_rows:

                            conn = get_connection()

                            cursor = conn.cursor()

                            cursor.executemany(
                                """
                                INSERT INTO students
                                (
                                    roll_no,
                                    name,
                                    branch,
                                    year,
                                    cgpa
                                )
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                valid_rows
                            )

                            conn.commit()
                            conn.close()

                            st.success(
                                f"{len(valid_rows)} student(s) "
                                "imported successfully."
                            )

                        else:

                            st.warning(
                                "No valid student records found."
                            )

                        # ------------------------------------
                        # SHOW ERRORS
                        # ------------------------------------

                        if errors:

                            st.warning(
                                f"{len(errors)} row(s) "
                                "were not imported."
                            )

                            for error in errors[:20]:

                                st.write(
                                    "• " + error
                                )

                        st.rerun()

            except Exception as e:

                st.error(
                    f"Could not read the file: {e}"
                )

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    with tab4:

        st.subheader(
            "Student Analytics"
        )

        if students.empty:

            st.info(
                "Student data is required."
            )

        else:

            fig1 = px.histogram(
                students,
                x="cgpa",
                nbins=8,
                title="CGPA Distribution"
            )

            fig1 = professional_graph(
                fig1
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            branch_count = (
                students
                .groupby("branch")
                .size()
                .reset_index(
                    name="Students"
                )
            )

            fig2 = px.bar(
                branch_count,
                x="branch",
                y="Students",
                text="Students",
                title="Students by Branch"
            )

            fig2 = professional_graph(
                fig2
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            year_count = (
                students
                .groupby("year")
                .size()
                .reset_index(
                    name="Students"
                )
            )

            fig3 = px.pie(
                year_count,
                names="year",
                values="Students",
                title="Students by Year"
            )

            fig3 = professional_graph(
                fig3
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )


# ============================================================
# LEVEL 3 — COMPANIES
# ============================================================

elif page == "Companies":

    st.title(
        "Companies"
    )

    st.caption(
        "LEVEL 3 | Company Intelligence & Recruitment Demand"
    )

    companies = load_table("companies")

    total_companies = len(companies)

    total_demand = 0
    average_demand = 0
    roles = 0

    if not companies.empty:

        total_demand = int(
            companies[
                "students_required"
            ].sum()
        )

        average_demand = companies[
            "students_required"
        ].mean()

        roles = companies[
            "role"
        ].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Companies",
        total_companies
    )

    col2.metric(
        "Hiring Demand",
        total_demand
    )

    col3.metric(
        "Average Demand",
        f"{average_demand:.1f}"
    )

    col4.metric(
        "Job Roles",
        roles
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "Company Database",
            "Add Company",
            "Hiring Analytics"
        ]
    )

    # --------------------------------------------------------
    # COMPANY DATABASE
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Company Database"
        )

        if companies.empty:

            st.info(
                "No companies available."
            )

        else:

            search = st.text_input(
                "Search Company",
                placeholder="Search company or job role..."
            )

            filtered = companies.copy()

            if search:

                filtered = filtered[
                    filtered["name"]
                    .str.lower()
                    .str.contains(
                        search.lower(),
                        na=False
                    )
                    |
                    filtered["role"]
                    .str.lower()
                    .str.contains(
                        search.lower(),
                        na=False
                    )
                ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # ADD COMPANY
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "ADD COMPANY"
        )

        with st.form(
            "company_form"
        ):

            company_name = st.text_input(
                "Company Name",
                placeholder="ABC Technologies"
            )

            job_role = st.text_input(
                "Job Role",
                placeholder="Software Developer"
            )

            eligible_branches = st.multiselect(
                "Eligible Branches",
                [
                    "BCA",
                    "BCA Data Science",
                    "BSc Computer Science",
                    "BSc Data Science",
                    "BSc AI"
                ],
                default=[
                    "BCA",
                    "BCA Data Science"
                ]
            )

            students_required_text = st.text_input(
                "Students Required",
                value="300",
                placeholder="Example: 300"
            )

            drive_date = st.date_input(
                "Drive Date",
                value=date.today()
            )

            submitted = st.form_submit_button(
                "ADD COMPANY",
                type="primary"
            )

            if submitted:

                required_value, error = get_integer(
                    students_required_text,
                    "Students Required",
                    1,
                    100000
                )

                if not company_name.strip():

                    st.error(
                        "Company Name is required."
                    )

                elif not job_role.strip():

                    st.error(
                        "Job Role is required."
                    )

                elif not eligible_branches:

                    st.error(
                        "Select at least one eligible branch."
                    )

                elif error:

                    st.error(
                        error
                    )

                else:

                    conn = get_connection()

                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO companies
                        (
                            name,
                            role,
                            students_required,
                            drive_date
                        )
                        VALUES (?, ?, ?, ?)
                    """, (
                        company_name.strip(),
                        job_role.strip(),
                        required_value,
                        str(drive_date)
                    ))

                    conn.commit()
                    conn.close()

                    st.success(
                        "Company added successfully."
                    )

                    st.info(
                        "Eligible Branches: "
                        +
                        ", ".join(
                            eligible_branches
                        )
                    )

                    st.rerun()

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "Hiring Demand Analytics"
        )

        if companies.empty:

            st.info(
                "Company data required."
            )

        else:

            demand = (
                companies
                .groupby("name")
                [
                    "students_required"
                ]
                .sum()
                .reset_index()
            )

            fig1 = px.bar(
                demand,
                x="name",
                y="students_required",
                text="students_required",
                title="Hiring Demand by Company"
            )

            fig1 = professional_graph(
                fig1
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            role_count = (
                companies
                .groupby("role")
                .size()
                .reset_index(
                    name="Companies"
                )
            )

            fig2 = px.pie(
                role_count,
                names="role",
                values="Companies",
                title="Recruitment Role Distribution"
            )

            fig2 = professional_graph(
                fig2
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )


# ============================================================
# LEVEL 4 — ROOMS
# ============================================================

elif page == "Rooms":

    st.title(
        "Rooms"
    )

    st.caption(
        "LEVEL 4 | Placement Infrastructure Management"
    )

    rooms = load_table("rooms")

    total_rooms = len(rooms)

    total_capacity = 0
    average_capacity = 0
    largest_room = 0

    if not rooms.empty:

        total_capacity = int(
            rooms[
                "capacity"
            ].sum()
        )

        average_capacity = rooms[
            "capacity"
        ].mean()

        largest_room = int(
            rooms[
                "capacity"
            ].max()
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Rooms",
        total_rooms
    )

    col2.metric(
        "Total Capacity",
        total_capacity
    )

    col3.metric(
        "Average Capacity",
        f"{average_capacity:.1f}"
    )

    col4.metric(
        "Largest Room",
        largest_room
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "Room Database",
            "Add Room",
            "Capacity Analytics"
        ]
    )

    # --------------------------------------------------------
    # ROOM DATABASE
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Room Database"
        )

        if rooms.empty:

            st.info(
                "No rooms available."
            )

        else:

            st.dataframe(
                rooms,
                use_container_width=True,
                hide_index=True
            )

            st.subheader(
                "Room Availability"
            )

            for _, room in rooms.iterrows():

                st.markdown(
                    f"""
                    <div class="level-box">

                    <b>{room["room_name"]}</b>

                    <br><br>

                    Type:
                    {room.get("room_type", "Computer Lab")}

                    &nbsp;&nbsp; | &nbsp;&nbsp;

                    Capacity:
                    {int(room["capacity"])}

                    &nbsp;&nbsp; | &nbsp;&nbsp;

                    Available:
                    {room.get("available_from", "09:00")}
                    -
                    {room.get("available_until", "17:00")}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # --------------------------------------------------------
    # ADD ROOM
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "ADD ROOM"
        )

        with st.form(
            "room_form"
        ):

            room_name = st.text_input(
                "Room Name",
                placeholder="Lab 1"
            )

            room_type = st.selectbox(
                "Room Type",
                [
                    "Computer Lab",
                    "Seminar Hall",
                    "Classroom",
                    "Interview Room",
                    "Conference Room"
                ]
            )

            capacity_text = st.text_input(
                "Capacity",
                value="40",
                placeholder="Example: 40"
            )

            col1, col2 = st.columns(2)

            with col1:

                available_from = st.time_input(
                    "Available From",
                    value=time(9, 0)
                )

            with col2:

                available_until = st.time_input(
                    "Available Until",
                    value=time(17, 0)
                )

            submitted = st.form_submit_button(
                "ADD ROOM",
                type="primary"
            )

            if submitted:

                capacity_value, error = get_integer(
                    capacity_text,
                    "Capacity",
                    1,
                    10000
                )

                if not room_name.strip():

                    st.error(
                        "Room Name is required."
                    )

                elif error:

                    st.error(
                        error
                    )

                elif available_until <= available_from:

                    st.error(
                        "Available Until must be later "
                        "than Available From."
                    )

                else:

                    conn = get_connection()

                    cursor = conn.cursor()

                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM rooms
                        WHERE room_name = ?
                    """, (
                        room_name.strip(),
                    ))

                    exists = cursor.fetchone()[0]

                    if exists:

                        conn.close()

                        st.error(
                            "This room already exists."
                        )

                    else:

                        cursor.execute("""
                            INSERT INTO rooms
                            (
                                room_name,
                                capacity,
                                room_type,
                                available_from,
                                available_until
                            )
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            room_name.strip(),
                            capacity_value,
                            room_type,
                            available_from.strftime(
                                "%H:%M"
                            ),
                            available_until.strftime(
                                "%H:%M"
                            )
                        ))

                        conn.commit()
                        conn.close()

                        st.success(
                            "Room added successfully."
                        )

                        st.rerun()

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "Room Capacity Analytics"
        )

        if rooms.empty:

            st.info(
                "Room data required."
            )

        else:

            fig = px.bar(
                rooms,
                x="room_name",
                y="capacity",
                text="capacity",
                title="Room Capacity Comparison"
            )

            fig = professional_graph(
                fig
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# LEVEL 5 — PLACEMENT DRIVES
# ============================================================

elif page == "Placement Drives":

    st.title(
        "Placement Drives"
    )

    st.caption(
        "LEVEL 5 | Placement Drive Management"
    )

    drives = load_table("drives")
    companies = load_table("companies")

    total_drives = len(drives)

    unique_companies = 0
    unique_rounds = 0

    if not drives.empty:

        unique_companies = drives[
            "company"
        ].nunique()

        unique_rounds = drives[
            "round_name"
        ].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Drive Rounds",
        total_drives
    )

    col2.metric(
        "Companies",
        unique_companies
    )

    col3.metric(
        "Round Types",
        unique_rounds
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "Drive Schedule",
            "Create Drive",
            "Drive Analytics"
        ]
    )

    # --------------------------------------------------------
    # SCHEDULE
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Placement Drive Schedule"
        )

        if drives.empty:

            st.info(
                "No placement drives scheduled."
            )

        else:

            st.dataframe(
                drives,
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # CREATE DRIVE
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "CREATE PLACEMENT DRIVE"
        )

        if companies.empty:

            st.warning(
                "Add a company first."
            )

        else:

            with st.form(
                "drive_form"
            ):

                company = st.selectbox(
                    "Company",
                    companies[
                        "name"
                    ].tolist()
                )

                round_name = st.selectbox(
                    "Round",
                    [
                        "Aptitude",
                        "Technical",
                        "Coding",
                        "Technical Interview",
                        "HR Interview"
                    ]
                )

                drive_date = st.date_input(
                    "Drive Date",
                    value=date.today()
                )

                start_time = st.time_input(
                    "Start Time",
                    value=time(9, 0)
                )

                duration_text = st.text_input(
                    "Duration in Minutes",
                    value="60",
                    placeholder="Example: 60"
                )

                submitted = st.form_submit_button(
                    "SCHEDULE DRIVE",
                    type="primary"
                )

                if submitted:

                    duration_value, error = get_integer(
                        duration_text,
                        "Duration",
                        15,
                        1440
                    )

                    if error:

                        st.error(
                            error
                        )

                    else:

                        conn = get_connection()

                        cursor = conn.cursor()

                        cursor.execute("""
                            INSERT INTO drives
                            (
                                company,
                                round_name,
                                drive_date,
                                start_time,
                                duration
                            )
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            company,
                            round_name,
                            str(drive_date),
                            start_time.strftime(
                                "%H:%M"
                            ),
                            duration_value
                        ))

                        conn.commit()
                        conn.close()

                        st.success(
                            "Placement drive scheduled successfully."
                        )

                        st.rerun()

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    with tab3:

        if drives.empty:

            st.info(
                "Drive data required."
            )

        else:

            round_count = (
                drives
                .groupby("round_name")
                .size()
                .reset_index(
                    name="Drives"
                )
            )

            fig = px.bar(
                round_count,
                x="round_name",
                y="Drives",
                text="Drives",
                title="Placement Rounds"
            )

            fig = professional_graph(
                fig
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# LEVEL 6 — AI SCHEDULER
# ============================================================

elif page == "AI Scheduler":

    st.title(
        "AI Scheduler"
    )

    st.caption(
        "LEVEL 6 | Random Student Selection + Room-Time Optimization"
    )

    students = load_table("students")
    rooms = load_table("rooms")

    if students.empty:

        st.warning(
            "Student data is required."
        )

    elif rooms.empty:

        st.warning(
            "Room data is required."
        )

    else:

        st.subheader(
            "AI Scheduler Configuration"
        )

        st.markdown(
            """
            <div class="level-box">

            <b>Default:</b> PLACEX selects
            <b>25 students randomly</b> for the schedule.

            <br><br>

            The coordinator can enter a different number
            manually.

            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_students_text = st.text_input(
                "Students to Schedule",
                value="25",
                placeholder="Example: 25"
            )

        with col2:

            test_duration_text = st.text_input(
                "Round Duration (minutes)",
                value="60",
                placeholder="Example: 60"
            )

        with col3:

            starting_hour_text = st.text_input(
                "Starting Hour",
                value="9",
                placeholder="Example: 9"
            )

        selected_date = st.date_input(
            "Schedule Date",
            value=date.today()
        )

        generate = st.button(
            "GENERATE AI SCHEDULE",
            type="primary"
        )

        if generate:

            number_students, error1 = get_integer(
                selected_students_text,
                "Students to Schedule",
                1,
                len(students)
            )

            duration, error2 = get_integer(
                test_duration_text,
                "Round Duration",
                15,
                1440
            )

            starting_hour, error3 = get_integer(
                starting_hour_text,
                "Starting Hour",
                0,
                23
            )

            if error1:

                st.error(
                    error1
                )

            elif error2:

                st.error(
                    error2
                )

            elif error3:

                st.error(
                    error3
                )

            else:

                # ------------------------------------------------
                # RANDOM STUDENT SELECTION
                # ------------------------------------------------

                selected_students = students.sample(
                    n=number_students,
                    random_state=random.randint(
                        1,
                        1000000
                    )
                ).reset_index(
                    drop=True
                )

                # ------------------------------------------------
                # ROOM SORTING
                # ------------------------------------------------

                sorted_rooms = (
                    rooms
                    .sort_values(
                        "capacity",
                        ascending=False
                    )
                    .reset_index(
                        drop=True
                    )
                )

                schedule_rows = []

                student_index = 0
                batch_number = 1

                current_time = datetime.combine(
                    selected_date,
                    time(
                        starting_hour,
                        0
                    )
                )

                # ------------------------------------------------
                # ALLOCATE STUDENTS
                # ------------------------------------------------

                while (
                    student_index
                    <
                    len(selected_students)
                ):

                    for _, room in sorted_rooms.iterrows():

                        if (
                            student_index
                            >=
                            len(selected_students)
                        ):
                            break

                        capacity = int(
                            room["capacity"]
                        )

                        batch = selected_students.iloc[
                            student_index:
                            student_index + capacity
                        ]

                        for _, student in batch.iterrows():

                            schedule_rows.append({

                                "Student":
                                student["name"],

                                "Roll Number":
                                student["roll_no"],

                                "Branch":
                                student["branch"],

                                "CGPA":
                                student["cgpa"],

                                "Room":
                                room["room_name"],

                                "Room Type":
                                room.get(
                                    "room_type",
                                    "Computer Lab"
                                ),

                                "Capacity":
                                capacity,

                                "Date":
                                str(selected_date),

                                "Start Time":
                                current_time.strftime(
                                    "%H:%M"
                                ),

                                "End Time":
                                (
                                    current_time
                                    +
                                    timedelta(
                                        minutes=duration
                                    )
                                ).strftime(
                                    "%H:%M"
                                ),

                                "Batch":
                                batch_number

                            })

                        student_index += len(batch)

                        batch_number += 1

                    current_time += timedelta(
                        minutes=duration
                    )

                schedule_df = pd.DataFrame(
                    schedule_rows
                )

                st.session_state[
                    "placement_schedule"
                ] = schedule_df

                st.session_state[
                    "selected_scheduler_students"
                ] = selected_students

        # --------------------------------------------------------
        # DISPLAY GENERATED SCHEDULE
        # --------------------------------------------------------

        if (
            "placement_schedule"
            in st.session_state
        ):

            schedule_df = st.session_state[
                "placement_schedule"
            ]

            selected_df = st.session_state[
                "selected_scheduler_students"
            ]

            st.divider()

            st.subheader(
                "Randomly Selected Students"
            )

            st.success(
                f"{len(selected_df)} students were "
                "randomly selected for this schedule."
            )

            st.dataframe(
                selected_df[
                    [
                        "roll_no",
                        "name",
                        "branch",
                        "year",
                        "cgpa"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.subheader(
                "Generated AI Schedule"
            )

            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True
            )

            # ----------------------------------------------------
            # ROOM UTILIZATION
            # ----------------------------------------------------

            room_usage = (
                schedule_df
                .groupby("Room")
                .size()
                .reset_index(
                    name="Students Assigned"
                )
            )

            fig = px.bar(
                room_usage,
                x="Room",
                y="Students Assigned",
                text="Students Assigned",
                title="Room Utilization"
            )

            fig = professional_graph(
                fig
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# LEVEL 7 — RESULTS
# ============================================================

elif page == "Results":

    st.title(
        "Results"
    )

    st.caption(
        "LEVEL 7 | Placement Test Results"
    )

    results = load_table("results")
    students = load_table("students")
    companies = load_table("companies")

    total_attempts = len(results)

    if not results.empty:

        average_score = results[
            "score"
        ].mean()

        passed = len(
            results[
                results["result"]
                == "Passed"
            ]
        )

        pass_rate = (
            passed
            /
            total_attempts
        ) * 100

    else:

        average_score = 0
        passed = 0
        pass_rate = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Attempts",
        total_attempts
    )

    col2.metric(
        "Average Score",
        f"{average_score:.1f}"
    )

    col3.metric(
        "Passed",
        passed
    )

    col4.metric(
        "Pass Rate",
        f"{pass_rate:.1f}%"
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "Result Database",
            "Add Result",
            "Performance View"
        ]
    )

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    with tab1:

        st.subheader(
            "Result Database"
        )

        if results.empty:

            st.info(
                "No results available."
            )

        else:

            result_filter = st.selectbox(
                "Filter Result",
                [
                    "All",
                    "Passed",
                    "Failed"
                ]
            )

            filtered_results = results.copy()

            if result_filter != "All":

                filtered_results = filtered_results[
                    filtered_results["result"]
                    == result_filter
                ]

            st.dataframe(
                filtered_results,
                use_container_width=True,
                hide_index=True
            )

    # --------------------------------------------------------
    # ADD RESULT
    # --------------------------------------------------------

    with tab2:

        st.subheader(
            "ADD RESULT"
        )

        if students.empty or companies.empty:

            st.warning(
                "Students and companies are required."
            )

        else:

            with st.form(
                "result_form"
            ):

                student = st.selectbox(
                    "Student",
                    students[
                        "name"
                    ].tolist()
                )

                company = st.selectbox(
                    "Company",
                    companies[
                        "name"
                    ].tolist()
                )

                round_name = st.selectbox(
                    "Round",
                    [
                        "Aptitude",
                        "Technical",
                        "Coding",
                        "Interview",
                        "HR"
                    ]
                )

                topic = st.text_input(
                    "Topic",
                    placeholder="Python"
                )

                score_text = st.text_input(
                    "Score",
                    value="70",
                    placeholder="0 - 100"
                )

                result = st.selectbox(
                    "Result",
                    [
                        "Passed",
                        "Failed"
                    ]
                )

                submitted = st.form_submit_button(
                    "SAVE RESULT",
                    type="primary"
                )

                if submitted:

                    score_value, error = get_integer(
                        score_text,
                        "Score",
                        0,
                        100
                    )

                    if not topic.strip():

                        st.error(
                            "Topic is required."
                        )

                    elif error:

                        st.error(
                            error
                        )

                    else:

                        conn = get_connection()

                        cursor = conn.cursor()

                        cursor.execute("""
                            INSERT INTO results
                            (
                                student,
                                company,
                                round_name,
                                topic,
                                score,
                                result
                            )
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            student,
                            company,
                            round_name,
                            topic.strip(),
                            score_value,
                            result
                        ))

                        conn.commit()
                        conn.close()

                        st.success(
                            "Result saved successfully."
                        )

                        st.rerun()

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    with tab3:

        if results.empty:

            st.info(
                "Results required."
            )

        else:

            performance = (
                results
                .groupby("student")
                [
                    "score"
                ]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                performance,
                x="student",
                y="score",
                text="score",
                title="Average Student Score"
            )

            fig = professional_graph(
                fig
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# LEVEL 8 — ANALYTICS
# ============================================================

elif page == "Analytics":

    st.title(
        "Analytics"
    )

    st.caption(
        "LEVEL 8 | Placement Performance Analytics"
    )

    results = load_table("results")

    if results.empty:

        st.info(
            "Results data is required."
        )

    else:

        average_score = results[
            "score"
        ].mean()

        pass_rate = (
            len(
                results[
                    results["result"]
                    == "Passed"
                ]
            )
            /
            len(results)
        ) * 100

        highest_score = results[
            "score"
        ].max()

        total_topics = results[
            "topic"
        ].nunique()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Average Score",
            f"{average_score:.1f}"
        )

        col2.metric(
            "Pass Rate",
            f"{pass_rate:.1f}%"
        )

        col3.metric(
            "Highest Score",
            f"{highest_score:.0f}"
        )

        col4.metric(
            "Topics",
            total_topics
        )

        st.divider()

        # ----------------------------------------------------
        # ROUND PERFORMANCE
        # ----------------------------------------------------

        round_scores = (
            results
            .groupby("round_name")
            [
                "score"
            ]
            .mean()
            .reset_index()
        )

        fig1 = px.bar(
            round_scores,
            x="round_name",
            y="score",
            text="score",
            title="Average Score by Round"
        )

        fig1 = professional_graph(
            fig1
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # ----------------------------------------------------
        # TOPIC PERFORMANCE
        # ----------------------------------------------------

        topic_scores = (
            results
            .groupby("topic")
            [
                "score"
            ]
            .mean()
            .reset_index()
            .sort_values(
                "score"
            )
        )

        fig2 = px.bar(
            topic_scores,
            x="score",
            y="topic",
            orientation="h",
            text="score",
            title="Average Topic Performance"
        )

        fig2 = professional_graph(
            fig2
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # ----------------------------------------------------
        # PASS / FAIL
        # ----------------------------------------------------

        result_count = (
            results
            .groupby("result")
            .size()
            .reset_index(
                name="Count"
            )
        )

        fig3 = px.pie(
            result_count,
            names="result",
            values="Count",
            title="Pass vs Fail"
        )

        fig3 = professional_graph(
            fig3
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # ----------------------------------------------------
        # COMPANY PERFORMANCE
        # ----------------------------------------------------

        st.subheader(
            "Company Performance"
        )

        company_scores = (
            results
            .groupby("company")
            [
                "score"
            ]
            .mean()
            .reset_index()
        )

        st.dataframe(
            company_scores,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# LEVEL 9 — AI INSIGHTS
# ============================================================

elif page == "AI Insights":

    st.title(
        "AI Insights"
    )

    st.caption(
        "LEVEL 9 | AI-Powered Placement Intelligence"
    )

    students = load_table("students")
    results = load_table("results")
    companies = load_table("companies")

    if not students.empty:

        average_cgpa = students[
            "cgpa"
        ].mean()

        highest_cgpa = students[
            "cgpa"
        ].max()

        high_students = len(
            students[
                students["cgpa"] >= 8.5
            ]
        )

        st.subheader(
            "Student Intelligence"
        )

        st.markdown(
            f"""
            <div class="ai-box">

            <b>Academic Pattern Detected</b>

            <br><br>

            Average CGPA:
            <b>{average_cgpa:.2f}</b>

            <br><br>

            Highest CGPA:
            <b>{highest_cgpa:.2f}</b>

            <br><br>

            Students with CGPA 8.5+:
            <b>{high_students}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # WEAK TOPIC
    # --------------------------------------------------------

    if not results.empty:

        topic_average = (
            results
            .groupby("topic")
            [
                "score"
            ]
            .mean()
            .sort_values()
        )

        weakest_topic = topic_average.index[0]

        weakest_score = topic_average.iloc[0]

        st.subheader(
            "Learning Bottleneck"
        )

        st.markdown(
            f"""
            <div class="alert-box">

            <b>Lowest Performing Topic</b>

            <br><br>

            {weakest_topic}

            <br><br>

            Average Score:
            <b>{weakest_score:.1f}</b>

            <br><br>

            Additional practice can be planned
            for this topic.

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # ROUND BOTTLENECK
    # --------------------------------------------------------

    if not results.empty:

        round_average = (
            results
            .groupby("round_name")
            [
                "score"
            ]
            .mean()
            .sort_values()
        )

        weakest_round = round_average.index[0]

        weakest_round_score = round_average.iloc[0]

        st.subheader(
            "Placement Bottleneck"
        )

        st.markdown(
            f"""
            <div class="alert-box">

            <b>Lowest Performing Round</b>

            <br><br>

            {weakest_round}

            <br><br>

            Average Score:
            <b>{weakest_round_score:.1f}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # PASS RATE
    # --------------------------------------------------------

    if not results.empty:

        passed_count = len(
            results[
                results["result"]
                == "Passed"
            ]
        )

        total = len(results)

        pass_rate = (
            passed_count
            /
            total
        ) * 100

        if pass_rate >= 70:

            st.markdown(
                f"""
                <div class="success-box">

                <b>Placement Performance Pattern</b>

                <br><br>

                Current pass rate:
                <b>{pass_rate:.1f}%</b>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="alert-box">

                <b>Placement Preparation Alert</b>

                <br><br>

                Current pass rate:
                <b>{pass_rate:.1f}%</b>

                <br><br>

                Additional preparation may be useful.

                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # ANOMALY DETECTION
    # --------------------------------------------------------

    st.subheader(
        "AI Anomaly Detection"
    )

    if len(results) >= 8:

        anomaly_data = results[
            [
                "score"
            ]
        ].copy()

        model = IsolationForest(
            contamination=0.15,
            random_state=42
        )

        anomaly_data[
            "Prediction"
        ] = model.fit_predict(
            anomaly_data[
                [
                    "score"
                ]
            ]
        )

        anomaly_results = results.copy()

        anomaly_results[
            "AI Pattern"
        ] = (
            anomaly_data[
                "Prediction"
            ]
            .map({
                1: "Normal",
                -1: "Unusual"
            })
        )

        unusual = anomaly_results[
            anomaly_results[
                "AI Pattern"
            ]
            == "Unusual"
        ]

        st.info(
            f"AI detected {len(unusual)} "
            "unusual performance record(s)."
        )

        st.dataframe(
            anomaly_results[
                [
                    "student",
                    "company",
                    "round_name",
                    "topic",
                    "score",
                    "result",
                    "AI Pattern"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "At least 8 result records are required "
            "for anomaly detection."
        )

    # --------------------------------------------------------
    # COMPANY DEMAND
    # --------------------------------------------------------

    if not companies.empty:

        highest_demand = companies.loc[
            companies[
                "students_required"
            ].idxmax()
        ]

        st.subheader(
            "Company Demand Intelligence"
        )

        st.markdown(
            f"""
            <div class="ai-box">

            <b>Highest Hiring Demand</b>

            <br><br>

            Company:
            <b>{highest_demand["name"]}</b>

            <br><br>

            Role:
            <b>{highest_demand["role"]}</b>

            <br><br>

            Students Required:
            <b>{int(highest_demand["students_required"])}</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # FINAL AI MESSAGE
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        """
        <div class="ai-box">

        <b>PLACEX AI Decision Support</b>

        <br><br>

        PLACEX connects student information,
        company requirements, rooms, placement drives,
        results and analytics into one placement
        intelligence system.

        <br><br>

        The coordinator enters information through
        simple forms. PLACEX validates the information,
        stores it in SQLite and uses the stored data
        for scheduling, analytics and AI-based insights.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "PLACEX AI"
)

st.sidebar.caption(
    "Placement Intelligence & Optimization"
)

st.sidebar.caption(
    "LEVEL 1 → LEVEL 9"
)