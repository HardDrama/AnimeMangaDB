from scraper.core.browser_client import BrowserClient


class HttpClient:
    def fetch(self, url: str) -> str:
        return BrowserClient().fetch(url)