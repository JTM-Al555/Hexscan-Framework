import requests

from utils.logger import logger


class CVELookup:

    def __init__(self):

        self.base_url = (
            "https://services.nvd.nist.gov"
            "/rest/json/cves/2.0"
        )

    def search(self, keyword):

        try:

            response = requests.get(
                self.base_url,
                params={
                    "keywordSearch": keyword
                },
                timeout=15
            )

            data = response.json()

            vulnerabilities = (
                data.get(
                    "vulnerabilities",
                    []
                )
            )

            results = []

            for item in vulnerabilities[:5]:

                cve = item.get(
                    "cve",
                    {}
                )

                results.append({
                    "id": cve.get("id"),
                    "published": (
                        cve.get(
                            "published"
                        )
                    )
                })

            return results

        except Exception as error:

            logger.warning(
                f"CVE lookup failed: {error}"
            )

            return []