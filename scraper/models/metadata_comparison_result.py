from dataclasses import dataclass, field

from scraper.models.metadata_difference import (
    MetadataDifference,
)


@dataclass(slots=True)
class MetadataComparisonResult:
    differences: list[MetadataDifference] = field(
        default_factory=list
    )

    @property
    def has_changes(self) -> bool:
        return bool(self.differences)