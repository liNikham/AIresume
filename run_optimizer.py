from resume_optimizer import (
    optimize_resume
)

with open(
    "resumes/master_resume.html",
    encoding="utf-8"
) as f:

    html = f.read()

jd = open(
    "job_description.txt",
    encoding="utf-8"
).read()

updated_html = optimize_resume(
    html,
    jd
)

with open(
    "generated/updated_resume.html",
    "w",
    encoding="utf-8"
) as f:
    print(
    "Spring Boot found:",
    "Spring Boot" in updated_html
)

    print(
        "Kafka found:",
        "Kafka" in updated_html
    )

    f.write(updated_html)

print(
    "generated/updated_resume.html created"
)
from pdf_generator import (
    html_to_pdf
)

html_to_pdf(
    "generated/updated_resume.html",
    "generated/updated_resume.pdf"
)