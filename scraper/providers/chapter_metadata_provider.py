from abc import ABC, abstractmethod

from scraper.models.chapter_metadata import ChapterMetadata


class ChapterMetadataProvider(ABC):
    """
    Retrieves fresh metadata for a manga chapter.
    """

    @abstractmethod
    def get_chapter_metadata(
        self,
        chapter_number: int,
        source_url: str,
    ) -> ChapterMetadata:
        """
        Retrieve fresh metadata for one chapter.
        """
        raise NotImplementedError