import httpx


class HttpClient:
    """
    A simple HTTP client for downloading web pages
    """

    def fetch(self, url: str) -> str:
        response = httpx.get(
            url,
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "AnimeMangaDB/0.1 "
                    "(https://github.com/HardDrama/AnimeMangaDB)"
                )
            },
        )

        response.raise_for_status()

        return response.text