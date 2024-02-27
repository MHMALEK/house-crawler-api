from pyppeteer import launch
from pyppeteer_stealth import stealth
import requests
from bs4 import BeautifulSoup
import random
import time
import asyncio


class BrowserService:
    def __init__(self):
        self.browser = None

    async def start(self):
        self.browser = await launch(headless=False)

    async def get_page(self):
        if not self.browser:
            await self.start()
        page = await self.browser.newPage()
        await stealth(page)
        return page

    async def go_to_url(self, url):
        page = await self.get_page()
        await page.goto(url)
        return page

    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None


class BeautifulSoupService:
    def __init__(self, parser="html.parser"):
        self.soup = None
        self.parser = parser

    def parse(self, html):
        self.soup = BeautifulSoup(html, self.parser)

    def find_all_class(self, tag, class_):
        return self.soup.find_all(tag, class_=class_)

    def find_class(self, tag, class_):
        return self.soup.find(tag, class_=class_)

    def get_text(self, tag):
        return tag.get_text()

    def get_attribute(self, tag, attribute):
        return tag.get(attribute)


class BaseCrawler:
    def __init__(
        self,
        base_url,
        delay=1.0,
        max_retries=3,
        parser="html.parser",
        user_agents=None,
        cookies=None,
        use_browser=False,
    ):

        self.base_url = base_url
        self.delay = delay
        self.max_retries = max_retries
        self.parser = parser
        self.user_agents = user_agents or [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20220104 Firefox/108.0",
            "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        ]
        self.current_page = 1
        self.results = []
        self.cookies = cookies
        self.use_browser = use_browser
        self.browser_service = BrowserService() if use_browser else None

    def get_url(self, page):
        raise NotImplementedError(
            "Implement page URL construction for the specific service."
        )

    def log_error(self, message):
        print(message)

    async def get_page_browser(self, url):
        page = await self.browser_service.go_to_url(url)
        content = await page.content()
        print(content)
        return content

    def get_page(self, url):
        print(self.use_browser, url)
        if self.use_browser:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        retries = self.max_retries
        while retries:
            try:
                headers = {"User-Agent": random.choice(self.user_agents)}
                if self.cookies:
                    headers["Cookie"] = "; ".join(
                        [f"{k}={v}" for k, v in self.cookies.items()]
                    )
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    if (
                        not response.text
                    ):  # Avoid empty content after successful request
                        self.log_error(f"Empty content received from {url}")
                        continue
                    return response.text
                retries -= 1
                self.log_error(
                    f"Request failed for {url} (status code: {response.status_code}), Retrying..."
                )
                time.sleep(
                    self.delay * random.uniform(0.5, 1.5)
                )  # Adaptive delay with jitter
            except requests.exceptions.RequestException as e:
                retries -= 1
                self.log_error(f"Request failed: {str(e)}, Retrying...")
                time.sleep(self.delay * random.uniform(0.5, 1.5))
        return None

    def process_page(self, soup):
        raise NotImplementedError(
            "Implement data extraction logic for the specific service."
        )

    def should_stop(self):
        return False

    def crawl(self):
        """Starts the crawling process, navigating pages from the base URL until stopping criteria are met."""

        url = self.get_url(self.current_page)

        # 2. Fetch page content with error handling and rate limiting:
        page_contents = self.get_page(url)

        # 3. Exit if page retrieval fails or stopping criteria are met:
        if (
            page_contents is None or self.should_stop()
        ):  # Implement stopping criteria (e.g., max pages, no new data)
            self.log_error("Crawling finished.")
            return self.results

        # 4. Extract data from the parsed page:
        soup = BeautifulSoup(page_contents, self.parser)
        extracted_data = self.process_page(soup)
        self.results = extracted_data
        return self.results
