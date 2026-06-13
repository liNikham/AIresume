from bs4 import BeautifulSoup


def get_y_class(class_list):

    for cls in class_list:

        if cls.startswith("y"):
            return cls

    return None


def replace_bullet_by_classes(
        html,
        old_bullet_html,
        new_bullet_html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    old_soup = BeautifulSoup(
        old_bullet_html,
        "html.parser"
    )

    new_soup = BeautifulSoup(
        new_bullet_html,
        "html.parser"
    )

    old_divs = old_soup.find_all("div")
    new_divs = new_soup.find_all("div")

    if len(old_divs) != len(new_divs):
        return html

    for old_div, new_div in zip(
            old_divs,
            new_divs):

        y_class = get_y_class(
            old_div.get("class", [])
        )

        if not y_class:
            continue

        target = soup.find(
            "div",
            class_=lambda c:
                c and y_class in c
        )

        if target:

            target.replace_with(
                new_div
            )

    return soup.decode(formatter=None)