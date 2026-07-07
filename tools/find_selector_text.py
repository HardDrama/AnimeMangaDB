import argparse
from pathlib import Path

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(
        description="Locate text inside a downloaded HTML file."
    )

    parser.add_argument(
        "html_file",
        help="Path to the downloaded HTML file.",
    )

    parser.add_argument(
        "search_text",
        help="Text to search for.",
    )

    args = parser.parse_args()

    html = Path(args.html_file).read_text(
        encoding="utf-8"
    )

    soup = BeautifulSoup(html, "html.parser")

    found = False

    for element in soup.find_all(string=True):
        text = element.strip()

        if (
            text
            and args.search_text.lower()
            in text.lower()
        ):
            found = True

            print("=" * 80)
            print("Matched Text")
            print("-" * 80)
            print(text)

            print()
            print("Parent Element")
            print("-" * 80)
            print(element.parent)

            print()

    if not found:
        print("No matching text found.")


if __name__ == "__main__":
    main()