import re
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from scraper.models.chapter_metadata import ChapterMetadata
from scraper.models.provider_config import ChapterSelectorConfig


class FandomChapterMetadataExtractor:
    """
    Extracts Scope v3 chapter metadata from a Fandom page.

    Series-specific page structures are represented through
    configured extraction strategies.
    """

    def __init__(
        self,
        selectors: ChapterSelectorConfig,
    ):
        self.selectors = selectors

    def parse(
        self,
        html: str,
        chapter_number: int,
        source_url: str,
    ) -> ChapterMetadata:
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        chapter_title = self._extract_title(
            soup=soup,
            chapter_number=chapter_number,
        )

        manga_arc = self._extract_arc(
            soup=soup,
        )

        return ChapterMetadata(
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            manga_arc=manga_arc,
            source_url=source_url,
            last_updated=datetime.now(),
        )

    def _extract_title(
        self,
        soup: BeautifulSoup,
        chapter_number: int,
    ) -> str | None:
        strategy = self.selectors.title_strategy

        if strategy == "one_piece_title_sentence":
            return self._extract_one_piece_title_sentence(
                soup=soup,
                chapter_number=chapter_number,
            )

        if strategy == "naruto_page_title":
            return self._extract_naruto_page_title(
                soup=soup,
                chapter_number=chapter_number,
            )

        if strategy == "selector":
            return self._extract_selector_text(
                soup=soup,
                selector=self.selectors.title,
            )

        raise ValueError(
            f"Unsupported chapter title strategy: {strategy}"
        )

    def _extract_arc(
        self,
        soup: BeautifulSoup,
    ) -> str | None:
        strategy = self.selectors.arc_strategy

        if strategy == "one_piece_arc_category":
            return self._extract_one_piece_arc_category(
                soup
            )

        if strategy == "naruto_factbox_property":
            return self._extract_naruto_arc_factbox(
                soup
            )

        if strategy == "selector":
            return self._extract_selector_text(
                soup=soup,
                selector=self.selectors.manga_arc,
            )

        raise ValueError(
            f"Unsupported chapter arc strategy: {strategy}"
        )

    @staticmethod
    def _extract_one_piece_title_sentence(
        soup: BeautifulSoup,
        chapter_number: int,
    ) -> str | None:
        pattern = re.compile(
            rf'Chapter\s+{chapter_number}\s+is titled\s+["“](.+?)["”]',
            re.IGNORECASE,
        )

        for paragraph in soup.find_all("p"):
            text = " ".join(
                paragraph.get_text(
                    " ",
                    strip=True,
                ).split()
            )

            match = pattern.search(text)

            if match:
                return match.group(1).strip()

        return None

    def _extract_one_piece_arc_category(
        self,
        soup: BeautifulSoup,
    ) -> str | None:
        selector = self.selectors.manga_arc

        if not selector:
            return None

        element = soup.select_one(
            selector
        )

        if element is None:
            return None

        text = self._normalized_text(
            element
        )

        suffix = " Chapters"

        if text.endswith(suffix):
            text = text.removesuffix(suffix)

        return text or None

    def _extract_naruto_page_title(
        self,
        soup: BeautifulSoup,
        chapter_number: int,
    ) -> str | None:
        title = self._extract_selector_text(
            soup=soup,
            selector=self.selectors.title,
        )

        if title is None:
            return None

        suffix_pattern = re.compile(
            rf"\s*\(chapter\s+{chapter_number}\)\s*$",
            re.IGNORECASE,
        )

        return suffix_pattern.sub(
            "",
            title,
        ).strip() or None

    @staticmethod
    def _extract_naruto_arc_factbox(
        soup: BeautifulSoup,
    ) -> str | None:
        property_links = soup.select(
            ".smw-factbox-property-name a"
        )

        for property_link in property_links:
            property_name = property_link.get_text(
                " ",
                strip=True,
            )

            if property_name.casefold() != "arc":
                continue

            property_container = property_link.find_parent(
                class_="smw-factbox-property-name"
            )

            if property_container is None:
                continue

            value_container = property_container.find_next_sibling(
                class_="smw-factbox-property-values"
            )

            if value_container is None:
                continue

            value_link = value_container.find(
                "a",
                href=True,
            )

            if value_link is not None:
                return FandomChapterMetadataExtractor._normalized_text(
                    value_link
                )

            value = FandomChapterMetadataExtractor._normalized_text(
                value_container
            )

            return value or None

        return None

    @staticmethod
    def _extract_selector_text(
        soup: BeautifulSoup,
        selector: str | None,
    ) -> str | None:
        if not selector:
            return None

        element = soup.select_one(
            selector
        )

        if element is None:
            return None

        text = FandomChapterMetadataExtractor._normalized_text(
            element
        )

        return text or None

    @staticmethod
    def _normalized_text(
        element: Tag,
    ) -> str:
        return " ".join(
            element.get_text(
                " ",
                strip=True,
            ).split()
        )