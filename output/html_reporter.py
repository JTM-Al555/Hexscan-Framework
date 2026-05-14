import json
from datetime import datetime

from config.settings import OUTPUT_DIR


class HTMLReporter:

    def __init__(
        self,
        domain,
        results
    ):

        self.domain = domain
        self.results = results

    def generate(self):

        html = f"""
        <html>

        <head>

            <title>
                AI Recon Report
            </title>

            <style>

                body {{
                    background-color: #0f172a;
                    color: white;
                    font-family: Arial;
                    padding: 40px;
                }}

                h1 {{
                    color: #38bdf8;
                }}

                h2 {{
                    color: #22c55e;
                }}

                pre {{
                    background: #1e293b;
                    padding: 15px;
                    border-radius: 10px;
                    overflow-x: auto;
                }}

                img {{
                    margin-top: 20px;
                    border-radius: 10px;
                    width: 100%;
                    max-width: 1200px;
                }}

            </style>

        </head>

        <body>

            <h1>
                AI-Powered Recon Report
            </h1>

            <p>
                Target:
                {self.domain}
            </p>

            <p>
                Generated:
                {datetime.utcnow()}
            </p>
        """

        for key, value in (
            self.results.items()
        ):

            html += f"""
            <h2>{key}</h2>

            <pre>
{json.dumps(value, indent=4)}
            </pre>
            """

        screenshots = self.results.get(
            "screenshots",
            []
        )

        if screenshots:

            html += """
            <h2>
                Screenshots
            </h2>
            """

            for screenshot in screenshots:

                html += f"""
                <img src="../{screenshot}">
                """

        html += """
        </body>
        </html>
        """

        filename = (
            OUTPUT_DIR /
            f"{self.domain}.html"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(html)

        return filename