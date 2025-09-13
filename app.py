from flask import Flask, render_template
import csv
import os
from collections import defaultdict

app = Flask(__name__)


def read_csv_dicts(path):
    """Return a list[dict] from a CSV file (UTF-8, with headers)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_csv_singleton(path):
    rows = read_csv_dicts(path)
    return rows[0] if rows else {}


@app.route("/")
def index():
    data_dir = os.path.join(app.root_path, "data")

    contact = read_csv_singleton(os.path.join(data_dir, "contact.csv"))
    education = read_csv_dicts(os.path.join(data_dir, "education.csv"))
    experience = read_csv_dicts(os.path.join(data_dir, "experience.csv"))
    exp_bullets_rows = read_csv_dicts(os.path.join(data_dir, "experience_bullets.csv"))
    projects = read_csv_dicts(os.path.join(data_dir, "projects.csv"))
    proj_bullets_rows = read_csv_dicts(os.path.join(data_dir, "project_bullets.csv"))
    skills = read_csv_dicts(os.path.join(data_dir, "skills.csv"))

    # Attach bullets to experience
    exp_bullets = defaultdict(list)
    for row in exp_bullets_rows:
        exp_bullets[row["experience_id"]].append(row["bullet"])
    for e in experience:
        e["bullets"] = exp_bullets.get(e["id"], [])

    # Attach bullets to projects
    proj_bullets = defaultdict(list)
    for row in proj_bullets_rows:
        proj_bullets[row["project_id"]].append(row["bullet"])
    for p in projects:
        p["bullets"] = proj_bullets.get(p["id"], [])

    return render_template(
        "index.html",
        contact=contact,
        education=education,
        experience=experience,
        projects=projects,
        skills=skills,
    )


if __name__ == "__main__":
    # For local dev: http://127.0.0.1:5000/
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
