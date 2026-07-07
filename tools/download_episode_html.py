import argparse
from pathlib import Path

from scraper.core.browser_client import BrowserClient
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config


def main():
    parser = argparse.ArgumentParser(
        description="Download rendered episode HTML for inspection."
    )

    parser.add_argument(
        "--config",
        default="configs/fandom/one_piece.json",
        help="Path to provider config.",
    )

    parser.add_argument(
        "--episode",
        type=int,
        default=1,
        help="Episode number to download.",
    )

    args = parser.parse_args()

    config = load_provider_config(args.config)

    provider = FandomProvider(config)

    url = provider.build_episode_url(args.episode)

    print(f"Downloading {url}")

    html = BrowserClient().fetch(url)

    filename = f"episode_{args.episode}.html"

    Path(filename).write_text(
        html,
        encoding="utf-8",
    )

    print(f"Saved {filename}")


if __name__ == "__main__":
    main()