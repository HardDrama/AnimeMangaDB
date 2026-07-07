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
        metadata = self.metadata_service.get_metadata(
            episode
        )

        if metadata.title:
            return metadata.title

        return propose_episode_title(episode)