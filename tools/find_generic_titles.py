from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository


def main():
    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_list = repo.list_anime()

        print("Generic Episode Title Report")
        print("----------------------------")

        for anime in anime_list:
            episodes = repo.list_episodes_for_anime(anime.id)

            generic_titles = [
                episode
                for episode in episodes
                if episode.episode_title
                == f"Episode {episode.episode_number}"
            ]

            print()
            print(f"Anime: {anime.title}")
            print(f"Generic titles: {len(generic_titles)}")

            for episode in generic_titles[:10]:
                print(
                    f"- Episode {episode.episode_number}: "
                    f"{episode.episode_title}"
                )

    finally:
        session.close()


if __name__ == "__main__":
    main()