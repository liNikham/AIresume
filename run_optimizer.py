from resume_optimizer import (
    optimize_resume
)
from body_extractor import (
    extract_body
)

from body_replacer import (
    replace_body
)
from link_fixer import (
    fix_pdf_links
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
body = extract_body(html)
opt_result = optimize_resume(
    body,
    jd
)
updated_body = opt_result.get("html", "") if isinstance(opt_result, dict) else opt_result
if isinstance(opt_result, dict):
    print(f"Final ATS Score: {opt_result.get('ats_score')}/100 in {opt_result.get('iterations')} passes")

updated_html = replace_body(
    html,
    body,
    updated_body
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

fix_pdf_links(
   "generated/updated_resume.html",
    "generated/updated_resume.pdf"
)