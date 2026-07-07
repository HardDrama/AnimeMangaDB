from scraper.models.metadata_repair_application_result import (
    MetadataRepairApplicationResult,
)


class MetadataRepairApplicationService:
    """
    Applies metadata repair plans to database records.
    """

    def apply(
        self,
        episode,
        repair_plan,
        session=None,
        commit: bool = False,
    ):
        if commit and session is None:
            raise ValueError(
                "A database session is required when commit=True."
            )

        result = MetadataRepairApplicationResult()

        try:
            for repair in repair_plan.repairs:
                if repair.field == "title":
                    episode.episode_title = repair.new_value
                    result.applied += 1

                elif repair.field == "arc":
                    episode.arc = repair.new_value
                    result.applied += 1

                else:
                    result.skipped += 1

            result.committed = commit

            return result

        except Exception:
            if session is not None:
                session.rollback()

            raise