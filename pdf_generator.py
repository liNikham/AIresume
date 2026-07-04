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

    # ------------------------------------------------------------------
    # Fix: pdf2htmlEX uses absolutely-positioned <div class="d"> inside
    # <a class="l"> tags as transparent link overlays. Two problems
    # break clickable links in the PDF:
    #
    # 1. The print stylesheet hides ALL .d elements (@media print { .d{display:none} })
    # 2. Even when visible, the <a> tag has 0×0 bounding-box because its
    #    only child is absolutely-positioned (out-of-flow), so Chrome
    #    creates a zero-area PDF link annotation.
    #
    # Solution: inject JS that copies each overlay div's inline
    # dimensions up to its parent <a>, and CSS that overrides the
    # print-mode display:none.  Browserless waits for a marker
    # attribute before snapshotting the PDF.
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # CSS: override the pdf2htmlEX print stylesheet which hides all .d
    # elements (the transparent link overlay divs) in print mode.
    # Placed last in <head> so it wins by cascade order.
    LINK_FIX_CSS = (
        "<style>"
        "@media print { .d { display: block !important; } }"
        "</style>"
    )
    html_content = html_content.replace(
        "</head>", f"{LINK_FIX_CSS}\n</head>"
    )

    # ------------------------------------------------------------------
    # JS: pdf2htmlEX wraps link hit-areas as absolutely-positioned
    # <div class="d"> inside <a class="l"> tags.  The <a> itself has
    # zero bounding-box (abs-pos children are out-of-flow), so Chrome
    # creates zero-area PDF link annotations.
    #
    # This script copies each overlay div's inline position/dimensions
    # up to its parent <a> tag BEFORE the page load event fires, so the
    # <a> elements have correct bounding boxes when the PDF is snapped.
    # Placed right before </body> so the entire DOM is available and
    # the fix executes synchronously during page load.
    # ------------------------------------------------------------------
    LINK_FIX_JS = """
<script>
(function() {
    var links = document.querySelectorAll('a.l');
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        var div = link.querySelector('.d');
        if (div) {
            var style = div.getAttribute('style') || '';
            link.setAttribute('style', style);
            div.removeAttribute('style');
        }
    }
})();
</script>
"""
    html_content = html_content.replace(
        "</body>", f"{LINK_FIX_JS}\n</body>"
    )

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