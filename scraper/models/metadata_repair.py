from dataclasses import dataclass


@dataclass(slots=True)
class MetadataRepair:
    field: str
    current_value: str | None
    new_value: str | None