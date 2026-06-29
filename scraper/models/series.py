from pydantic import BaseModel, HttpUrl

class SeriesData(BaseModel):
    title: str

    fantom_url: HttpUrl

    language: str = "en"

    active: bool = True