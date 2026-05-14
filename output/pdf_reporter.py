import json
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

from config.settings import OUTPUT_DIR


class PDFReporter:

    def __init__(
        self,
        domain,
        results
    ):

        self.domain = domain
        self.results = results

    def generate(self):

        filename = (
            OUTPUT_DIR /
            f"{self.domain}.pdf"
        )

        document = (
            SimpleDocTemplate(
                str(filename),
                pagesize=letter
            )
        )

        styles = (
            getSampleStyleSheet()
        )

        elements = []

        title = Paragraph(
            (
                f"<b>AI-Powered "
                f"Recon Report</b>"
            ),
            styles["Title"]
        )

        elements.append(title)

        elements.append(
            Spacer(1, 20)
        )

        target = Paragraph(
            (
                f"<b>Target:</b> "
                f"{self.domain}"
            ),
            styles["BodyText"]
        )

        elements.append(target)

        generated = Paragraph(
            (
                f"<b>Generated:</b> "
                f"{datetime.utcnow()}"
            ),
            styles["BodyText"]
        )

        elements.append(generated)

        elements.append(
            Spacer(1, 20)
        )

        for key, value in (
            self.results.items()
        ):

            heading = Paragraph(
                f"<b>{key}</b>",
                styles["Heading2"]
            )

            elements.append(
                heading
            )

            formatted = json.dumps(
                value,
                indent=4,
                default=str
            )

            content = Preformatted(
                formatted,
                styles["Code"]
            )

            elements.append(
                content
            )

            elements.append(
                Spacer(1, 15)
            )

        document.build(
            elements
        )

        return filename