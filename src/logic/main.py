from asyncio import gather, get_running_loop
from json import JSONDecodeError, dumps, loads
from typing import cast

from promplate import ChainContext, Jump, Message, Node
from promplate.chain.node import ChainContext
from promptools.extractors import extract_json
from rich import print

from ..templates.schema.output import Output
from ..utils.llm.openai import openai
from ..utils.load import load_template
from .tools import call_tool, tools

main = Node(load_template("main"), {"tools": tools}, llm=openai)


@main.end_process
async def collect_results(context: ChainContext):
    await collect_results(context)

    raise Jump(into=main)



    try:
        context["parsed"] = loads(context.result)
        context.pop("partial", None)
    except JSONDecodeError:
        context["parsed"] = extract_json(context.result, {}, Output)
        context["partial"] = True
    print("parsed json:", context["parsed"])



    actions = cast(dict, context["parsed"]).get("actions", [])

    if actions:
        loop = get_running_loop()
        for action in actions[slice(None, -1 if context.get("partial") else None)]:
            loop.create_task(call_tool(action["name"], action["body"]))
            print(f"start <{action['name']}> with {action['body']}")
