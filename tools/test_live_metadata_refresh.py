from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)


def main():
    session = SessionLocal()

    try:
        episode = (
            session.query
        )

        # Pick the first episode in the database.
        from scraper.database.models import Episode

        episode = (
            session.query(Episode)
            .order_by(Episode.id)
            .first()
        )

        if episode is None:
            print("No episodes found in database.")
            return

        print("Live Metadata Refresh Smoke Test")
        print("--------------------------------")
        print(f"Episode ID: {episode.id}")
        print(f"Episode Number: {episode.episode_number}")
        print(f"Current Title: {episode.episode_title}")

        service = EpisodeMetadataService()

        metadata = service.get_metadata(episode)

        print()
        print("Retrieved Metadata")
        print("------------------")
        print(f"Title: {metadata.title}")
        print(f"Arc: {metadata.arc}")
        print(f"Source URL: {metadata.source_url}")

    finally:
        session.close()


if __name__ == "__main__":
    main()