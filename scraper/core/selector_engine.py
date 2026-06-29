from bs4 import BeautifulSoup

from scraper.models import ProviderConfig


class SelectorEngine:
    """
    Retrieves data from HTML using selectors defined in a ProviderConfig.
    """

    def __init__(self, soup: BeautifulSoup, config: ProviderConfig):
        self.soup = soup
        self.config = config

    def get_text(self, selector_name: str) -> str | None:
        """
        Return the text for a configured selector.
        """

        selectors = self.config.selectors.model_dump()

        selector = selectors.get(selector_name)

        if not selector:
            return None

        element = self.soup.select_one(selector)

        if element is None:
            return None

        return element.get_text(strip=True)