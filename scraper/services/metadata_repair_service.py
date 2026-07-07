from scraper.models.metadata_repair import (
    MetadataRepair,
)
from scraper.models.metadata_repair_plan import (
    MetadataRepairPlan,
)
from scraper.services.metadata_comparison_service import (
    MetadataComparisonService,
)


class MetadataRepairService:
    """
    Converts metadata comparison results
    into repair plans.
    """

    def __init__(
        self,
        comparison_service: MetadataComparisonService | None = None,
    ):
        self.comparison_service = (
            comparison_service
            or MetadataComparisonService()
        )

    def build_repair_plan(
        self,
        episode,
        metadata,
    ) -> MetadataRepairPlan:
        comparison = self.comparison_service.compare(
            episode,
            metadata,
        )

        plan = MetadataRepairPlan()

        for difference in comparison.differences:
            plan.repairs.append(
                MetadataRepair(
                    field=difference.field,
                    current_value=difference.current_value,
                    new_value=difference.live_value,
                )
            )

        return plan