from scraper.models.metadata_repair_application_result import (
    MetadataRepairApplicationResult,
)


class MetadataRepairApplicationService:
    """
    Applies metadata repair plans to database records.

    This service is intentionally non-destructive for now.
    """

    def apply(
        self,
        episode,
        repair_plan,
    ):
        result = MetadataRepairApplicationResult()

        for repair in repair_plan.repairs:
            if repair.field == "title":
                episode.episode_title = repair.new_value
                result.applied += 1

            elif repair.field == "arc":
                episode.arc = repair.new_value
                result.applied += 1

            else:
                result.skipped += 1

        return result