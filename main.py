import json
import queue
import threading
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from link_fixer import fix_pdf_links
from resume_optimizer import optimize_resume
from body_extractor import extract_body
from body_replacer import replace_body
from pdf_generator import html_to_pdf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")


@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/download")
def download_pdf():
    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return FileResponse(
        "generated/updated_resume.pdf",
        media_type="application/pdf",
        filename="Nikhil_Mahadik_Resume.pdf",
        headers=headers
    )


@app.post("/generate-stream")
def generate_resume_stream(job_description: str = Form(...)):
    def event_stream():
        q = queue.Queue()

        def progress_callback(step_id, progress, message, extra=None):
            payload = {
                "status": "progress",
                "step": step_id,
                "progress": progress,
                "message": message
            }
            if extra and isinstance(extra, dict):
                payload.update(extra)
            q.put(payload)

        def worker():
            try:
                q.put({
                    "status": "progress",
                    "step": "init",
                    "progress": 5,
                    "message": "Loading master resume and parsing structure..."
                })

                with open(
                    "resumes/master_resume.html",
                    encoding="utf-8"
                ) as f:
                    html = f.read()

                body = extract_body(html)

                opt_result = optimize_resume(
                    body,
                    job_description,
                    progress_callback=progress_callback
                )

                if isinstance(opt_result, dict):
                    updated_body = opt_result.get("html", "")
                    ats_score = opt_result.get("ats_score", 0)
                    initial_score = opt_result.get("initial_score", 0)
                    iterations = opt_result.get("iterations", 1)
                    score_history = opt_result.get("score_history", [])
                    breakdown = opt_result.get("breakdown", {})
                    feedback = opt_result.get("feedback", "")
                    missing_keywords = opt_result.get("missing_keywords", [])
                else:
                    updated_body = opt_result
                    ats_score, initial_score, iterations = 80, 70, 1
                    score_history, breakdown, feedback, missing_keywords = [70, 80], {}, "", []

                q.put({
                    "status": "progress",
                    "step": "assembly",
                    "progress": 90,
                    "message": "Reconstructing HTML document..."
                })

                updated_html = replace_body(
                    html,
                    body,
                    updated_body
                )

                output_html = "generated/updated_resume.html"
                output_pdf = "generated/updated_resume.pdf"

                with open(
                    output_html,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(updated_html)

                q.put({
                    "status": "progress",
                    "step": "pdf",
                    "progress": 95,
                    "message": "Rendering PDF & calibrating hyperlinks..."
                })

                html_to_pdf(
                    output_html,
                    output_pdf
                )

                fix_pdf_links(
                    output_html,
                    output_pdf
                )

                q.put({
                    "status": "complete",
                    "progress": 100,
                    "message": f"Resume optimization complete! Final ATS Score: {ats_score}/100",
                    "download_url": "/download",
                    "preview_url": "/generated/updated_resume.pdf",
                    "ats_score": ats_score,
                    "initial_score": initial_score,
                    "iterations": iterations,
                    "score_history": score_history,
                    "breakdown": breakdown,
                    "feedback": feedback,
                    "missing_keywords": missing_keywords
                })

            except Exception as e:
                print(f"Error during stream generation: {e}")
                q.put({
                    "status": "error",
                    "message": str(e)
                })
            finally:
                q.put(None)

        thread = threading.Thread(target=worker)
        thread.start()

        while True:
            item = q.get()
            if item is None:
                break
            yield f"data: {json.dumps(item)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")



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

        opt_result = optimize_resume(
            body,
            job_description
        )
        updated_body = opt_result.get("html", "") if isinstance(opt_result, dict) else opt_result

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

        headers = {
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        return FileResponse(
            output_pdf,
            media_type="application/pdf",
            filename="Nikhil_Mahadik_Resume.pdf",
            headers=headers
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