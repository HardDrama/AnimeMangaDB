from datetime import datetime

from scraper.database.base import Base
from scraper.database.models import Anime
from scraper.database.models import EpisodeChapter
from scraper.models.episode import EpisodeData
from scraper.repositories.episode_repository import EpisodeRepository

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


def create_test_session():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    TestingSession = sessionmaker(bind=engine)

    return TestingSession()


def test_get_or_create_anime_creates_anime():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    assert anime.id is not None
    assert anime.title == "One Piece"


def test_get_or_create_anime_reuses_existing_anime():
    session = create_test_session()
    repo = EpisodeRepository(session)

    first = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    second = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    assert first.id == second.id

def make_episode_data() -> EpisodeData:
    return EpisodeData(
        anime_title="One Piece",
        episode_number=1130,
        episode_title="Episode 1130",
        manga_start=1096,
        manga_end=1096,
        arc=None,
        source_url="https://onepiece.fandom.com/wiki/Episode_1130",
    )

def make_arc_episode_data(
    episode_number: int,
    arc: str | None,
) -> EpisodeData:
    return EpisodeData(
        anime_title="Test Anime",
        episode_number=episode_number,
        episode_title=(
            f"Episode {episode_number}"
        ),
        manga_start=None,
        manga_end=None,
        arc=arc,
        source_url=(
            "https://example.com/wiki/"
            f"Episode_{episode_number}"
        ),
    )


def test_create_episode_creates_episode():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    assert episode.id is not None
    assert episode.episode_number == 1130
    assert episode.episode_title == "Episode 1130"


def test_create_episode_reuses_existing_episode():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    first = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    second = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    assert first.id == second.id

def test_add_episode_chapters_creates_chapter_link():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    stmt = select(EpisodeChapter).where(
        EpisodeChapter.episode_id == episode.id
    )

    chapters = session.execute(stmt).scalars().all()

    assert len(chapters) == 1
    assert chapters[0].chapter_number == 1096


def test_add_episode_chapters_does_not_duplicate_links():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    stmt = select(EpisodeChapter).where(
        EpisodeChapter.episode_id == episode.id
    )

    chapters = session.execute(stmt).scalars().all()

    assert len(chapters) == 1

def test_episode_needs_update_returns_false_when_data_matches():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    assert repo.episode_needs_update(
        episode=episode,
        data=make_episode_data(),
    ) is False


def test_episode_needs_update_returns_true_when_title_changes():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    changed_data = make_episode_data()
    changed_data.episode_title = "Updated Episode 1130"

    assert repo.episode_needs_update(
        episode=episode,
        data=changed_data,
    ) is True

def test_create_episode_updates_existing_episode_when_data_changes():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    original = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    changed_data = make_episode_data()
    changed_data.episode_title = "Updated Episode 1130"

    updated = repo.create_episode(
        anime=anime,
        data=changed_data,
    )

    assert original.id == updated.id
    assert updated.episode_title == "Updated Episode 1130"

def test_chapter_mappings_need_update_returns_false_when_chapters_match():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    assert repo.chapter_mappings_need_update(
        episode=episode,
        chapter_numbers=[1096],
    ) is False


def test_chapter_mappings_need_update_returns_true_when_chapters_change():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    assert repo.chapter_mappings_need_update(
        episode=episode,
        chapter_numbers=[1097],
    ) is True

def test_replace_episode_chapters_replaces_old_mappings():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="One Piece",
        provider="fandom",
        base_url="https://onepiece.fandom.com",
    )

    episode = repo.create_episode(
        anime=anime,
        data=make_episode_data(),
    )

    repo.add_episode_chapters(
        episode=episode,
        chapter_numbers=[1096],
    )

    repo.replace_episode_chapters(
        episode=episode,
        chapter_numbers=[1097],
    )

    chapters = repo.get_chapter_numbers_for_episode(episode)

    assert chapters == [1097]

def test_get_episodes_by_anime_and_chapter_limits_results_to_anime():
    session = create_test_session()
    repository = EpisodeRepository(
        session
    )

    one_piece = (
        repository.get_or_create_anime(
            title="One Piece",
            provider="fandom",
            base_url=(
                "https://onepiece.fandom.com"
            ),
        )
    )

    naruto = (
        repository.get_or_create_anime(
            title="Naruto",
            provider="fandom",
            base_url=(
                "https://naruto.fandom.com"
            ),
        )
    )

    one_piece_data = make_episode_data()

    one_piece_episode = (
        repository.create_episode(
            anime=one_piece,
            data=one_piece_data,
        )
    )

    naruto_data = EpisodeData(
        anime_title="Naruto",
        episode_number=500,
        episode_title="Naruto Episode 500",
        manga_start=1096,
        manga_end=1096,
        arc=None,
        source_url=(
            "https://naruto.fandom.com/"
            "wiki/Episode_500"
        ),
    )

    naruto_episode = (
        repository.create_episode(
            anime=naruto,
            data=naruto_data,
        )
    )

    repository.add_episode_chapters(
        episode=one_piece_episode,
        chapter_numbers=[1096],
    )

    repository.add_episode_chapters(
        episode=naruto_episode,
        chapter_numbers=[1096],
    )

    results = (
        repository
        .get_episodes_by_anime_and_chapter(
            anime_id=one_piece.id,
            chapter_number=1096,
        )
    )

    assert [
        episode.id
        for episode in results
    ] == [
        one_piece_episode.id
    ]

    assert all(
        episode.anime_id == one_piece.id
        for episode in results
    )

def test_list_arc_summaries_groups_episode_and_manga_arcs():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="Test Anime",
        provider="test",
        base_url="https://example.com",
    )

    repo.create_episode(
        anime=anime,
        data=make_arc_episode_data(
            episode_number=1,
            arc="Romance Dawn",
        ),
    )

    repo.create_episode(
        anime=anime,
        data=make_arc_episode_data(
            episode_number=2,
            arc="Romance Dawn",
        ),
    )

    repo.create_episode(
        anime=anime,
        data=make_arc_episode_data(
            episode_number=3,
            arc="Orange Town",
        ),
    )

    repo.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
        source_url=(
            "https://example.com/wiki/"
            "Chapter_1"
        ),
        last_updated=datetime.now(),
    )

    repo.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=2,
        chapter_title=(
            "They Call Him Straw Hat Luffy"
        ),
        manga_arc="Romance Dawn Arc",
        source_url=(
            "https://example.com/wiki/"
            "Chapter_2"
        ),
        last_updated=datetime.now(),
    )

    repo.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=3,
        chapter_title="Enter Zolo",
        manga_arc="Orange Town Arc",
        source_url=(
            "https://example.com/wiki/"
            "Chapter_3"
        ),
        last_updated=datetime.now(),
    )

    results = repo.list_arc_summaries(
        anime.id
    )

    assert results == [
        {
            "name": "Romance Dawn",
            "episode_arc": "Romance Dawn",
            "manga_arc": "Romance Dawn Arc",
            "episode_count": 2,
            "chapter_count": 2,
        },
        {
            "name": "Orange Town",
            "episode_arc": "Orange Town",
            "manga_arc": "Orange Town Arc",
            "episode_count": 1,
            "chapter_count": 1,
        },
    ]

    session.close()

def test_list_arc_summaries_ignores_missing_arc_values():
    session = create_test_session()
    repo = EpisodeRepository(session)

    anime = repo.get_or_create_anime(
        title="Test Anime",
        provider="test",
        base_url="https://example.com",
    )

    repo.create_episode(
        anime=anime,
        data=make_arc_episode_data(
            episode_number=1,
            arc=None,
        ),
    )

    repo.create_episode(
        anime=anime,
        data=make_arc_episode_data(
            episode_number=2,
            arc="",
        ),
    )

    repo.create_episode(
        anime=anime,
        data=make_arc_episode_data(
            episode_number=3,
            arc="Valid Arc",
        ),
    )

    repo.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=1,
        chapter_title="Missing Arc Chapter",
        manga_arc=None,
        source_url=(
            "https://example.com/wiki/"
            "Chapter_1"
        ),
        last_updated=datetime.now(),
    )

    repo.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=2,
        chapter_title="Blank Arc Chapter",
        manga_arc="",
        source_url=(
            "https://example.com/wiki/"
            "Chapter_2"
        ),
        last_updated=datetime.now(),
    )

    repo.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=3,
        chapter_title="Valid Arc Chapter",
        manga_arc="Valid Arc",
        source_url=(
            "https://example.com/wiki/"
            "Chapter_3"
        ),
        last_updated=datetime.now(),
    )

    results = repo.list_arc_summaries(
        anime.id
    )

    assert results == [
        {
            "name": "Valid Arc",
            "episode_arc": "Valid Arc",
            "manga_arc": "Valid Arc",
            "episode_count": 1,
            "chapter_count": 1,
        },
    ]

    session.close()