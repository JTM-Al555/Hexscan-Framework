import asyncio
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

from ai.analyzer import AIAnalyzer
from ai.cve_mapper import CVEMapper

from core.async_scanner import AsyncPortScanner
from core.dns_enum import DNSEnumerator
from core.headers_analyzer import HeadersAnalyzer
from core.http_probe import HTTPProbe
from core.js_analyzer import JavaScriptAnalyzer
from core.screenshot import ScreenshotEngine
from core.ssl_analyzer import SSLAnalyzer
from core.subdomain_enum import SubdomainEnumerator
from core.tech_fingerprint import TechnologyFingerprinter
from core.web_crawler import WebCrawler
from core.whois_lookup import WhoisLookup

from output.html_reporter import HTMLReporter
from output.json_reporter import JSONReporter
from output.markdown_reporter import MarkdownReporter

from utils.banner import show_banner
from utils.cli import get_args
from utils.helpers import validate_domain
from utils.logger import logger
from output.pdf_reporter import (
    PDFReporter
)


console = Console()


class ReconFramework:

    def __init__(self, domain):

        self.domain = domain

        self.results = {}

        self.start_time = time.time()

    async def run(self):

        logger.info(
            f"Starting recon against {self.domain}"
        )

        console.print(
            Panel.fit(
                (
                    f"[bold cyan]Target:[/bold cyan] "
                    f"{self.domain}"
                ),
                title="AI-Powered Recon Framework"
            )
        )

        try:

            await self.run_basic_modules()

            await self.run_async_modules()

            self.run_analysis_modules()

            self.run_ai_analysis()

            self.generate_reports()

            self.show_statistics()

            return self.results

        except Exception as error:

            logger.error(
                f"Framework error: {error}"
            )


            console.print(
                (
                    f"[bold red]Error:[/bold red] "
                    f"{error}"
                )
            )

            return {}

    async def run_basic_modules(self):

        console.print(
            "\n[bold blue]"
            "Running basic enumeration..."
            "[/bold blue]"
        )

        self.results["dns"] = (
            DNSEnumerator(
                self.domain
            ).run()
        )

        self.results["whois"] = (
            WhoisLookup(
                self.domain
            ).run()
        )

        self.results["http"] = (
            HTTPProbe(
                self.domain
            ).run()
        )

    async def run_async_modules(self):

        console.print(
            "\n[bold blue]"
            "Running async modules..."
            "[/bold blue]"
        )

        with Progress() as progress:

            task = progress.add_task(
                "[cyan]Scanning...",
                total=4
            )

            crawl_task = (
                WebCrawler(
                    self.domain
                ).crawl()
            )

            js_task = (
                JavaScriptAnalyzer(
                    self.domain
                ).run()
            )

            screenshot_task = (
                ScreenshotEngine(
                    self.domain
                ).run()
            )

            port_task = (
                AsyncPortScanner(
                    self.domain
                ).run()
            )

            (
                crawl_results,
                js_results,
                screenshots,
                ports
            ) = await asyncio.gather(
                crawl_task,
                js_task,
                screenshot_task,
                port_task
            )

            progress.update(
                task,
                advance=4
            )

        self.results[
            "web_crawler"
        ] = crawl_results

        self.results[
            "javascript_analysis"
        ] = js_results

        self.results[
            "screenshots"
        ] = screenshots

        self.results[
            "ports"
        ] = ports

    def run_analysis_modules(self):

        console.print(
            "\n[bold blue]"
            "Running analysis modules..."
            "[/bold blue]"
        )

        headers = (
            self.results[
                "http"
            ].get(
                "headers",
                {}
            )
        )

        self.results[
            "subdomains"
        ] = (
            SubdomainEnumerator(
                self.domain
            ).run()
        )

        self.results[
            "ssl"
        ] = (
            SSLAnalyzer(
                self.domain
            ).run()
        )

        self.results[
            "security_headers"
        ] = (
            HeadersAnalyzer(
                headers
            ).analyze()
        )

        technologies = (
            TechnologyFingerprinter(
                headers
            ).detect()
        )

        self.results[
            "technologies"
        ] = technologies

        self.results[
            "cves"
        ] = (
            CVEMapper(
                technologies
            ).map_cves()
        )

    def run_ai_analysis(self):

        console.print(
            "\n[bold blue]"
            "Running AI analysis..."
            "[/bold blue]"
        )

        ai_analysis = (
            AIAnalyzer(
                self.results
            ).analyze()
        )

        self.results[
            "ai_analysis"
        ] = ai_analysis

    def generate_reports(self):

        console.print(
            "\n[bold blue]"
            "Generating reports..."
            "[/bold blue]"
        )

        JSONReporter(
            self.domain,
            self.results
        ).save()

        MarkdownReporter(
            self.domain,
            self.results
        ).generate()

        HTMLReporter(
            self.domain,
            self.results
        ).generate()

        PDFReporter(
            self.domain,
            self.results
        ).generate()

    def show_statistics(self):

        elapsed = round(
            time.time() -
            self.start_time,
            2
        )

        stats = Table(
            title="Scan Statistics"
        )

        stats.add_column(
            "Metric",
            style="cyan"
        )

        stats.add_column(
            "Value",
            style="green"
        )

        stats.add_row(
            "Target",
            self.domain
        )

        stats.add_row(
            "Modules",
            str(
                len(
                    self.results
                )
            )
        )

        stats.add_row(
            "Execution Time",
            f"{elapsed}s"
        )

        stats.add_row(
            "Generated",
            str(
                datetime.utcnow()
            )
        )

        console.print(stats)

        logger.info(
            f"Recon completed in {elapsed}s"
        )


def display_results(results):

    table = Table(
        title="Recon Summary"
    )

    table.add_column(
        "Module",
        style="cyan",
        no_wrap=True
    )

    table.add_column(
        "Status",
        style="green"
    )

    table.add_column(
        "Type",
        style="yellow"
    )

    for key, value in results.items():

        status = (
            "Completed"
            if value
            else "Empty"
        )

        value_type = (
            type(value).__name__
        )

        table.add_row(
            key,
            status,
            value_type
        )

    console.print(table)


async def main():

    show_banner()

    args = get_args()

    domain = args.domain

    if not validate_domain(domain):

        console.print(
            "[bold red]"
            "Invalid domain"
            "[/bold red]"
        )

        return

    framework = (
        ReconFramework(domain)
    )

    results = await framework.run()

    if results:

        display_results(results)

        console.print(
            "\n[bold green]"
            "Reports generated successfully."
            "[/bold green]"
        )

        console.print(
            "[bold cyan]"
            "Check the output folder."
            "[/bold cyan]"
        )

    else:

        console.print(
            "[bold red]"
            "Recon failed."
            "[/bold red]"
        )


if __name__ == "__main__":

    asyncio.run(main())