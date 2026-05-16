import asyncio
import httpx

from bs4 import BeautifulSoup
from urllib.parse import (
    urljoin,
    urlparse
)

from utils.logger import logger


class WebCrawler:

    def __init__(self, domain):

        self.domain = domain

        self.base_url = (
            f"https://{domain}"
        )

        self.visited = set()

        self.found_links = set()

        self.interesting = {

            "admin_panels": [],

            "api_endpoints": [],

            "graphql": [],

            "auth_pages": []
        }

        self.headers = {

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            )
        }

    async def fetch(self, url):

        try:

            async with httpx.AsyncClient(

                headers=self.headers,

                verify=False,

                follow_redirects=True,

                timeout=15

            ) as client:

                response = await client.get(
                    url
                )

                return response.text

        except Exception as error:

            logger.warning(
                f"Failed to fetch {url}: {error}"
            )

            return ""

    def is_internal(self, url):

        parsed = urlparse(url)

        return (
            parsed.netloc == ""
            or self.domain in parsed.netloc
        )

    def analyze_link(self, url):

        lower = url.lower()

        if "admin" in lower:

            self.interesting[
                "admin_panels"
            ].append(url)

        if "login" in lower or "auth" in lower:

            self.interesting[
                "auth_pages"
            ].append(url)

        if "/api/" in lower:

            self.interesting[
                "api_endpoints"
            ].append(url)

        if "graphql" in lower:

            self.interesting[
                "graphql"
            ].append(url)

    async def crawl_page(self, url):

        if url in self.visited:
            return

        self.visited.add(url)

        logger.info(
            f"Crawling: {url}"
        )

        html = await self.fetch(url)

        if not html:
            return

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        for tag in soup.find_all("a"):

            href = tag.get("href")

            if not href:
                continue

            full_url = urljoin(
                self.base_url,
                href
            )

            if not self.is_internal(
                full_url
            ):
                continue

            clean_url = (
                full_url.split("#")[0]
            )

            self.found_links.add(
                clean_url
            )

            self.analyze_link(
                clean_url
            )

    async def check_special_files(self):

        special_files = [

            "/robots.txt",

            "/sitemap.xml"
        ]

        found = []

        for path in special_files:

            url = (
                self.base_url + path
            )

            content = await self.fetch(
                url
            )

            if content:

                found.append(url)

        return found

    async def crawl(self):

        logger.info(
            f"Starting crawl for {self.domain}"
        )

        await self.crawl_page(
            self.base_url
        )

        special_files = (
            await self.check_special_files()
        )

        results = {

            "total_links": len(
                self.found_links
            ),

            "links": list(
                self.found_links
            ),

            "interesting": (
                self.interesting
            ),

            "special_files": (
                special_files
            )
        }

        logger.info(
            (
                f"Crawler discovered "
                f"{len(self.found_links)} "
                f"links"
            )
        )

        return results