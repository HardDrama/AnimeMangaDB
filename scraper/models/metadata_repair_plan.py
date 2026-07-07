from dataclasses import dataclass, field

from scraper.models.metadata_repair import (
    MetadataRepair,
)


@dataclass(slots=True)
class MetadataRepairPlan:
    repairs: list[MetadataRepair] = field(
        default_factory=list
    )

    @property
    def has_repairs(self) -> bool:
        return bool(self.repairs)