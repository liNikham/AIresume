import os
import re
import time

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
5. Preserve approximate line lengths.
6. Update content aggressively according to the JD.
7. Reflect company expectations.
8. You may change target role.
9. You may introduce JD keywords.
10. Return ONLY HTML.
11. Do not add markdown.
12. Do not add explanation.
"""

    return call_gemini(prompt)


def optimize_bullet(
        bullet_html,
        jd):
    print(jd)

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
5. Keep same approximate length.
6. Optimize for ATS.
7. Return HTML only.
8. Do not add markdown.
9. Do not add explanations.
"""

    return call_gemini(prompt)