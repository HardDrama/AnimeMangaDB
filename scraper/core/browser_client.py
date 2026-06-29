from playwright.sync_api import sync_playwright


class BrowserClient:
    """
    Downloads fully rendered HTML using Playwright.
    """

    def fetch(self, url: str) -> str:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page(
                viewport={
                    "width": 1920,
                    "height": 1080,
                },
                user_agent=(
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                ),
            )

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            page.wait_for_timeout(3000)

            html = page.content()

            browser.close()

            return html