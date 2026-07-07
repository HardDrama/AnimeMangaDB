from dataclasses import dataclass


@dataclass(slots=True)
class MetadataRepairApplicationResult:
    applied: int = 0
    skipped: int = 0