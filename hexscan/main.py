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
from core.dir_fuzzer import DirectoryFuzzer
from core.waf_detector import WAFDetector
from core.parameter_discovery import ParameterDiscovery
from database.database import DatabaseManager

from output.html_reporter import HTMLReporter
from output.json_reporter import JSONReporter
from output.markdown_reporter import MarkdownReporter

from utils.banner import show_banner
from utils.cli import get_args
from utils.helpers import validate_domain
from utils.logger import logger
from output.pdf_reporter import PDFReporter
from core.risk_engine import RiskEngine

# ✅ ADDED UI SYSTEM
from utils.ui import show_header, section, task


console = Console()


class ReconFramework:

    def __init__(self, domain):

        self.domain = domain
        self.results = {}
        self.start_time = time.time()

        # flags
        self.no_ai = False
        self.fast_mode = False
        self.deep_mode = False
        self.json_mode = False

    async def run(self):

        logger.info(f"Starting recon against {self.domain}")

        console.print(
            Panel.fit(
                f"[bold cyan]Target:[/bold cyan] {self.domain}",
                title="HEXSCAN"
            )
        )

        # ✅ ADDED HEADER UI
        show_header(self.domain, "NORMAL")

        try:
            section("DISCOVERY PHASE")

            await self.run_basic_modules()

            section("DEEP SCAN PHASE")

            await self.run_async_modules()

            section("ANALYSIS PHASE")

            self.run_analysis_modules()

            self.run_ai_analysis()

            section("REPORTING PHASE")

            self.generate_reports()

            DatabaseManager().save_scan(
    self.domain,
    self.results
)

            self.show_statistics()

            return self.results

        except Exception as error:

            logger.error(f"Framework error: {error}")

            console.print(
                f"[bold red]Error:[/bold red] {error}"
            )

            return {}

    async def run_basic_modules(self):

        console.print("\n[bold blue]Running basic enumeration...[/bold blue]")

        task("DNS Enumeration", "running")
        self.results["dns"] = DNSEnumerator(self.domain).run()
        task("DNS Enumeration", "done")

        task("WHOIS Lookup", "running")
        self.results["whois"] = WhoisLookup(self.domain).run()
        task("WHOIS Lookup", "done")

        task("HTTP Probe", "running")
        # ✅ FIXED: await the async HTTPProbe
        self.results["http"] = await HTTPProbe(self.domain).run()
        task("HTTP Probe", "done")

    async def run_async_modules(self):

        console.print("\n[bold blue]Running async modules...[/bold blue]")

        with Progress() as progress:

            task_id = progress.add_task("[cyan]Scanning...", total=4)

            crawl_task = WebCrawler(self.domain).crawl()
            dir_task = DirectoryFuzzer(self.domain).run()
            js_task = JavaScriptAnalyzer(self.domain).run()
            screenshot_task = ScreenshotEngine(self.domain).run()
            port_task = AsyncPortScanner(self.domain).run()

            crawl_results, dir_results, js_results, screenshots, ports = await asyncio.gather(
                crawl_task,
                dir_task,
                js_task,
                screenshot_task,
                port_task
            )

            progress.update(task_id, advance=4)

        self.results["web_crawler"] = crawl_results
        self.results["directories"] = dir_results
        self.results["javascript_analysis"] = js_results
        self.results["screenshots"] = screenshots
        self.results["ports"] = ports
        

    def run_analysis_modules(self):

        console.print("\n[bold blue]Running analysis modules...[/bold blue]")

        headers = self.results["http"].get("headers", {})

        self.results["subdomains"] = SubdomainEnumerator(self.domain).run()
        self.results["ssl"] = SSLAnalyzer(self.domain).run()
        self.results["security_headers"] = HeadersAnalyzer(headers).analyze()
        self.results["waf"] = WAFDetector(
    headers
).detect()
        self.results["parameters"] = (
    ParameterDiscovery(
        self.results
    ).run()
)

        technologies = TechnologyFingerprinter(headers).detect()
        self.results["technologies"] = technologies

        self.results["cves"] = CVEMapper(technologies).map_cves()
        self.results["risk_analysis"] = (
    RiskEngine(
        self.results
    ).analyze()
)

    def run_ai_analysis(self):

        console.print("\n[bold blue]Running AI analysis...[/bold blue]")

        if self.no_ai:
            self.results["ai_analysis"] = "AI disabled"
            return

        self.results["ai_analysis"] = AIAnalyzer(self.results).analyze()

    def generate_reports(self):

        console.print("\n[bold blue]Generating reports...[/bold blue]")

        JSONReporter(self.domain, self.results).save()
        MarkdownReporter(self.domain, self.results).generate()
        HTMLReporter(self.domain, self.results).generate()
        PDFReporter(self.domain, self.results).generate()

    def show_statistics(self):

        elapsed = round(time.time() - self.start_time, 2)

        stats = Table(title="Scan Statistics")

        stats.add_column("Metric", style="cyan")
        stats.add_column("Value", style="green")

        stats.add_row("Target", self.domain)
        stats.add_row("Modules", str(len(self.results)))
        stats.add_row("Execution Time", f"{elapsed}s")
        stats.add_row("Generated", str(datetime.utcnow()))

        console.print(stats)

        logger.info(f"Recon completed in {elapsed}s")


def display_results(results):

    table = Table(title="Recon Summary")

    table.add_column("Module", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Type", style="yellow")

    for key, value in results.items():

        status = "Completed" if value else "Empty"
        value_type = type(value).__name__

        table.add_row(key, status, value_type)

    console.print(table)


async def main():

    show_banner()
    args = get_args()

    domain = args.domain

    if not validate_domain(domain):
        console.print("[bold red]Invalid domain[/bold red]")
        return

    framework = ReconFramework(domain)

    framework.no_ai = getattr(args, "no_ai", False)
    framework.fast_mode = getattr(args, "fast", False)
    framework.deep_mode = getattr(args, "deep", False)
    framework.json_mode = getattr(args, "json", False)

    results = await framework.run()

    if framework.json_mode:
        import json
        print(json.dumps(results, indent=4))
        return

    if results:

        display_results(results)

        console.print("\n[bold green]Reports generated successfully.[/bold green]")
        console.print("[bold cyan]Check the output folder.[/bold cyan]")

    else:
        console.print("[bold red]Recon failed.[/bold red]")


def cli_main():
    """
    Entry point for hexscan CLI command
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]HEXSCAN interrupted by user[/bold red]")
        logger.warning("Scan interrupted by user")
