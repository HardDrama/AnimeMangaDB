from scraper.providers.base_provider import BaseProvider


class FandomProvider(BaseProvider):
    """
    Provider implementation for Fandom wikis.

    Responsibility:
    - ONLY builds episode URLs
    - Does NOT crawl or scrape index pages
    """

    def build_episode_url(self, episode_number: int) -> str:
        """
        Build a direct URL to an episode page.
        """
        return (
            self.config.base_url
            + self.config.episode_path.format(episode=episode_number)
        )

    def get_episode_list(self) -> list[tuple[int, str]]:
        """
        Legacy/compat method (not used by crawler anymore).

        Keeping minimal fallback behavior to avoid breaking older code paths.
        """
        # Temporary safe fallback (single episode test)
        episode_number = 1130

        return [
            (
                episode_number,
                self.build_episode_url(episode_number),
            )
        ]