from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository


def main():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_list = repo.list_anime()

        print("Missing Arc Report")
        print("------------------")

        for anime in anime_list:
            episodes = repo.list_episodes_for_anime(anime.id)

            missing_arcs = [
                episode
                for episode in episodes
                if not episode.arc
            ]

            print()
            print(f"Anime: {anime.title}")
            print(f"Missing arcs: {len(missing_arcs)}")

            for episode in missing_arcs[:10]:
                print(
                    f"- Episode {episode.episode_number}: "
                    f"{episode.episode_title}"
                )

    finally:
        session.close()


if __name__ == "__main__":
    main()