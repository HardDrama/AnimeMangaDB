from scraper.database.models import Anime, Episode
from scraper.database.session import SessionLocal


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
            .all()
        )

        total = len(episodes)

        missing_titles = [
            episode
            for episode in episodes
            if not episode.episode_title
            or episode.episode_title
            == f"Episode {episode.episode_number}"
        ]

        missing_arcs = [
            episode
            for episode in episodes
            if not episode.arc
        ]

        print("Scope v2 Database Audit")
        print("-----------------------")
        print(f"Anime: {anime.title}")
        print()
        print(f"Episodes Checked : {total}")
        print(f"Missing Titles   : {len(missing_titles)}")
        print(f"Missing Arcs     : {len(missing_arcs)}")

        if missing_titles:
            print()
            print("Episodes Missing Titles")
            print("-----------------------")
            for episode in missing_titles[:25]:
                print(f"Episode {episode.episode_number}")

        if missing_arcs:
            print()
            print("Episodes Missing Arcs")
            print("---------------------")
            for episode in missing_arcs[:25]:
                print(f"Episode {episode.episode_number}")

    finally:
        session.close()


if __name__ == "__main__":
    main()