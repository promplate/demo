from contextlib import suppress
from functools import cached_property
from json import JSONDecodeError
from typing import cast

from bs4 import BeautifulSoup
from fake_useragent.fake import FakeUserAgent
from html2text import html2text
from httpx import AsyncClient, HTTPError

from .base import AbstractTool

ua = FakeUserAgent(min_percentage=0.5)


class Browser(AbstractTool):
    """Fetch an url. The only parameter `url`. URLs on the page can be used for reference. If you want to know any realworld fact, you should search Google."""

    name = "fetch"

    @cached_property
    def client(self):
        return AsyncClient(http2=True, headers={"accept": "application/json,text/html,text/*"}, follow_redirects=True, timeout=10)

    @property
    def headers(self):
        return {"user-agent": ua.random}

    def parse_html(self, html: str, url: str):
        soup = BeautifulSoup(html, "html.parser")
        # todo: give each url an id and replace it
        for img in soup.select("img"):
            if cast(str, img.get("src", "")).startswith("data"):
                del img["src"]
        for a in soup.select("a"):
            if len(cast(str, a.get("href", ""))) > 50:
                del a["href"]
        return html2text(str(soup), url, 0)

    async def fetch(self, url: str):
        for _ in range(5):
            with suppress(HTTPError):
                return await self.client.get(url, headers=self.headers)

    async def __call__(self, url: str):
        res = await self.fetch(url)
        if res is None:
            return

        try:
            return res.json()
        except JSONDecodeError:
            if "html" in res.headers.get("content-type", ""):
                return self.parse_html(res.text, url)
            return res.text
