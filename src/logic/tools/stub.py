from partial_json_parser import JSON

from .base import AbstractTool


class Browser(AbstractTool):
    name = "fetch"
    description = "fetch an url. the only paremeter `url`"

    def __call__(self, url: str):
        return url
