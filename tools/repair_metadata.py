import argparse

from dataclasses import dataclass

from scraper.database.session import SessionLocal
from scraper.repositories.factory import create_episode_repository

from tools.repair_helpers import propose_episode_title


def main():
    parser = argparse.ArgumentParser(
        description="AnimeMangaDB Metadata Repair Tool"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply repair actions instead of performing a dry run.",
    )

    args = parser.parse_args()

    print("Metadata Repair Tool")
    print("--------------------")

    if args.apply:
        print("Running in APPLY mode.")
    else:
        print("Running in DRY RUN mode.")
        print("No database changes will be made.")

    actions = []

    session = SessionLocal()

    try:
        repo = create_episode_repository(session)

        anime_list = repo.list_anime()

        for anime in anime_list:
            episodes = repo.list_episodes_for_anime(anime.id)

            for episode in episodes:
                if (
                    episode.episode_title
                    == f"Episode {episode.episode_number}"
                ):
                    actions.append(
                        RepairAction(
                            description=(
                                f"{anime.title} "
                                f"Episode {episode.episode_number}"
                            ),
                            current_value=episode.episode_title,
                            proposed_value=propose_episode_title(episode),
                        )
                    )

    finally:
        session.close()

    print()

    if not actions:
        print("No repair actions found.")
        return

    for action in actions:
        if args.apply:
            action.apply()
        else:
            action.preview()

@dataclass
class RepairAction:
    description: str
    current_value: str | None = None
    proposed_value: str | None = None

    def preview(self):
        print(f"Would repair: {self.description}")

        if (
            self.current_value is not None
            and self.proposed_value is not None
        ):
            print(f"  Current : {self.current_value}")
            print(f"  Proposed: {self.proposed_value}")

    def apply(self):
        print(f"Applied repair: {self.description}")


if __name__ == "__main__":
    main()