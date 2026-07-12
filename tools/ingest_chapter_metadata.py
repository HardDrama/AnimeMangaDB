import argparse

from scraper.core.browser_client import BrowserClient
from scraper.database.session import SessionLocal
from scraper.providers.chapter_metadata_factory import (
    create_chapter_metadata_provider,
)
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)
from scraper.services.chapter_metadata_ingestion_service import (
    ChapterMetadataIngestionService,
)
from scraper.services.chapter_url_discovery_service import (
    ChapterUrlDiscoveryService,
)
from scraper.utils.config_loader import load_provider_config


SERIES_CONFIGS = {
    "One Piece": "configs/fandom/one_piece.json",
    "Naruto": "configs/fandom/naruto.json",
}


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Discover, extract, and save metadata "
            "for one manga chapter."
        )
    )

    parser.add_argument(
        "--anime",
        required=True,
        help="Anime title associated with the manga series.",
    )

    parser.add_argument(
        "--chapter",
        type=int,
        required=True,
        help="Manga chapter number to ingest.",
    )

    args = parser.parse_args()

    config_path = SERIES_CONFIGS.get(
        args.anime
    )

    if config_path is None:
        print(
            f'No chapter metadata configuration '
            f'found for: "{args.anime}"'
        )
        return

    session = SessionLocal()

    try:
        repository = EpisodeRepository(
            session
        )

        anime = repository.get_anime_by_title(
            args.anime
        )

        if anime is None:
            print(
                f'Anime not found in database: '
                f'"{args.anime}"'
            )
            return

        existing = repository.get_chapter_metadata(
            anime_id=anime.id,
            chapter_number=args.chapter,
        )

        config = load_provider_config(
            config_path
        )

        browser_client = BrowserClient()

        discovery_service = (
            ChapterUrlDiscoveryService(
                config=config,
                browser_client=browser_client,
            )
        )

        provider = create_chapter_metadata_provider(
            provider_name=anime.provider,
            config_path=config_path,
            browser_client=browser_client,
        )

        ingestion_service = (
            ChapterMetadataIngestionService(
                discovery_service=discovery_service,
                provider=provider,
                repository=repository,
            )
        )

        chapter = ingestion_service.ingest(
            anime=anime,
            chapter_number=args.chapter,
        )

        status = (
            "Inserted"
            if existing is None
            else "Updated"
        )

        print("Chapter Metadata Ingestion")
        print("--------------------------")
        print(f"Series : {anime.title}")
        print(f"Chapter: {chapter.chapter_number}")
        print(
            f"Title  : "
            f"{chapter.chapter_title or 'Not available'}"
        )
        print(
            f"Arc    : "
            f"{chapter.manga_arc or 'Not available'}"
        )
        print(
            f"Source : "
            f"{chapter.source_url or 'Not available'}"
        )
        print(f"Status : {status}")

    except Exception as error:
        print("Chapter metadata ingestion failed.")
        print(f"Reason: {error}")

    finally:
        session.close()


if __name__ == "__main__":
    main()