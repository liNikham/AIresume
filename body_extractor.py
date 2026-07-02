def extract_body(html):

    start_token = 'class="t m0 x1 h4 y4'
    end_token = 'class="t m0 x5 h4 y2c'

    start = html.find(start_token)

    if start == -1:
        raise Exception("Objective section not found.")

    # Go back to the beginning of the div
    start = html.rfind("<div", 0, start)

    end = html.find(end_token)

    if end == -1:
        raise Exception("Achievements section not found.")

    # Go back to beginning of Achievements div
    end = html.rfind("<div", 0, end)

    body = html[start:end]

    return body