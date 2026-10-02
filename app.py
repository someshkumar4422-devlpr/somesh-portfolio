import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


BASE_DIR = Path(__file__).resolve().parent
RESUME_PATH = BASE_DIR / "resume" / "resume.pdf"
DATABASE_PATH = BASE_DIR / "instance" / "contact_messages.db"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or os.urandom(32),
    DATABASE=str(DATABASE_PATH),
    MAX_CONTENT_LENGTH=1024 * 1024,
)

PROJECTS = [
    {
        "number": "01",
        "name": "Transparent Hostel Maintenance Portal",
        "description": "A clear request-tracking portal that helps students report hostel issues and follow each update through resolution.",
        "stack": ["Python", "Flask", "SQLite", "HTML/CSS"],
        "github": "https://github.com/your-username/hostel-maintenance-portal",
        "demo": "https://example.com/hostel-maintenance-portal",
    },
    {
        "number": "02",
        "name": "Student Attendance Management System",
        "description": "A practical system for organizing class attendance, reviewing records, and making student data easier to manage.",
        "stack": ["Python", "SQL", "HTML/CSS"],
        "github": "https://github.com/your-username/attendance-management-system",
        "demo": "https://example.com/attendance-management-system",
    },
    {
        "number": "03",
        "name": "Personal Portfolio Website",
        "description": "A responsive portfolio built to share my background, selected projects, and progress as a computer science student.",
        "stack": ["Python", "Flask", "JavaScript", "CSS"],
        "github": "https://github.com/your-username/personal-portfolio",
        "demo": "https://example.com/personal-portfolio",
    },
]

SKILLS = [
    ("C", "Programming"),
    ("Python", "Programming"),
    ("Java", "Programming"),
    ("Data Structures", "Core CS"),
    ("SQL", "Data"),
    ("HTML", "Web"),
    ("CSS", "Web"),
    ("Git / GitHub", "Tools"),
    ("DBMS", "Core CS"),
    ("Computer Networks", "Core CS"),
]


@contextmanager
def get_db_connection():
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_database():
    with get_db_connection() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )


def create_starter_resume():
    if RESUME_PATH.exists():
        return

    RESUME_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(RESUME_PATH),
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="Somesh Kumar - Resume",
        author="Somesh Kumar",
    )
    stylesheet = getSampleStyleSheet()
    stylesheet.add(ParagraphStyle(
        name="ResumeName", parent=stylesheet["Title"], fontName="Helvetica-Bold",
        fontSize=25, leading=30, textColor=colors.HexColor("#18211e"),
        alignment=TA_LEFT, spaceAfter=5,
    ))
    stylesheet.add(ParagraphStyle(
        name="ResumeHeading", parent=stylesheet["Heading2"], fontName="Helvetica-Bold",
        fontSize=11, leading=15, textColor=colors.HexColor("#b65238"),
        spaceBefore=13, spaceAfter=4,
    ))
    stylesheet.add(ParagraphStyle(
        name="ResumeBody", parent=stylesheet["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=colors.HexColor("#303a36"),
        spaceAfter=4,
    ))

    content = [
        Paragraph("Somesh Kumar", stylesheet["ResumeName"]),
        Paragraph("B.Tech Computer Science and Engineering Student", stylesheet["ResumeBody"]),
        Paragraph("somesh.kumar@example.com | github.com/your-username | linkedin.com/in/your-profile", stylesheet["ResumeBody"]),
        Paragraph("PROFILE", stylesheet["ResumeHeading"]),
        Paragraph(
            "Second-year B.Tech CSE student at SRKR Engineering College interested in software development, problem solving, networking, and cybersecurity. Building a strong foundation through coursework and practical projects.",
            stylesheet["ResumeBody"],
        ),
        Paragraph("EDUCATION", stylesheet["ResumeHeading"]),
        Paragraph("B.Tech - Computer Science and Engineering<br/>SRKR Engineering College | Currently in 2nd year", stylesheet["ResumeBody"]),
        Paragraph("TECHNICAL SKILLS", stylesheet["ResumeHeading"]),
        Paragraph("C, Python, Java, Data Structures, SQL, HTML, CSS, Git/GitHub, DBMS, Computer Networks", stylesheet["ResumeBody"]),
        Paragraph("SELECTED PROJECTS", stylesheet["ResumeHeading"]),
        Paragraph("<b>Transparent Hostel Maintenance Portal</b> - A request-tracking portal designed to make hostel maintenance updates easier to follow.", stylesheet["ResumeBody"]),
        Paragraph("<b>Student Attendance Management System</b> - An application concept for organizing attendance records and student data.", stylesheet["ResumeBody"]),
        Paragraph("<b>Personal Portfolio Website</b> - A responsive Flask portfolio for presenting my skills, education, and projects.", stylesheet["ResumeBody"]),
        Spacer(1, 8),
        Paragraph("Starter resume: replace the example contact links with your own details before sharing.", stylesheet["ResumeBody"]),
    ]
    document.build(content)


@app.get("/")
def home():
    return render_template("index.html", projects=PROJECTS, skills=SKILLS, year=datetime.now().year)


@app.get("/resume")
def download_resume():
    create_starter_resume()
    return send_file(RESUME_PATH, as_attachment=True, download_name="Somesh_Kumar_Resume.pdf")


@app.post("/contact")
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if request.form.get("company", "").strip():
        return redirect(url_for("home", _anchor="contact"))

    if not name or len(name) > 100:
        flash("Please enter your name (up to 100 characters).", "error")
    elif not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) or len(email) > 254:
        flash("Please enter a valid email address.", "error")
    elif not message or len(message) > 5000:
        flash("Please enter a message (up to 5,000 characters).", "error")
    else:
        with get_db_connection() as connection:
            connection.execute(
                "INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)",
                (name, email, message),
            )
        flash("Thanks for reaching out. Your message has been received.", "success")

    return redirect(url_for("home", _anchor="contact"))


init_database()
create_starter_resume()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)