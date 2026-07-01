from bs4 import BeautifulSoup
import re

from scraper.core.http_client import HttpClient


class FandomEpisodeIndexCrawler:
    """
    Robust crawler for Fandom Episode Guide.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = HttpClient()

    def get_episode_list(self) -> list[int]:
        guide_url = f"{self.base_url}/wiki/Episode_Guide"

        html = self.client.fetch(guide_url)
        soup = BeautifulSoup(html, "html.parser")

        saga_links = set()

        # STEP 1: collect saga links
        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "Episode_Guide/" in href and href != "/wiki/Episode_Guide":
                saga_links.add(self.base_url + href)

        episode_numbers = set()

        # STEP 2: scrape saga pages
        for url in saga_links:
            html = self.client.fetch(url)
            soup = BeautifulSoup(html, "html.parser")

            # Extract ANY text containing "Episode XXX"
            text = soup.get_text(" ", strip=True)

            matches = re.findall(r"Episode\s+(\d+)", text)

            for m in matches:
                num = int(m)
                if num > 0:
                    episode_numbers.add(num)

        return sorted(episode_numbers)