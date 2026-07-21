from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scraper.database.models_shared_manga import (
    Episode,
    EpisodeChapter,
    SharedMangaBase,
)
from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository,
)
from scraper.services.shared_manga_api_service import (
    SharedMangaApiService,
)


def create_service():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    SharedMangaBase.metadata.create_all(
        bind=engine,
    )

    session = Session(engine)
    episode_repository = EpisodeRepository(
        session
    )
    manga_repository = MangaRepository(
        session
    )

    service = SharedMangaApiService(
        episode_repository=episode_repository,
        manga_repository=manga_repository,
    )

    return (
        session,
        episode_repository,
        manga_repository,
        service,
    )


def seed_shared_naruto(
    session,
    episode_repository,
    manga_repository,
):
    manga = manga_repository.get_or_create_manga(
        title="Naruto",
        provider="fandom",
        base_url="https://naruto.fandom.com",
    )

    naruto = episode_repository.get_or_create_anime(
        title="Naruto",
        provider="fandom",
        base_url="https://naruto.fandom.com",
        manga_id=manga.id,
    )

    shippuden = (
        episode_repository.get_or_create_anime(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )
    )

    manga_repository.create_or_update_chapter_metadata(
        manga=manga,
        chapter_number=245,
        chapter_title="Homecoming",
        manga_arc="Kazekage Rescue Mission",
        source_url=(
            "https://naruto.fandom.com/wiki/"
            "Chapter_245"
        ),
        last_updated=datetime(
            2026,
            7,
            20,
        ),
    )

    shippuden_episode = Episode(
        anime_id=shippuden.id,
        episode_number=1,
        episode_title="Homecoming",
        arc="Kazekage Rescue Mission",
        source_url=(
            "https://naruto.fandom.com/wiki/"
            "Naruto:_Shippuden_Episode_1"
        ),
        last_updated=datetime(
            2026,
            7,
            20,
        ),
    )

    session.add(shippuden_episode)
    session.commit()
    session.refresh(shippuden_episode)

    session.add(
        EpisodeChapter(
            episode_id=shippuden_episode.id,
            chapter_number=245,
        )
    )
    session.commit()

    return manga, naruto, shippuden


def test_series_responses_share_chapter_count():
    (
        session,
        episode_repository,
        manga_repository,
        service,
    ) = create_service()

    with session:
        seed_shared_naruto(
            session,
            episode_repository,
            manga_repository,
        )

        series = service.list_series()

        counts = {
            item.title: item.chapter_count
            for item in series
        }

        assert counts == {
            "Naruto": 1,
            "Naruto Shippuden": 1,
        }


def test_anime_chapter_routes_resolve_shared_metadata():
    (
        session,
        episode_repository,
        manga_repository,
        service,
    ) = create_service()

    with session:
        _, naruto, shippuden = seed_shared_naruto(
            session,
            episode_repository,
            manga_repository,
        )

        naruto_chapter = (
            service.get_chapter_for_anime(
                anime_id=naruto.id,
                chapter_number=245,
            )
        )

        shippuden_chapter = (
            service.get_chapter_for_anime(
                anime_id=shippuden.id,
                chapter_number=245,
            )
        )

        assert naruto_chapter is not None
        assert shippuden_chapter is not None
        assert naruto_chapter.chapter_title == (
            "Homecoming"
        )
        assert shippuden_chapter.chapter_title == (
            "Homecoming"
        )


def test_anime_chapter_episode_lookup_stays_anime_scoped():
    (
        session,
        episode_repository,
        manga_repository,
        service,
    ) = create_service()

    with session:
        _, naruto, shippuden = seed_shared_naruto(
            session,
            episode_repository,
            manga_repository,
        )

        naruto_episodes = (
            service.list_episodes_for_anime_chapter(
                anime_id=naruto.id,
                chapter_number=245,
            )
        )

        shippuden_episodes = (
            service.list_episodes_for_anime_chapter(
                anime_id=shippuden.id,
                chapter_number=245,
            )
        )

        assert naruto_episodes == []
        assert shippuden_episodes is not None
        assert len(shippuden_episodes) == 1
        assert (
            shippuden_episodes[0].anime_title
            == "Naruto Shippuden"
        )


def test_arc_summary_combines_episode_and_manga_data():
    (
        session,
        episode_repository,
        manga_repository,
        service,
    ) = create_service()

    with session:
        _, _, shippuden = seed_shared_naruto(
            session,
            episode_repository,
            manga_repository,
        )

        arcs = service.list_arcs_for_anime(
            shippuden.id
        )

        assert arcs is not None
        assert len(arcs) == 1
        assert arcs[0].name == (
            "Kazekage Rescue Mission"
        )
        assert arcs[0].episode_count == 1
        assert arcs[0].chapter_count == 1


def test_search_expands_shared_metadata_per_anime():
    (
        session,
        episode_repository,
        manga_repository,
        service,
    ) = create_service()

    with session:
        seed_shared_naruto(
            session,
            episode_repository,
            manga_repository,
        )

        response = service.search("Homecoming")

        assert len(response.episodes) == 1
        assert len(response.chapter_metadata) == 2

        assert {
            item.anime_title
            for item
            in response.chapter_metadata
        } == {
            "Naruto",
            "Naruto Shippuden",
        }


def test_missing_series_and_chapter_return_none():
    (
        session,
        _,
        _,
        service,
    ) = create_service()

    with session:
        assert service.get_series(999) is None
        assert (
            service.list_chapters_for_anime(
                999
            )
            is None
        )
        assert (
            service.get_chapter_for_anime(
                anime_id=999,
                chapter_number=1,
            )
            is None
        )
