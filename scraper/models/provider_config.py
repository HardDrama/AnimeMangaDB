from pydantic import BaseModel


class SelectorConfig(BaseModel):
    title: str


class ProviderConfig(BaseModel):
    series: str
    base_url: str
    episode_path: str
    selectors: SelectorConfig