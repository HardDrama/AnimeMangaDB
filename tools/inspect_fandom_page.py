import argparse

from pathlib import Path

from bs4 import BeautifulSoup

from scraper.core.http_client import HttpClient


def inspect(url: str):
    client = HttpClient()

    print(f"Downloading: {url}")

    html = client.fetch(url)

    output_dir = Path("inspect_output")
    output_dir.mkdir(exist_ok=True)

    safe_name = (
        url.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace(":", "_")
    )

    output_file = output_dir / f"{safe_name}.html"

    output_file.write_text(
        html,
        encoding="utf-8",
    )

    print(f"Saved HTML to: {output_file}")

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

    print()
    print("Infobox data-source fields:")
    print("---------------------------")

    for element in soup.select("[data-source]"):
        print(element["data-source"])

    print()
    print("Tables found:")
    print("-------------")

    tables = soup.find_all("table")

    print(f"{len(tables)} table(s)")

    print()
    print("Links containing 'Episode_Guide':")
    print("---------------------------------")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "Episode_Guide" in href:
            print(href)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inspect a Fandom page structure"
    )

    parser.add_argument(
        "url",
        nargs="?",
        default="https://naruto.fandom.com/wiki/Episode_1",
        help="Fandom page URL to inspect",
    )

    args = parser.parse_args()

    inspect(args.url)