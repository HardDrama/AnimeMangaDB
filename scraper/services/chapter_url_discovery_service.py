import re
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
        self._index_html: str | None = None

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

        if (
            chapter_config.url_strategy
            == "numbered_list_items"
        ):
            return self._discover_numbered_list_item(
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

        html = self._get_index_html(
            index_url
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        for link in soup.find_all(
            "a",
            href=True,
        ):
            link_text = " ".join(
                link.get_text(
                    " ",
                    strip=True,
                ).split()
            )

            title_text = (
                link.get("title", "")
                .strip()
            )

            candidate_numbers = set()

            for candidate_text in (
                link_text,
                title_text,
            ):
                candidate_numbers.update(
                    self._extract_chapter_numbers(
                        candidate_text
                    )
                )

            if chapter_number in candidate_numbers:
                return urljoin(
                    self.config.base_url,
                    link["href"],
                )

        return None

    def _discover_numbered_list_item(
        self,
        chapter_number: int,
    ) -> str | None:
        chapter_config = self.config.chapter_metadata

        if (
            chapter_config is None
            or self.browser_client is None
            or chapter_config.index_section_id is None
        ):
            return None

        index_url = urljoin(
            self.config.base_url,
            chapter_config.index_path,
        )

        html = self._get_index_html(
            index_url
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        subsection_ids = (
            chapter_config.index_subsection_ids
            or []
        )

        if subsection_ids:
            return self._discover_from_subsections(
                soup=soup,
                subsection_ids=subsection_ids,
                chapter_number=chapter_number,
            )

        return self._discover_from_h2_section(
            soup=soup,
            section_id=chapter_config.index_section_id,
            chapter_number=chapter_number,
        )
    
    def _discover_from_subsections(
        self,
        soup: BeautifulSoup,
        subsection_ids: list[str],
        chapter_number: int,
    ) -> str | None:
        for subsection_id in subsection_ids:
            heading_marker = soup.find(
                id=subsection_id
            )

            if heading_marker is None:
                continue

            heading = heading_marker.find_parent(
                ["h3", "h4"]
            )

            if heading is None:
                continue

            for sibling in heading.find_next_siblings():
                # A new h2 leaves the parent section.
                # A new h3 starts the next sibling work.
                if sibling.name in {
                    "h2",
                    "h3",
                }:
                    break

                source_url = (
                    self._find_numbered_list_item_url(
                        container=sibling,
                        chapter_number=chapter_number,
                    )
                )

                if source_url is not None:
                    return source_url

        return None

    def _discover_from_h2_section(
        self,
        soup: BeautifulSoup,
        section_id: str,
        chapter_number: int,
    ) -> str | None:
        heading_marker = soup.find(
            id=section_id
        )

        if heading_marker is None:
            return None

        heading = heading_marker.find_parent(
            "h2"
        )

        if heading is None:
            return None

        for sibling in heading.find_next_siblings():
            if sibling.name == "h2":
                break

            source_url = (
                self._find_numbered_list_item_url(
                    container=sibling,
                    chapter_number=chapter_number,
                )
            )

            if source_url is not None:
                return source_url

        return None
    
    def _find_numbered_list_item_url(
        self,
        container,
        chapter_number: int,
    ) -> str | None:
        for list_item in container.select(
            "li"
        ):
            candidate_number = (
                self._extract_numbered_list_item(
                    list_item.get_text(
                        " ",
                        strip=True,
                    )
                )
            )

            if candidate_number != chapter_number:
                continue

            link = list_item.find(
                "a",
                href=True,
            )

            if link is None:
                continue

            return urljoin(
                self.config.base_url,
                link["href"],
            )

        return None

    def _get_index_html(
        self,
        index_url: str,
    ) -> str:
        if self._index_html is None:
            self._index_html = (
                self.browser_client.fetch(
                    index_url
                )
            )

        return self._index_html

    @staticmethod
    def _extract_chapter_numbers(
        text: str,
    ) -> set[int]:
        matches = re.findall(
            r"\bchapter\s+(\d+)\b",
            text,
            flags=re.IGNORECASE,
        )

        return {
            int(match)
            for match in matches
        }

    @staticmethod
    def _extract_numbered_list_item(
        text: str,
    ) -> int | None:
        match = re.match(
            r"^\s*0*(\d+)\.",
            text,
        )

        if match is None:
            return None

        return int(
            match.group(1)
        )