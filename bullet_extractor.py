from bs4 import BeautifulSoup


def extract_experience_bullets(html):

    soup = BeautifulSoup(html, "html.parser")

    divs = soup.find_all("div")

    inside_experience = False

    bullets = []
    current_bullet = []

    for div in divs:

        text = div.get_text(" ", strip=True)

        if text == "Experience":
            inside_experience = True
            continue

        if text == "Projects":
            break

        if not inside_experience:
            continue

        if text.startswith("●"):

            if current_bullet:
                bullets.append(current_bullet)

            current_bullet = []

        current_bullet.append(str(div))

    if current_bullet:
        bullets.append(current_bullet)

    return bullets

def extract_project_bullets(html):

    soup = BeautifulSoup(html, "html.parser")

    divs = soup.find_all("div")

    inside_projects = False

    bullets = []
    current_bullet = []

    for div in divs:

        text = div.get_text(" ", strip=True)

        if text == "Projects":
            inside_projects = True
            continue

        if text == "Skills":
            break

        if not inside_projects:
            continue

        if text.startswith("●"):

            if current_bullet:
                bullets.append(current_bullet)

            current_bullet = []

        current_bullet.append(str(div))

    if current_bullet:
        bullets.append(current_bullet)

    return bullets