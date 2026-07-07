from scraper.database.models import Anime, Episode
from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)


MAX_EPISODES = 10


def main():
    session = SessionLocal()

    try:
        anime = (
            session.query(Anime)
            .order_by(Anime.id)
            .first()
        )

        if anime is None:
            print("No anime found.")
            return

        episodes = (
            session.query(Episode)
            .filter(Episode.anime_id == anime.id)
            .order_by(Episode.episode_number)
            .limit(MAX_EPISODES)
            .all()
        )

        service = EpisodeMetadataService()

        checked = 0
        matching = 0
        different = 0

        print("Series Metadata Comparison")
        print("--------------------------")
        print(f"Anime: {anime.title}")
        print()

        for episode in episodes:
            checked += 1

            metadata = service.get_metadata(episode)

            current_title = episode.episode_title
            current_arc = episode.arc
            current_source = (
                str(episode.source_url)
                if episode.source_url
                else None
            )

            live_source = (
                str(metadata.source_url)
                if metadata.source_url
                else None
            )

            changes = []

            if current_title != metadata.title:
                changes.append("Title")

            if current_arc != metadata.arc:
                changes.append("Arc")

            if current_source != live_source:
                changes.append("Source URL")

            if changes:
                different += 1

                print(
                    f"Episode {episode.episode_number}: "
                    + ", ".join(changes)
                )
            else:
                matching += 1

        print()
        print("Summary")
        print("-------")
        print(f"Episodes Checked : {checked}")
        print(f"Up-to-Date       : {matching}")
        print(f"Different        : {different}")

    finally:
        session.close()


if __name__ == "__main__":
    main()