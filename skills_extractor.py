from bs4 import BeautifulSoup


def extract_skills(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    divs = soup.find_all("div")

    skills = []

    inside = False

    for div in divs:

        text = div.get_text(
            " ",
            strip=True
        )

        if text == "Skills":

            inside = True

            continue

        if inside:

            skills.append(
                str(div)
            )

    return skills