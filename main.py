from fastapi import FastAPI
from fastapi.responses import FileResponse

from resume_optimizer import optimize_resume
from pdf_generator import html_to_pdf

app = FastAPI()


@app.post("/generate")
def generate_resume(
        jd: str):

    with open(
            "resumes/master_resume.html",
            encoding="utf-8"
    ) as f:

        html = f.read()

    updated_html = optimize_resume(
        html,
        jd
    )

    with open(
            "generated/updated_resume.html",
            "w",
            encoding="utf-8"
    ) as f:

        f.write(updated_html)

    html_to_pdf(
        "generated/updated_resume.html",
        "generated/updated_resume.pdf"
    )

    return FileResponse(
        "generated/updated_resume.pdf",
        filename="resume.pdf"
    )