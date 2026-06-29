from bs4 import BeautifulSoup


class HtmlParser:
    """
    Wraps BeautifulSoup so all parsers use the same configuration.
    """

    def parse(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")