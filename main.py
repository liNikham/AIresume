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
                placeholder="Paste Job Description Here"></textarea>

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

    try:

        print("=" * 50)
        print("STEP 1 - Request received")
        print("=" * 50)

        print(
            f"JD Length: {len(job_description)}"
        )

        with open(
                "resumes/master_resume.html",
                encoding="utf-8"
        ) as f:

            html = f.read()

        print("STEP 2 - Resume loaded")

        updated_html = optimize_resume(
            html,
            job_description
        )

        print("STEP 3 - Optimization finished")

        with open(
                "generated/updated_resume.html",
                "w",
                encoding="utf-8"
        ) as f:

            f.write(updated_html)

        print("STEP 4 - HTML saved")

        html_to_pdf(
            "generated/updated_resume.html",
            "generated/updated_resume.pdf"
        )

        print("STEP 5 - PDF generated")

        return FileResponse(
            "generated/updated_resume.pdf",
            media_type="application/pdf",
            filename="resume.pdf"
        )

    except Exception as e:

        print("=" * 50)
        print("ERROR OCCURRED")
        print("=" * 50)

        print(str(e))

        return {
            "success": False,
            "error": str(e)
        }