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
        return {
            "applied": 0,
            "skipped": len(repair_plan.repairs),
        }