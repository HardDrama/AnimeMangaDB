import argparse

from scraper.database.models import Episode
from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)
from scraper.services.metadata_repair_service import (
    MetadataRepairService,
)


def main():
    parser = argparse.ArgumentParser(
        description="Preview proposed metadata repairs."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Maximum episodes to preview.",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply repairs instead of previewing them.",
    )

    args = parser.parse_args()

    session = SessionLocal()

    try:
        episodes = (
            session.query(Episode)
            .order_by(Episode.id)
            .limit(args.limit)
            .all()
        )

        if not episodes:
            print("No episodes found.")
            return

        metadata_service = EpisodeMetadataService()
        repair_service = MetadataRepairService()

        if args.apply:
            print("Metadata Repair Apply")
            print("---------------------")
            print("Apply mode is not implemented yet.")
            print("No database changes will be made.")
        else:
            print("Metadata Repair Preview")
            print("-----------------------")

        episodes_with_repairs = 0
        total_repairs = 0

        for episode in episodes:
            metadata = metadata_service.get_metadata(episode)

            plan = repair_service.build_repair_plan(
                episode,
                metadata,
            )

            print()
            print(f"Episode {episode.episode_number}")
            print("-" * 20)

            if not plan.has_repairs:
                print("No repairs needed.")
                continue

            print(f"{len(plan.repairs)} repair(s) proposed.")
            episodes_with_repairs += 1
            total_repairs += len(plan.repairs)
            print()

            for repair in plan.repairs:
                print(repair.field.replace("_", " ").title())
                print(f"  Current : {repair.current_value}")
                print(f"  New     : {repair.new_value}")
                print()

        print()
        print("Summary")
        print("-------")
        print(f"Episodes Checked      : {len(episodes)}")
        print(f"Episodes With Repairs : {episodes_with_repairs}")
        print(f"Total Proposed Repairs: {total_repairs}")

    finally:
        session.close()


if __name__ == "__main__":
    main()