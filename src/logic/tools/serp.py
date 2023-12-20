from functools import cached_property
from typing import Literal

from httpx import AsyncClient
from pydantic import validate_call

from ...utils.config import env
from ...utils.load import load_template
from .base import AbstractTool


class Serper(AbstractTool):
    __doc__ = load_template("schema/serp").text

    name = "serp"

    @cached_property
    def client(self) -> AsyncClient:
        return AsyncClient(
            base_url="https://google.serper.dev/",
            headers={"X-API-KEY": env.serper_api_key, "Content-Type": "application/json"},
        )

    @validate_call
    async def __call__(self, query: str, type: Literal["search", "news", "places"] = "search", page: int = 1):
        return (await self.client.post(f"/{type}", json={"q": query, "page": page})).json()
