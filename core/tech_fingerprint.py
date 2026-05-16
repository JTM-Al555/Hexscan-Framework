import re

from bs4 import BeautifulSoup


class TechnologyFingerprinter:

    def __init__(self, headers, html=""):

        self.headers = headers

        self.html = html

        self.detected = set()

    def detect_headers(self):

        server = (
            self.headers.get(
                "server",
                ""
            ).lower()
        )

        powered = (
            self.headers.get(
                "x-powered-by",
                ""
            ).lower()
        )

        if "cloudflare" in server:
            self.detected.add(
                "Cloudflare"
            )

        if "nginx" in server:
            self.detected.add(
                "Nginx"
            )

        if "apache" in server:
            self.detected.add(
                "Apache"
            )

        if "express" in powered:
            self.detected.add(
                "Express"
            )

        if "php" in powered:
            self.detected.add(
                "PHP"
            )

    def detect_html_patterns(self):

        html_lower = self.html.lower()

        patterns = {

            "React": [
                "react",
                "_reactRootContainer"
            ],

            "Next.js": [
                "_next",
                "__NEXT_DATA__"
            ],

            "Vue": [
                "vue"
            ],

            "Angular": [
                "ng-app",
                "angular"
            ],

            "Tailwind CSS": [
                "tailwind"
            ],

            "Bootstrap": [
                "bootstrap"
            ],

            "jQuery": [
                "jquery"
            ],

            "GraphQL": [
                "graphql"
            ],

            "WordPress": [
                "wp-content",
                "wp-json"
            ],

            "Vercel": [
                "vercel"
            ],

            "Netlify": [
                "netlify"
            ]
        }

        for tech, signatures in (
            patterns.items()
        ):

            for signature in signatures:

                if signature.lower() in html_lower:

                    self.detected.add(
                        tech
                    )

    def detect_meta_tags(self):

        soup = BeautifulSoup(
            self.html,
            "html.parser"
        )

        generator = soup.find(
            "meta",
            attrs={
                "name": "generator"
            }
        )

        if generator:

            content = generator.get(
                "content",
                ""
            )

            if content:

                self.detected.add(
                    content
                )

    def detect(self):

        self.detect_headers()

        self.detect_html_patterns()

        self.detect_meta_tags()

        return list(
            self.detected
        )