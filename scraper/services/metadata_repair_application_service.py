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
        return MetadataRepairApplicationResult(
            applied=0,
            skipped=len(repair_plan.repairs),
        )