from bs4 import BeautifulSoup

SECTION_NAMES = [
    "Objective",
    "Experience",
    "Projects",
    "Skills",
    "Achievements",
    "Education"
]


def extract_sections(html):

    soup = BeautifulSoup(html, "html.parser")

    divs = soup.find_all("div")

    sections = {}

    current_section = None

    for div in divs:

        text = div.get_text(" ", strip=True)

        if text in SECTION_NAMES:
            current_section = text
            sections[current_section] = []
            continue

        if current_section:
            sections[current_section].append(str(div))

    return sections