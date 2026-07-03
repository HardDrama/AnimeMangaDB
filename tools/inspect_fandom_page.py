from pathlib import Path

from bs4 import BeautifulSoup

from scraper.core.http_client import HttpClient


def inspect(url: str):
    client = HttpClient()

    print(f"Downloading: {url}")

    html = client.fetch(url)

    Path("inspect.html").write_text(
        html,
        encoding="utf-8",
    )

    soup = BeautifulSoup(html, "html.parser")

    print()
    print("Title:")
    print("----------------")
    print(soup.title.string if soup.title else "None")

    print()
    print("First five headings:")
    print("----------------")

    for heading in soup.find_all(
        ["h1", "h2", "h3"]
    )[:5]:
        print(
            heading.get_text(
                " ",
                strip=True,
            )
        )


if __name__ == "__main__":
    inspect(
        "https://naruto.fandom.com/wiki/Episode_1"
    )