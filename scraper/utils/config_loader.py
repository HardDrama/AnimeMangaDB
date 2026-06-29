import json
from pathlib import Path

from scraper.models import ProviderConfig


def load_provider_config(path: str) -> ProviderConfig:
    data = json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )

    return ProviderConfig.model_validate(data)