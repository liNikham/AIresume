from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from link_fixer import fix_pdf_links
from resume_optimizer import optimize_resume
from body_extractor import extract_body
from body_replacer import replace_body
from pdf_generator import html_to_pdf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():

    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/generate")
def generate_resume(job_description: str = Form(...)):

    try:

        print("=" * 60)
        print("STEP 1 - Request Received")
        print("=" * 60)

        with open(
            "resumes/master_resume.html",
            encoding="utf-8"
        ) as f:
            html = f.read()

        print("✓ Master resume loaded")

        body = extract_body(html)

        print("✓ Body extracted")

        updated_body = optimize_resume(
            body,
            job_description
        )

        print("✓ Resume optimized")

        updated_html = replace_body(
            html,
            body,
            updated_body
        )

        print("✓ HTML reconstructed")

        output_html = "generated/updated_resume.html"
        output_pdf = "generated/updated_resume.pdf"

        with open(
            output_html,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(updated_html)

        print("✓ HTML saved")

        html_to_pdf(
            output_html,
            output_pdf
        )
        fix_pdf_links(
            "generated/updated_resume.html",
                "generated/updated_resume.pdf"
            )

        print("✓ PDF generated")

        return FileResponse(
            output_pdf,
            media_type="application/pdf",
            filename="Nikhil_Mahadik_Resume.pdf",
        )

    except Exception as e:

        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(e)

        return {
            "success": False,
            "error": str(e)
        }