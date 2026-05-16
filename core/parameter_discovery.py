import re

from utils.logger import logger


class ParameterDiscovery:

    def __init__(self, results):

        self.results = results

        self.parameters = set()

    def extract_from_links(self):

        crawler = self.results.get(
            "web_crawler",
            {}
        )

        links = crawler.get(
            "links",
            []
        )

        pattern = r"\?([a-zA-Z0-9_\-]+)="

        for link in links:

            matches = re.findall(
                pattern,
                link
            )

            for match in matches:

                self.parameters.add(
                    match
                )

    def extract_from_js(self):

        js = self.results.get(
            "javascript_analysis",
            {}
        )

        pattern = r"[?&]([a-zA-Z0-9_\-]+)="

        for _, data in js.items():

            endpoints = data.get(
                "endpoints",
                []
            )

            for endpoint in endpoints:

                matches = re.findall(
                    pattern,
                    endpoint
                )

                for match in matches:

                    self.parameters.add(
                        match
                    )

    def add_common_params(self):

        common = [

            "id",
            "page",
            "url",
            "next",
            "redirect",
            "callback",
            "token",
            "email",
            "user",
            "query",
            "search",
            "lang",
            "file",
            "download",
            "redirect_uri"
        ]

        for param in common:

            self.parameters.add(
                param
            )

    def run(self):

        logger.info(
            "Starting parameter discovery"
        )

        self.extract_from_links()

        self.extract_from_js()

        self.add_common_params()

        final = sorted(
            list(self.parameters)
        )

        logger.info(
            (
                f"Discovered "
                f"{len(final)} "
                f"parameters"
            )
        )

        return {

            "total": len(final),

            "parameters": final
        }