from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scraper.models.provider_config import ProviderConfig


class ChapterUrlDiscoveryService:
    """
    Discovers chapter URLs using the configured series strategy.
    """

    def __init__(
        self,
        config: ProviderConfig,
        browser_client=None,
    ):
        self.config = config
        self.browser_client = browser_client

    def discover_url(
        self,
        chapter_number: int,
    ) -> str | None:
        chapter_config = self.config.chapter_metadata

        if chapter_config is None:
            return None

        if chapter_config.url_strategy == "numbered":
            return self._build_numbered_url(
                chapter_number
            )

        if (
            chapter_config.url_strategy
            == "discovered_links"
        ):
            return self._discover_link_from_index(
                chapter_number
            )

        raise ValueError(
            "Unsupported chapter URL strategy: "
            f"{chapter_config.url_strategy}"
        )

    def _build_numbered_url(
        self,
        chapter_number: int,
    ) -> str | None:
        chapter_config = self.config.chapter_metadata

        if (
            chapter_config is None
            or chapter_config.chapter_path is None
        ):
            return None

        path = chapter_config.chapter_path.format(
            chapter=chapter_number
        )

        return urljoin(
            self.config.base_url,
            path,
        )

    def _discover_link_from_index(
        self,
        chapter_number: int,
    ) -> str | None:
        chapter_config = self.config.chapter_metadata

        if (
            chapter_config is None
            or self.browser_client is None
        ):
            return None

        index_url = urljoin(
            self.config.base_url,
            chapter_config.index_path,
        )

        html = self.browser_client.fetch(
            index_url
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        target_text = f"chapter {chapter_number}"

        for link in soup.find_all(
            "a",
            href=True,
        ):
            link_text = " ".join(
                link.get_text(
                    " ",
                    strip=True,
                ).lower().split()
            )

            title_text = (
                link.get("title", "")
                .strip()
                .lower()
            )

            if (
                target_text in link_text
                or target_text in title_text
            ):
                return urljoin(
                    self.config.base_url,
                    link["href"],
                )

        return None