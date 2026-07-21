from scraper.api.schemas import (
    ArcSummaryResponse,
    ChapterMetadataResponse,
    ChapterMetadataSearchResponse,
    ChapterSearchResult,
    EpisodeResponse,
    SearchResponse,
    SeriesResponse,
)
from scraper.database.models import (
    Anime,
    ChapterMetadata,
    Episode,
)
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)
from scraper.repositories.manga_repository import (
    MangaRepository,
)


class SharedMangaApiService:
    """
    Production application service for the anime-centric REST API.

    The public API continues to expose anime routes while chapter
    metadata is resolved through each anime record's shared manga.
    """

    def __init__(
        self,
        episode_repository: EpisodeRepository,
        manga_repository: MangaRepository,
    ):
        self.episode_repository = episode_repository
        self.manga_repository = manga_repository

    @staticmethod
    def episode_response(
        episode: Episode,
        anime_title: str | None = None,
    ) -> EpisodeResponse:
        resolved_title = anime_title

        if resolved_title is None:
            resolved_title = episode.anime.title

        return EpisodeResponse(
            id=episode.id,
            anime_id=episode.anime_id,
            anime_title=resolved_title,
            episode_number=episode.episode_number,
            episode_title=episode.episode_title,
            title=episode.episode_title,
            arc=episode.arc,
            source_url=episode.source_url,
        )

    def series_response(
        self,
        anime: Anime,
    ) -> SeriesResponse:
        return SeriesResponse(
            id=anime.id,
            title=anime.title,
            provider=anime.provider,
            base_url=anime.base_url,
            episode_count=(
                self.episode_repository
                .count_episodes_for_anime(
                    anime.id
                )
            ),
            chapter_count=(
                self.manga_repository
                .count_chapters_for_anime(
                    anime
                )
            ),
        )

    @staticmethod
    def chapter_response(
        chapter: ChapterMetadata,
    ) -> ChapterMetadataResponse:
        return ChapterMetadataResponse(
            chapter_number=chapter.chapter_number,
            chapter_title=chapter.chapter_title,
            manga_arc=chapter.manga_arc,
            source_url=chapter.source_url,
            last_updated=chapter.last_updated,
        )

    def list_series(
        self,
    ) -> list[SeriesResponse]:
        return [
            self.series_response(anime)
            for anime
            in self.episode_repository.list_anime()
        ]

    def get_series(
        self,
        anime_id: int,
    ) -> SeriesResponse | None:
        anime = (
            self.episode_repository
            .get_anime_by_id(anime_id)
        )

        if anime is None:
            return None

        return self.series_response(anime)

    def list_episodes_for_anime(
        self,
        anime_id: int,
    ) -> list[EpisodeResponse] | None:
        anime = (
            self.episode_repository
            .get_anime_by_id(anime_id)
        )

        if anime is None:
            return None

        episodes = (
            self.episode_repository
            .list_episodes_for_anime(anime_id)
        )

        return [
            self.episode_response(
                episode,
                anime_title=anime.title,
            )
            for episode in episodes
        ]

    def list_chapters_for_anime(
        self,
        anime_id: int,
    ) -> list[ChapterMetadataResponse] | None:
        anime = (
            self.episode_repository
            .get_anime_by_id(anime_id)
        )

        if anime is None:
            return None

        chapters = (
            self.manga_repository
            .list_chapter_metadata_for_anime(
                anime
            )
        )

        return [
            self.chapter_response(chapter)
            for chapter in chapters
        ]

    def get_chapter_for_anime(
        self,
        anime_id: int,
        chapter_number: int,
    ) -> ChapterMetadataResponse | None:
        anime = (
            self.episode_repository
            .get_anime_by_id(anime_id)
        )

        if anime is None:
            return None

        chapter = (
            self.manga_repository
            .get_chapter_metadata_for_anime(
                anime=anime,
                chapter_number=chapter_number,
            )
        )

        if chapter is None:
            return None

        return self.chapter_response(chapter)

    def list_episodes_for_anime_chapter(
        self,
        anime_id: int,
        chapter_number: int,
    ) -> list[EpisodeResponse] | None:
        anime = (
            self.episode_repository
            .get_anime_by_id(anime_id)
        )

        if anime is None:
            return None

        chapter = (
            self.manga_repository
            .get_chapter_metadata_for_anime(
                anime=anime,
                chapter_number=chapter_number,
            )
        )

        if chapter is None:
            return None

        episodes = (
            self.episode_repository
            .get_episodes_by_anime_and_chapter(
                anime_id=anime_id,
                chapter_number=chapter_number,
            )
        )

        return [
            self.episode_response(
                episode,
                anime_title=anime.title,
            )
            for episode in episodes
        ]

    def list_episodes_for_chapter(
        self,
        chapter_number: int,
    ) -> list[EpisodeResponse]:
        episodes = (
            self.episode_repository
            .get_episodes_by_chapter(
                chapter_number
            )
        )

        return [
            self.episode_response(episode)
            for episode in episodes
        ]

    def list_arcs_for_anime(
        self,
        anime_id: int,
    ) -> list[ArcSummaryResponse] | None:
        anime = (
            self.episode_repository
            .get_anime_by_id(anime_id)
        )

        if anime is None:
            return None

        episode_arcs = (
            self.episode_repository
            .list_episode_arc_summaries(
                anime_id
            )
        )

        manga_arcs = (
            self.manga_repository
            .list_manga_arc_summaries(
                anime.manga_id
            )
        )

        summaries: dict[str, dict] = {}
        ordering: dict[str, tuple[int, int]] = {}

        for arc in episode_arcs:
            key = (
                self.episode_repository
                .normalize_arc_name(
                    arc["episode_arc"]
                )
            )

            summaries[key] = {
                "name": arc["name"],
                "episode_arc": (
                    arc["episode_arc"]
                ),
                "manga_arc": None,
                "episode_count": (
                    arc["episode_count"]
                ),
                "chapter_count": 0,
            }

            ordering[key] = (
                0,
                arc["first_episode"],
            )

        for arc in manga_arcs:
            key = (
                self.manga_repository
                .normalize_arc_name(
                    arc["manga_arc"]
                )
            )

            if key not in summaries:
                summaries[key] = {
                    "name": arc["name"],
                    "episode_arc": None,
                    "manga_arc": (
                        arc["manga_arc"]
                    ),
                    "episode_count": 0,
                    "chapter_count": (
                        arc["chapter_count"]
                    ),
                }

                ordering[key] = (
                    1,
                    arc["first_chapter"],
                )

                continue

            summaries[key]["manga_arc"] = (
                arc["manga_arc"]
            )
            summaries[key]["chapter_count"] = (
                arc["chapter_count"]
            )

        return [
            ArcSummaryResponse(
                **summaries[key]
            )
            for key in sorted(
                summaries,
                key=lambda item: ordering[item],
            )
        ]

    def search(
        self,
        query: str,
    ) -> SearchResponse:
        anime_results = (
            self.episode_repository
            .search_anime(query)
        )

        episode_results = (
            self.episode_repository
            .search_episodes(query)
        )

        metadata_results = (
            self.manga_repository
            .search_chapter_metadata(query)
        )

        chapter_results: list[
            ChapterSearchResult
        ] = []

        try:
            chapter_number = int(query)
        except ValueError:
            chapter_number = None

        if chapter_number is not None:
            chapter_episodes = (
                self.episode_repository
                .get_episodes_by_chapter(
                    chapter_number
                )
            )

            if chapter_episodes:
                chapter_results.append(
                    ChapterSearchResult(
                        chapter_number=chapter_number,
                        episodes=[
                            self.episode_response(
                                episode
                            )
                            for episode
                            in chapter_episodes
                        ],
                    )
                )

        metadata_responses: list[
            ChapterMetadataSearchResponse
        ] = []

        for chapter in metadata_results:
            for anime in chapter.manga.anime:
                metadata_responses.append(
                    ChapterMetadataSearchResponse(
                        anime_id=anime.id,
                        anime_title=anime.title,
                        chapter_number=(
                            chapter.chapter_number
                        ),
                        chapter_title=(
                            chapter.chapter_title
                        ),
                        manga_arc=chapter.manga_arc,
                        source_url=chapter.source_url,
                        last_updated=(
                            chapter.last_updated
                        ),
                    )
                )

        metadata_responses.sort(
            key=lambda item: (
                item.anime_title.casefold(),
                item.chapter_number,
            )
        )

        return SearchResponse(
            anime=[
                self.series_response(anime)
                for anime in anime_results
            ],
            episodes=[
                self.episode_response(episode)
                for episode in episode_results
            ],
            chapters=chapter_results,
            chapter_metadata=metadata_responses,
        )
