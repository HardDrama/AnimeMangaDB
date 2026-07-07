from scraper.database.models import Episode
from scraper.database.session import SessionLocal

from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)
from scraper.services.metadata_comparison_service import (
    MetadataComparisonService,
)


def main():
    session = SessionLocal()

    try:
        episode = (
            session.query(Episode)
            .order_by(Episode.id)
            .first()
        )

        if episode is None:
            print("No episodes found in database.")
            return

        service = EpisodeMetadataService()
        metadata = service.get_metadata(episode)

        comparison_service = MetadataComparisonService()

        print("Episode Metadata Comparison")
        print("---------------------------")
        print(f"Episode ID: {episode.id}")
        print(f"Episode Number: {episode.episode_number}")
        print()

        print("Current Database")
        print("----------------")
        print(f"Title      : {episode.episode_title}")
        print(f"Arc        : {episode.arc}")
        print(f"Source URL : {episode.source_url}")
        print()

        print("Live Metadata")
        print("-------------")
        print(f"Title      : {metadata.title}")
        print(f"Arc        : {metadata.arc}")
        print(f"Source URL : {metadata.source_url}")
        print()

        comparison = comparison_service.compare(
            episode,
            metadata,
        )

        if comparison.has_changes:
            print("Differences")
            print("-----------")
            print(
                f"{len(comparison.differences)} of 3 fields differ."
            )
            print()

            for difference in comparison.differences:
                print(
                    difference.field.replace("_", " ").title()
                )
                print(
                    f"  Current : {difference.current_value}"
                )
                print(
                    f"  Live    : {difference.live_value}"
                )
                print()
        else:
            print("Differences")
            print("-----------")
            print("All 3 metadata fields match.")

    finally:
        session.close()


if __name__ == "__main__":
    main()