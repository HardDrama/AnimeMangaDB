from tools.repair_helpers import propose_episode_title


class MetadataProposalService:
    """
    Generates proposed metadata improvements for existing records.
    """

    def propose_episode_title(
        self,
        episode,
    ):
        return propose_episode_title(episode)