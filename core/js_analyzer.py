import re
import httpx

from bs4 import BeautifulSoup

from utils.logger import logger


class JavaScriptAnalyzer:

    def __init__(self, domain):

        self.domain = domain

        self.base_url = (
            f"https://{domain}"
        )

        self.headers = {

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            )
        }

    async def fetch_html(self):

        try:

            async with httpx.AsyncClient(

                verify=False,

                follow_redirects=True,

                timeout=20,

                headers=self.headers

            ) as client:

                response = await client.get(
                    self.base_url
                )

                return response.text

        except Exception as error:

            logger.warning(
                f"HTML fetch failed: {error}"
            )

            return ""

    async def fetch_js(self, url):

        try:

            async with httpx.AsyncClient(

                verify=False,

                follow_redirects=True,

                timeout=20,

                headers=self.headers

            ) as client:

                response = await client.get(
                    url
                )

                return response.text

        except Exception as error:

            logger.warning(
                f"JS fetch failed: {error}"
            )

            return ""

    def extract_js_files(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        js_files = []

        for script in soup.find_all(
            "script"
        ):

            src = script.get("src")

            if not src:
                continue

            if src.startswith("http"):

                js_files.append(src)

            elif src.startswith("/"):

                js_files.append(
                    self.base_url + src
                )

        return list(set(js_files))

    def extract_endpoints(self, content):

        pattern = r"""
        (?:
            https?://[^\s"'<>]+
            |
            /[a-zA-Z0-9_\-/\.]+
        )
        """

        matches = re.findall(
            pattern,
            content,
            re.VERBOSE
        )

        return list(set(matches))

    def detect_secrets(self, content):

        patterns = {

            "AWS Access Key": (
                r"AKIA[0-9A-Z]{16}"
            ),

            "Google API Key": (
                r"AIza[0-9A-Za-z\-_]{35}"
            ),

            "Stripe Live Key": (
                r"sk_live_[0-9a-zA-Z]{24}"
            ),

            "GitHub Token": (
                r"github_pat_[0-9A-Za-z_]+"
            ),

            "JWT Token": (
                r"eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+"
            ),

            "Firebase URL": (
                r"https://[a-z0-9\-]+\.firebaseio\.com"
            ),

            "Discord Webhook": (
                r"https://discord(?:app)?\.com/api/webhooks/[0-9]+/[A-Za-z0-9_\-]+"
            )
        }

        findings = {}

        for name, pattern in (
            patterns.items()
        ):

            matches = re.findall(
                pattern,
                content
            )

            if matches:

                findings[name] = list(
                    set(matches)
                )

        return findings

    async def run(self):

        logger.info(
            f"Analyzing JavaScript for {self.domain}"
        )

        html = await self.fetch_html()

        if not html:

            return {}

        js_files = (
            self.extract_js_files(html)
        )

        logger.info(
            f"Found {len(js_files)} JS files"
        )

        results = {}

        for js_url in js_files:

            logger.info(
                f"Processing {js_url}"
            )

            content = await self.fetch_js(
                js_url
            )

            if not content:
                continue

            endpoints = (
                self.extract_endpoints(
                    content
                )
            )

            secrets = (
                self.detect_secrets(
                    content
                )
            )

            results[js_url] = {

                "total_endpoints": (
                    len(endpoints)
                ),

                "endpoints": endpoints,

                "secrets": secrets
            }

        logger.info(
            (
                f"JS analysis completed "
                f"with {len(results)} files"
            )
        )

        return results