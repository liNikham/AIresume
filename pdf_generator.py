import os
import requests


def html_to_pdf(html_file: str, output_pdf: str) -> None:
    """
    Converts a local HTML file to PDF using Browserless PDF API.
    """

    token = os.environ.get("BROWSERLESS_TOKEN")

    if not token:
        raise ValueError(
            "Missing BROWSERLESS_TOKEN environment variable."
        )

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"Sending {html_file} to Browserless...")

    response = requests.post(
        f"https://production-sfo.browserless.io/pdf?token={token}",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "html": html_content,
            "options": {
                "format": "A4",
                "printBackground": True,
                "preferCSSPageSize": True,
                "margin": {
                    "top": "0mm",
                    "right": "0mm",
                    "bottom": "0mm",
                    "left": "0mm"
                }
            }
        },
        timeout=120,
    )

    response.raise_for_status()

    with open(output_pdf, "wb") as f:
        f.write(response.content)

    print(f"Successfully generated PDF: {output_pdf}")