def propose_episode_title(episode):
    """
    Returns a proposed replacement title for an episode.

    Currently this is only a placeholder.
    Later versions will retrieve the title from the
    scraper/provider.
    """

    if (
        episode.episode_title
        == f"Episode {episode.episode_number}"
    ):
        return "(lookup required)"

    return episode.episode_title