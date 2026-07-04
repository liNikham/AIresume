from dataclasses import dataclass
from lxml import html
import re

@dataclass
class HTMLLink:
    href: str
    page: int
    left: float
    bottom: float
    width: float
    height: float

def extract_number(style: str, key: str) -> float:
    m = re.search(rf"{key}:([\d\.]+)px", style)
    return float(m.group(1)) if m else 0.0

def extract_links(html_file: str):
    with open(html_file, encoding="utf8") as f:
        source = f.read()

    root = html.fromstring(source)

    pages = root.xpath('//div[contains(@class,"pf")]')

    links = []

    for page_index, page in enumerate(pages):
        anchors = page.xpath('.//a[@href]')

        for a in anchors:
            href = a.attrib["href"]

            div = a.xpath('.//div')
            if not div:
                continue

            style = div[0].attrib.get("style", "")

            links.append(
                HTMLLink(
                    href=href,
                    page=page_index,
                    left=extract_number(style, "left"),
                    bottom=extract_number(style, "bottom"),
                    width=extract_number(style, "width"),
                    height=extract_number(style, "height"),
                )
            )

    return links