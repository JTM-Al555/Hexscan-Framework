from typing import Dict
import httpx

from config.settings import (
    REQUEST_TIMEOUT,
    USER_AGENT
)

from utils.logger import logger


class HTTPProbe:

    def __init__(self, domain):
        self.domain = domain
        self.targets = [
            f"https://{domain}",
            f"http://{domain}"
        ]

    def collect_headers(self, response):
        important_headers = [
            "server",
            "content-type",
            "content-length",
            "x-powered-by"
        ]

        headers = {}
        for header in important_headers:
            headers[header] = response.headers.get(header, "Not Present")

        return headers

    async def run(self) -> Dict:   # <-- changed to async
        for target in self.targets:
            try:
                async with httpx.AsyncClient(
                    headers={"User-Agent": USER_AGENT},
                    timeout=REQUEST_TIMEOUT,
                    follow_redirects=True
                ) as client:
                    response = await client.get(target)   # <-- await instead of sync

                    return {
                        "url": str(response.url),
                        "status_code": response.status_code,
                        "headers": self.collect_headers(response),
                        "response_size": len(response.text),
                        "body": response.text
                    }

            except Exception as error:
                logger.warning(f"HTTP probe failed: {error}")

        return {"error": "Connection failed"}
