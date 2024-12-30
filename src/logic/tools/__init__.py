from asyncio import Future
from json import dumps
from typing import cast

from partial_json_parser import JSON
from promplate import Context
from promplate.chain.utils import resolve

from .base import AbstractTool
from .fetch import Browser
from .python import CodeInterpreter
from .serp import Serper

tools: list[AbstractTool] = [CodeInterpreter(), Serper(), Browser()]
tool_map: dict[str, AbstractTool] = {tool.name: tool for tool in tools}


async def call_tool(name: str, body: Context):
    tool = tool_map[name]
    return await resolve(tool(**body))
