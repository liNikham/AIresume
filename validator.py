from bs4 import BeautifulSoup


def validate_fragment(
        old_html,
        new_html):

    old = BeautifulSoup(
        old_html,
        "html.parser"
    )

    new = BeautifulSoup(
        new_html,
        "html.parser"
    )

    if len(old.find_all("div")) != \
            len(new.find_all("div")):

        return False, "Div mismatch"

    # if len(old.find_all("span")) != \
    #         len(new.find_all("span")):

    #     return False, "Span mismatch"

    old_classes = [
        set(d.get("class") or [])
        for d in old.find_all("div")
    ]

    new_classes = [
        set(d.get("class") or [])
        for d in new.find_all("div")
    ]

    if old_classes != new_classes:

        return False, "Class mismatch"

    return True, "OK"