import fitz
import os

from link_extractor import extract_links


def fix_pdf_links(
    html_file: str,
    pdf_file: str
):

    links = extract_links(html_file)

    doc = fitz.open(pdf_file)

    for link in links:

        page = doc[link.page]

        pdf_height = page.rect.height

        x0 = link.left
        x1 = link.left + link.width

        y0 = pdf_height - link.bottom - link.height
        y1 = pdf_height - link.bottom

        rect = fitz.Rect(
            x0,
            y0,
            x1,
            y1
        )

        page.insert_link(
            {
                "kind": fitz.LINK_URI,
                "from": rect,
                "uri": link.href,
            }
        )

        print(f"Inserted {link.href}")

    temp_pdf = pdf_file.replace(".pdf", "_temp.pdf")

    doc.save(
        temp_pdf,
        garbage=4,
        deflate=True,
    )

    doc.close()

    os.replace(
        temp_pdf,
        pdf_file
    )