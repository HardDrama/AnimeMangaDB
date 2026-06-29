from scraper.providers.base_provider import BaseProvider


class FandomProvider(BaseProvider):
    """
    Provider implementation for Fandom wikis.
    """

    def build_episode_url(self, episode_number: int) -> str:
        return (
            self.config.base_url
            + self.config.episode_path.format(
                episode=episode_number
            )
        )