def replace_body(
        html,
        original_body,
        updated_body):

    if original_body not in html:
        raise Exception("Original body not found.")

    return html.replace(
        original_body,
        updated_body,
        1
    )