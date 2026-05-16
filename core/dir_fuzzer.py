import asyncio
import httpx

from utils.logger import logger


class DirectoryFuzzer:

    def __init__(self, domain):

        self.domain = domain

        self.base_url = (
            f"https://{domain}"
        )

        self.wordlist = [

    # AUTH
    "login",
    "signin",
    "signup",
    "register",
    "auth",
    "oauth",

    # ADMIN
    "admin",
    "administrator",
    "dashboard",
    "control",
    "panel",
    "cpanel",
    "manage",

    # API
    "api",
    "api/v1",
    "api/v2",
    "graphql",
    "swagger",
    "swagger-ui",
    "openapi",

    # DEV
    "dev",
    "test",
    "testing",
    "staging",
    "beta",
    "sandbox",

    # BACKUPS
    "backup",
    "backups",
    "db",
    "database",
    "dump",
    "old",
    "temp",

    # CONFIG
    "config",
    ".env",
    ".git",
    ".github",
    ".svn",

    # FILES
    "robots.txt",
    "sitemap.xml",
    "crossdomain.xml",

    # CONTENT
    "uploads",
    "upload",
    "images",
    "img",
    "media",
    "assets",

    # JS/CSS
    "js",
    "css",
    "static",

    # USER
    "account",
    "profile",
    "user",
    "users",

    # SHOP
    "cart",
    "checkout",
    "payment",
    "orders",

    # DOCS
    "docs",
    "documentation",
    "redoc",

    # INTERNAL
    "internal",
    "private",
    "secret",

    # COMMON
    "search",
    "home",
    "status",
    "health",
    "server-status",

    # CMS
    "wp-admin",
    "wp-content",
    "wordpress",

    # MONITORING
    "metrics",
    "monitor",
    "grafana",
    "prometheus"
]

        self.results = []

    async def check_path(
        self,
        client,
        path
    ):

        url = (
            f"{self.base_url}/{path}"
        )

        try:

            response = await client.get(
                url
            )

            if response.status_code in [
                200,
                301,
                302,
                403
            ]:

                logger.info(
                    (
                        f"Discovered: "
                        f"{url}"
                    )
                )

                self.results.append({

                    "url": url,

                    "status": (
                        response.status_code
                    )
                })

        except Exception:
            pass

    async def run(self):

        logger.info(
            (
                f"Starting directory fuzzing "
                f"for {self.domain}"
            )
        )

        async with httpx.AsyncClient(

            verify=False,

            follow_redirects=True,

            timeout=10

        ) as client:

            tasks = []

            for path in self.wordlist:

                tasks.append(

                    self.check_path(
                        client,
                        path
                    )
                )

            await asyncio.gather(
                *tasks
            )

        return {

            "total_found": len(
                self.results
            ),

            "directories": (
                self.results
            )
        }