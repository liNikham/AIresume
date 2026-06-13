from bullet_extractor import (
    extract_experience_bullets,
    extract_project_bullets
)

with open(
    "resumes/master_resume.html",
    encoding="utf-8"
) as f:

    html = f.read()

experience = extract_experience_bullets(
    html
)

projects = extract_project_bullets(
    html
)

print(
    f"Experience Bullets: {len(experience)}"
)

print(
    f"Project Bullets: {len(projects)}"
)