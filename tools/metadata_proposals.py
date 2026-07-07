from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)

from tools.repair_helpers import (
    propose_episode_title,
)


class MetadataProposalService:
    """
    Generates proposed metadata improvements.
    """

    def __init__(self):
        self.metadata_service = EpisodeMetadataService()

    def propose_episode_title(
        self,
        episode,
    ):
        fresh_title = self.metadata_service.get_episode_title(
            episode
        )

        if fresh_title:
            return fresh_title

        return propose_episode_title(episode)