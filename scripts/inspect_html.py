from pathlib import Path

from bs4 import BeautifulSoup

HTML_FILE = "tests/fixtures/one_piece_episode_1130.html"


def main():
    html = Path(HTML_FILE).read_text(encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")

    while True:
        selector = input("\nCSS selector (or 'quit'): ")

        if selector.lower() == "quit":
            break

        try:
            matches = soup.select(selector)
        except Exception as e:
            print(f"Invalid selector: {e}")
            continue

        print(f"\nFound {len(matches)} match(es).\n")

        for i, element in enumerate(matches[:5], start=1):
            print(f"----- Match {i} -----")
            print(element.prettify()[:1000])
            print("-" * 40)


if __name__ == "__main__":
    main()
