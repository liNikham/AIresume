import os
import re
import time
import json

import google.generativeai as genai

from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)

# Gemini Free Tier:
# 10 requests/minute
# => 1 request every ~6 seconds
MIN_INTERVAL = 7

LAST_REQUEST_TIME = 0


def wait_for_rate_limit():
    global LAST_REQUEST_TIME

    current = time.time()

    elapsed = current - LAST_REQUEST_TIME

    if elapsed < MIN_INTERVAL:

        sleep_time = MIN_INTERVAL - elapsed

        print(
            f"Rate limit protection: sleeping {sleep_time:.2f}s"
        )

        time.sleep(sleep_time)

    LAST_REQUEST_TIME = time.time()


def clean_response(text):

    text = text.strip()

    text = text.replace(
        "```html",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    return text.strip()


def call_gemini(prompt):

    while True:

        try:

            wait_for_rate_limit()

            response = model.generate_content(
                prompt
            )

            return clean_response(
                response.text
            )

        except ResourceExhausted as e:

            error_text = str(e)

            print(
                "\nQuota exceeded."
            )

            match = re.search(
                r"retry in ([0-9]+)",
                error_text,
                re.IGNORECASE
            )

            wait_seconds = 60

            if match:
                wait_seconds = int(
                    match.group(1)
                ) + 2

            print(
                f"Waiting {wait_seconds} seconds..."
            )

            time.sleep(wait_seconds)


from bs4 import BeautifulSoup

def call_gemini_batch(prompt):
    print("Calling Gemini API in batch mode...", flush=True)
    while True:
        try:
            wait_for_rate_limit()
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            print("Gemini API response received successfully.", flush=True)
            raw_text = response.text.strip()

            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            raw_text = raw_text.strip()

            return json.loads(raw_text)

        except ResourceExhausted as e:

            error_text = str(e)

            print(
                "\nQuota exceeded during batch call.",
                flush=True
            )

            match = re.search(
                r"retry in ([0-9]+)",
                error_text,
                re.IGNORECASE
            )

            wait_seconds = 60

            if match:
                wait_seconds = int(
                    match.group(1)
                ) + 2

            print(
                f"Waiting {wait_seconds} seconds...",
                flush=True
            )

            time.sleep(wait_seconds)

        except Exception as e:
            print(f"Unexpected error in call_gemini_batch: {e}", flush=True)
            raise e


def evaluate_ats_score(resume_html, jd):
    print("Evaluating ATS match score...", flush=True)
    soup = BeautifulSoup(resume_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    prompt = f"""
You are an expert ATS (Applicant Tracking System) reviewer and hiring manager.
Evaluate how well the following RESUME matches the given JOB DESCRIPTION.

JOB DESCRIPTION:
{jd}

RESUME TEXT:
{text}

Provide an objective, realistic ATS score evaluation from 0 to 100 based on:
1. Keyword Overlap & Frequency (0-30 pts)
2. Technical Skills & Tools Match (0-30 pts)
3. Action Verbs & Quantifiable Results (0-20 pts)
4. Overall Relevance to Target Role (0-20 pts)

Return a valid JSON object strictly matching this schema:
{{
  "ats_score": <integer 0-100>,
  "breakdown": {{
    "keyword_match": <integer 0-30>,
    "skills_alignment": <integer 0-30>,
    "quantifiable_results": <integer 0-20>,
    "relevance": <integer 0-20>
  }},
  "missing_keywords": ["<keyword1>", "<keyword2>", ...],
  "feedback": "<short constructive feedback sentence for improving the ATS score>"
}}
Do not include extra text outside the JSON object.
"""
    try:
        res = call_gemini_batch(prompt)
        print(f"ATS Evaluation result: {res}", flush=True)
        return res
    except Exception as e:
        print(f"Error during evaluate_ats_score: {e}", flush=True)
        return {
            "ats_score": 75,
            "breakdown": {"keyword_match": 20, "skills_alignment": 20, "quantifiable_results": 15, "relevance": 20},
            "missing_keywords": [],
            "feedback": "Could not complete evaluation automatically."
        }


def optimize_section(
        section_name,
        fragment,
        jd):

    prompt = f"""
You are an expert ATS resume optimizer.

JOB DESCRIPTION

{jd}

SECTION NAME

{section_name}

CURRENT HTML

{fragment}

RULES

1. Preserve EVERY div class exactly.
2. Preserve EVERY span class exactly.
3. Preserve EXACT div count.
4. Preserve EXACT span count.
5. NEVER change the company name "Infosys Limited".
6. If "Infosys Limited" appears in the HTML, it must remain exactly unchanged.
7. Preserve approximate line lengths.
8. Update content aggressively according to the JD.
9. Reflect company expectations.
10. You may change target role.
11. You may introduce JD keywords.
12. Return ONLY HTML.
13. Do not add markdown.
14. Do not add explanation.
"""

    return call_gemini(prompt)


def optimize_bullet(
        bullet_html,
        jd):
    

    prompt = f"""
You are a resume optimization engine.

JOB DESCRIPTION

{jd}

CURRENT BULLET HTML

{bullet_html}

RULES

1. Keep EXACT div count.
2. Keep EXACT span count.
3. Keep ALL classes.
4. Modify ONLY text.
5. NEVER change the company name "Infosys Limited".
6. If "Infosys Limited" appears in the HTML, it must remain exactly unchanged.
7. Preserve approximate line lengths.
8. Output must fit within the same visual width as the original PDF.
9. Optimize for ATS.
10. Return HTML only.
11. Do not add markdown.
12. Do not add explanations.
"""

    return call_gemini(prompt)


def optimize_resume_batch(
        objective_html,
        skills_html,
        exp_bullets_html,
        proj_bullets_html,
        jd,
        feedback=None,
        missing_keywords=None):

    payload = {
        "objective": objective_html,
        "skills": skills_html,
        "experience_bullets": exp_bullets_html,
        "project_bullets": proj_bullets_html
    }

    extra_instructions = ""
    if feedback or missing_keywords:
        extra_instructions = f"""
PREVIOUS ATS EVALUATION FEEDBACK:
- Specific Feedback: {feedback or 'None'}
- Critical Missing Keywords to Integrate: {', '.join(missing_keywords) if missing_keywords else 'None'}

TARGET GOAL FOR THIS REFINEMENT PASS:
Target an ATS Score strictly above 80. Seamlessly integrate the missing keywords into technical skills, career summary/objective, and experience/project bullets while preserving HTML formatting and realism.
"""

    prompt = f"""
You are an expert ATS resume optimization engine.

JOB DESCRIPTION:
{jd}
{extra_instructions}
INPUT RESUME HTML SECTIONS (JSON):
{json.dumps(payload, indent=2)}

RULES:
1. Preserve EXACT div count and span count for EVERY section and bullet.
2. Keep ALL HTML element classes, inline styles, IDs, and structural tags EXACTLY as provided.
3. NEVER change the company name "Infosys Limited" if present in the HTML.
4. Update text aggressively to align with the target role and incorporate relevant ATS keywords from the JD.
5. Preserve approximate line lengths and visual fit.
6. Return a valid JSON object matching the exact key structure of the input:
   {{
     "objective": "<updated objective html>",
     "skills": "<updated skills html>",
     "experience_bullets": ["<updated exp bullet 1>", "<updated exp bullet 2>", ...],
     "project_bullets": ["<updated proj bullet 1>", "<updated proj bullet 2>", ...]
   }}
7. Do not include extra text or explanations outside the JSON object.
8. CRITICAL: The returned list "experience_bullets" MUST contain EXACTLY {len(exp_bullets_html)} elements. The returned list "project_bullets" MUST contain EXACTLY {len(proj_bullets_html)} elements. Each element in these lists must correspond exactly to the input element at the same index, maintaining its HTML tags and structure.
"""

    return call_gemini_batch(prompt)
