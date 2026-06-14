import os
import requests


def html_to_pdf(html_file: str, output_pdf: str) -> None:
    """Converts a local pdf2htmlEX HTML file to PDF using PDFShift's official v3 structure."""
    # 1. Retrieve your API key from environment variables
    api_key = os.environ.get("PDFSHIFT_API_KEY")

    if not api_key:
        raise ValueError(
            "Missing PDFSHIFT_API_KEY environment variable. Please set it."
        )

    # 2. Read your local heavy resume HTML file contents as a text string
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"Sending heavy pdf2htmlEX file ({html_file}) to PDFShift API...")

    # 3. Match the official documentation structure exactly
    # We replace the URL string with your raw html_content string
    response = requests.post(
        "https://api.pdfshift.io/v3/convert/pdf",
        headers={"X-API-Key": api_key},
        json={
            "source": html_content,  # Passing the file text directly here
            "landscape": False,
            "use_print": False,
        },
    )

    # 4. Built-in error handling from the documentation snippet
    response.raise_for_status()

    # 5. Save the generated binary content to your destination path
    with open(output_pdf, "wb") as f:
        f.write(response.content)

    print(f"Successfully generated pixel-perfect PDF: {output_pdf}")