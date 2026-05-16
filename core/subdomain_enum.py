import requests

from utils.logger import logger


class SubdomainEnumerator:

    def __init__(self, domain):

        self.domain = domain

        self.results = set()

    def crtsh(self):

        try:

            logger.info(
                "Querying crt.sh"
            )

            url = (
                "https://crt.sh/"
                f"?q=%.{self.domain}"
                "&output=json"
            )

            response = requests.get(
                url,
                timeout=20
            )

            if response.status_code != 200:
                return

            data = response.json()

            for entry in data:

                name = entry.get(
                    "name_value",
                    ""
                )

                for sub in name.split("\n"):

                    sub = sub.strip()

                    if (
                        self.domain in sub
                    ):

                        self.results.add(
                            sub
                        )

        except Exception as error:

            logger.warning(
                f"crt.sh failed: {error}"
            )

    def hackertarget(self):

        try:

            logger.info(
                "Querying HackerTarget"
            )

            url = (
                "https://api.hackertarget.com/"
                f"hostsearch/?q={self.domain}"
            )

            response = requests.get(
                url,
                timeout=20
            )

            if response.status_code != 200:
                return

            lines = response.text.splitlines()

            for line in lines:

                if "," not in line:
                    continue

                subdomain = (
                    line.split(",")[0]
                )

                self.results.add(
                    subdomain
                )

        except Exception as error:

            logger.warning(
                (
                    "HackerTarget failed: "
                    f"{error}"
                )
            )

    def common_permutations(self):

        common = [

            "dev",
            "api",
            "test",
            "staging",
            "mail",
            "vpn",
            "beta",
            "admin",
            "cdn",
            "portal",
            "dashboard",
            "app",
            "mobile",
            "internal"
        ]

        for sub in common:

            self.results.add(
                f"{sub}.{self.domain}"
            )

    def run(self):

        logger.info(
            (
                f"Starting subdomain "
                f"enumeration for "
                f"{self.domain}"
            )
        )

        self.crtsh()

        self.hackertarget()

        self.common_permutations()

        final = sorted(
            list(self.results)
        )

        logger.info(
            (
                f"Discovered "
                f"{len(final)} "
                f"subdomains"
            )
        )

        return {

            "total": len(final),

            "subdomains": final
        }