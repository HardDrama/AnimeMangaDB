class ScraperPipeline:
    def __init__(
        self,
        config,
        provider,
        client,
        extractor,
        repo,
    ):
        self.config = config
        self.provider = provider
        self.client = client
        self.extractor = extractor
        self.repo = repo

    def scrape_episode(
        self,
        episode_number: int,
        episode_url: str | None = None,
    ) -> dict:
        url = episode_url or self.provider.build_episode_url(
            episode_number
        )

        html = self.client.fetch(url)

        episode_data = self.extractor.parse(
            html=html,
            episode_number=episode_number,
            source_url=url,
        )

        anime = self.repo.get_or_create_anime(
            title=self.config.series,
            provider="fandom",
            base_url=self.config.base_url,
        )

        saved_episode = self.repo.create_episode(
            anime=anime,
            data=episode_data,
        )

        chapter_numbers = []

        if episode_data.manga_start is not None:
            if episode_data.manga_end is None:
                chapter_numbers = [episode_data.manga_start]
            else:
                chapter_numbers = list(
                    range(
                        episode_data.manga_start,
                        episode_data.manga_end + 1,
                    )
                )

        if self.repo.chapter_mappings_need_update(
            episode=saved_episode,
            chapter_numbers=chapter_numbers,
        ):
            self.repo.replace_episode_chapters(
                episode=saved_episode,
                chapter_numbers=chapter_numbers,
            )

        if episode_data.manga_start is None:
            chapter_display = "No chapter mapping found"
        else:
            chapter_display = (
                f"{episode_data.manga_start} → {episode_data.manga_end}"
            )

        print(f"Episode ID: {saved_episode.id}")
        print(f"Title: {saved_episode.episode_title}")
        print(f"Chapters: {chapter_display}")

        return {
            "episode_number": episode_number,
            "has_chapters": episode_data.manga_start is not None,
        }