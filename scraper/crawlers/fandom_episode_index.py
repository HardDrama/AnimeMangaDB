from bs4 import BeautifulSoup
import re

from scraper.core.http_client import HttpClient
from scraper.models import EpisodeReference


class FandomEpisodeIndexCrawler:
    """
    Discovers episode numbers from One Piece Fandom Episode Guide pages.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = HttpClient()

    def get_episode_list(self) -> list[EpisodeReference]:
        guide_url = f"{self.base_url}/wiki/Episode_Guide"

        html = self.client.fetch(guide_url)
        soup = BeautifulSoup(html, "html.parser")

        saga_links: set[str] = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if "/wiki/Episode_Guide/" not in href:
                continue

            # Remove arc fragments like #Arabasta_Arc
            href = href.split("#")[0]

            full_url = self.base_url + href
            saga_links.add(full_url)

        episode_numbers: set[int] = set()

        for url in sorted(saga_links):
            html = self.client.fetch(url)
            soup = BeautifulSoup(html, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"]

                match = re.search(r"/wiki/Episode_(\d+)$", href)

                if match:
                    episode_numbers.add(int(match.group(1)))

        return [
            EpisodeReference(
                episode_number=episode_number,
                url=f"{self.base_url}/wiki/Episode_{episode_number}",
            )
            for episode_number in sorted(episode_numbers)
        ]