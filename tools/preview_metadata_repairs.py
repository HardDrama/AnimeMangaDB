import argparse

from scraper.database.models import Episode
from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)
from scraper.services.metadata_repair_service import (
    MetadataRepairService,
)
from scraper.services.metadata_repair_application_service import (
    MetadataRepairApplicationService,
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

    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm that repairs should be applied.",
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
        application_service = (
            MetadataRepairApplicationService()
        )

        if args.apply:
            print("Metadata Repair Tool")
            print("--------------------")
            print("Running in APPLY mode.")

            if not args.yes:
                print("Missing confirmation flag: --yes")
                print("No database changes will be made.")
                return

            print("Apply mode placeholder.")
            print("Repair plans will be passed to the application service.")
            print()
        else:
            print("Metadata Repair Tool")
            print("--------------------")
            print("Running in PREVIEW mode.")

        episodes_with_repairs = 0
        total_repairs = 0

        for episode in episodes:
            metadata = metadata_service.get_metadata(episode)

            plan = repair_service.build_repair_plan(
                episode,
                metadata,
            )

            if args.apply:
                result = application_service.apply(
                    episode,
                    plan,
                )

                print(
                    f"Application Result: "
                    f"{result.applied} applied, "
                    f"{result.skipped} skipped."
                )
                print(
                    f"Database Updated : {result.committed}"
                )
                print()

                continue

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