from weasyprint import HTML


def html_to_pdf(
        html_file,
        output_pdf):

    HTML(
        filename=html_file
    ).write_pdf(
        output_pdf
    )