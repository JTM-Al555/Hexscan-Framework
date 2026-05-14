import argparse

def get_args():

    parser = argparse.ArgumentParser(
        description="Hexscan - AI Cyber Recon Tool"
    )

    parser.add_argument(
        "domain",
        help="Target domain (example: chatgpt.com)"
    )

    parser.add_argument(
        "--fast",
        action="store_true",
        help="Run lightweight scan only"
    )

    parser.add_argument(
        "--deep",
        action="store_true",
        help="Run full deep scan (default)"
    )

    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable AI analysis"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output only JSON results"
    )

    return parser.parse_args()