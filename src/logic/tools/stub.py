"""
This file defines the Browser class which can be used to fetch and parse HTML content from the web.
It includes functionality to make HTTP requests with retries and to process the HTML content.

Classes:
    Browser: A tool to perform web requests and process the results.
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
    """
The Browser class is designed to perform web requests and process HTML content.
It includes methods to fetch URLs with automatic retry, parse HTML to remove undesired attributes,
and to return structured data from JSON responses or textual information from HTML.
    """
    "fetch an url. the only paremeter `url`"

    name = "fetch"

    @cached_property
    def client(self):
        """
        Provides an AsyncClient instance configured with HTTP/2 support, appropriate headers,
        and redirection following for making web requests.
        
        Returns:
            An instance of AsyncClient.
        """
        return AsyncClient(http2=True, headers={"accept": "application/json,text/html,text/*"}, follow_redirects=True)

    @property
    def headers(self):
        """
        Provides a dictionary of default HTTP headers for use in web requests, with a random user-agent string.
        
        Returns:
            A dictionary containing the 'user-agent' header.
        """
        return {"user-agent": ua.random}

    def parse_html(self, html: str, url: str):
        """
        Parses an HTML string, removing 'src' attributes from 'img' tags that start with 'data',
        and returns the modified HTML as text. It uses the given URL to resolve relative links.
        
        Parameters:
            html: The HTML content as a string.
            url: The base URL used for parsing the HTML content.
        
        Returns:
            The processed HTML content as text without 'data' prefixed 'src' attributes in 'img' tags.
        """
        soup = BeautifulSoup(html, "html.parser")
        # todo: give each url an id and replace it
        for img in soup.select("img"):
            if cast(str, img.get("src", "")).startswith("data"):
                del img["src"]
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
