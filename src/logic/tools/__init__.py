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


states: dict[tuple[str, str], Future | JSON] = {}


def hashable(json: dict):
    return dumps(json, sort_keys=True)


async def call_tool(name: str, body: Context):
    key = (name, hashable(body))

    if key not in states:
        job = states[key] = Future()
        tool = tool_map[name]
        result = await resolve(tool(**body))
        job.set_result(result)
        return result

    job = states.get(key)
    return cast(JSON, await job if isinstance(job, Future) else job)
