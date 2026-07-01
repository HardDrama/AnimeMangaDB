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
    
    def get_episode_list(self) -> list[tuple[int, str]]:
        """
        Return a list of (episode_number, url) pairs.
        For now, this is a placeholder implementation.
        """

        episode_number = 1130

        return [
            (
                episode_number,
                self.build_episode_url(episode_number),
            )
        ]