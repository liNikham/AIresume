from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

from resume_optimizer import optimize_resume
from pdf_generator import html_to_pdf

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>

    <head>
        <title>Resume AI</title>
    </head>

    <body>

        <h2>AI Resume Optimizer</h2>

        <form action="/generate" method="post">

            <textarea
                name="job_description"
                rows="20"
                cols="100"
                placeholder="Paste Job Description Here">
            </textarea>

            <br><br>

            <button type="submit">
                Generate Resume
            </button>

        </form>

    </body>

    </html>
    """


@app.post("/generate")
def generate_resume(
        job_description: str = Form(...)
):

    with open(
            "resumes/master_resume.html",
            encoding="utf-8"
    ) as f:

        html = f.read()

    updated_html = optimize_resume(
        html,
        job_description
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
        media_type="application/pdf",
        filename="resume.pdf"
    )