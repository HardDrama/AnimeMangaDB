from dataclasses import dataclass


@dataclass(slots=True)
class MetadataDifference:
    field: str
    current_value: str | None
    live_value: str | None