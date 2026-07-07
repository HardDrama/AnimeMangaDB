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

            if "Title" in differences:
                print("Title")
                print(f"  Current : {episode.episode_title}")
                print(f"  Live    : {metadata.title}")
                print()

            if "Arc" in differences:
                print("Arc")
                print(f"  Current : {episode.arc}")
                print(f"  Live    : {metadata.arc}")
                print()

            if "Source URL" in differences:
                print("Source URL")
                print(f"  Current : {episode.source_url}")
                print(f"  Live    : {metadata.source_url}")
                print()
        else:
            print(
                f"All {total_fields} metadata fields match."
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()