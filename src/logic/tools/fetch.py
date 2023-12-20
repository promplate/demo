"""
This file contains a class that represents a simple browser to fetch and parse URLs,
using asynchronous HTTP requests and providing methods to parse HTML content.
"""

from contextlib import suppress
from functools import cached_property
from json import JSONDecodeError
from typing import cast

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from html2text import html2text
from httpx import AsyncClient, HTTPError

from .base import AbstractTool

ua = UserAgent(min_percentage=0.5)


class Browser(AbstractTool):
    """Fetch an url. The only paremeter `url`. URLs on the page can be used for reference. If you want to know any realworld fact, you should search Google."""

    name = "fetch"

    @cached_property
    def client(self):
        """Initializes and returns an HTTP client with pre-configured settings.

        Returns:
            AsyncClient: An instance of httpx.AsyncClient configured for the browser.
        """
        return AsyncClient(http2=True, headers={"accept": "application/json,text/html,text/*"}, follow_redirects=True, timeout=10)

    @property
    def headers(self):
        """Gets the headers to be used for HTTP requests, including a random user-agent.

        Returns:
            dict: A dictionary containing the 'user-agent' header.
        """
        return {"user-agent": ua.random}

    def parse_html(self, html: str, url: str):
        """Parses HTML content, removing or altering certain elements like images and links.

        Args:
            html (str): The HTML content to be parsed.
            url (str): The base URL to resolve relative links.

        Returns:
            str: The text representation of the parsed HTML.
        """
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
        """Fetches the content of a URL using an asynchronous HTTP GET request.

        Args:
            url (str): The URL to fetch.

        Returns:
            Optional[Response]: The HTTP response received, or None if an HTTPError occurred.
        """
        for _ in range(5):
            with suppress(HTTPError):
                return await self.client.get(url, headers=self.headers)

    async def __call__(self, url: str):
        """Acts as a callable method for the class to fetch and process a URL.

        Args:
            url (str): The URL to be processed.

        Returns:
            Optional[Union[dict, str]]: The processed data from the URL, which can be a JSON
                dictionary, text representation of HTML, or raw text, depending on the content type.
        """
        res = await self.fetch(url)
        if res is None:
            return

        try:
            return res.json()
        except JSONDecodeError:
            if "html" in res.headers.get("content-type", ""):
                return self.parse_html(res.text, url)
            return res.text
