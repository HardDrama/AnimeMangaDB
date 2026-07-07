from pathlib import Path

from scraper.core.browser_client import BrowserClient
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config


def main():
    episode_number = 1

    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    provider = FandomProvider(config)

    url = provider.build_episode_url(
        episode_number
    )

    print(f"Downloading {url}")

    html = BrowserClient().fetch(url)

    filename = (
        f"episode_{episode_number}.html"
    )

    Path(filename).write_text(
        html,
        encoding="utf-8",
    )

    print(f"Saved {filename}")


if __name__ == "__main__":
    main()