from bs4 import BeautifulSoup


def extract_objective(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    divs = soup.find_all("div")

    objective = []

    inside = False

    for div in divs:

        text = div.get_text(
            " ",
            strip=True
        )

        if text == "Objective":

            inside = True

            continue

        if text == "Experience":

            break

        if inside:

            objective.append(
                str(div)
            )

    return objective