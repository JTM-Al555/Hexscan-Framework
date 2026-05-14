import argparse


def get_args():

    parser = argparse.ArgumentParser(
        description=(
            "AI-Powered Recon Framework"
        )
    )

    parser.add_argument(
        "domain",
        help="Target domain"
    )

    return parser.parse_args()