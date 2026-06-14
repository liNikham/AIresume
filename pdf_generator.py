from playwright.sync_api import sync_playwright


def html_to_pdf(
        html_file,
        output_pdf):

    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()

        page.goto(
            f"file:///{html_file}",
            wait_until="networkidle"
        )

        page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True
        )

        browser.close()