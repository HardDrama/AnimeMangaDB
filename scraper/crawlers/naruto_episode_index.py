from bs4 import BeautifulSoup

from scraper.core.http_client import HttpClient
from scraper.crawlers.base_episode_index import BaseEpisodeIndexCrawler
from scraper.models import EpisodeReference


class NarutoEpisodeIndexCrawler(BaseEpisodeIndexCrawler):
    """
    Discovers original Naruto episode URLs from Narutopedia.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = HttpClient()

    def get_episode_list(self) -> list[EpisodeReference]:
        index_url = f"{self.base_url}/wiki/List_of_Animated_Media"

        html = self.client.fetch(index_url)
        soup = BeautifulSoup(html, "html.parser")

        tables = soup.find_all("table")

        if not tables:
            return []

        # Table 1 is original Naruto.
        naruto_table = tables[0]

        episodes: list[tuple[int, str]] = []

        for row in naruto_table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])

            if len(cells) < 2:
                continue

            episode_text = cells[0].get_text(strip=True)

            if not episode_text.isdigit():
                continue

            episode_number = int(episode_text)

            title_link = cells[1].find("a", href=True)

            if not title_link:
                continue

            href = title_link["href"]

            if href.startswith("http"):
                episode_url = href
            else:
                episode_url = self.base_url + href

            episodes.append(
                EpisodeReference(
                    episode_number=episode_number,
                    url=episode_url,
                )
            )

        return episodes