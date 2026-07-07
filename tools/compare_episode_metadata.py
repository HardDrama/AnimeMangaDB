from scraper.database.models import Episode
from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
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

        print("Differences")
        print("-----------")

        differences = []

        total_fields = 3

        if episode.episode_title != metadata.title:
            differences.append("Title")

        if episode.arc != metadata.arc:
            differences.append("Arc")

        if episode.source_url != metadata.source_url:
            differences.append("Source URL")

        if differences:
            print(
                f"{len(differences)} of "
                f"{total_fields} fields differ."
            )
            print()

            for field in differences:
                print(f"- {field}")
        else:
            print(
                f"All {total_fields} metadata fields match."
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()