from scraper.core.browser_client import BrowserClient


class HttpClient:
    """
    A simple HTTP client for downloading web pages.
    """

    def fetch(self, url: str) -> str:
        return BrowserClient().fetch(url)