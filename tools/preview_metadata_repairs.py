from scraper.database.models import Episode
from scraper.database.session import SessionLocal
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)
from scraper.services.metadata_repair_service import (
    MetadataRepairService,
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
            print("No episodes found.")
            return

        metadata_service = EpisodeMetadataService()
        repair_service = MetadataRepairService()

        metadata = metadata_service.get_metadata(
            episode
        )

        plan = repair_service.build_repair_plan(
            episode,
            metadata,
        )

        print("Metadata Repair Preview")
        print("-----------------------")
        print(f"Episode {episode.episode_number}")
        print()

        if not plan.has_repairs:
            print("No repairs needed.")
            return

        print(
            f"{len(plan.repairs)} repair(s) proposed."
        )
        print()

        for repair in plan.repairs:
            print(
                repair.field.replace("_", " ").title()
            )
            print(
                f"  Current : {repair.current_value}"
            )
            print(
                f"  New     : {repair.new_value}"
            )
            print()

    finally:
        session.close()


if __name__ == "__main__":
    main()