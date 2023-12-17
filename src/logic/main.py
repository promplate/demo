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
    parsed = cast(dict, context["parsed"])
    actions = parsed.get("actions", [])

    if not actions:
        return

    results = await gather(*(call_tool(i["name"], i["body"]) for i in actions))

    messages = cast(list[Message], context["messages"])

    messages.append({"role": "assistant", "content": context.result})

    messages.extend(
        [
            {
                "role": "system",
                "name": cast(str, action["name"]),
                "content": (str(result) if isinstance(result, (Exception, str)) else dumps(result, ensure_ascii=False, indent=2)),
            }
            for action, result in zip(actions, results)
        ]
    )

    del parsed["actions"]

    raise Jump(into=main)


@main.mid_process
def parse_json(context: ChainContext):
    try:
        context["parsed"] = loads(context.result)
        context.pop("partial", None)
    except JSONDecodeError:
        context["parsed"] = extract_json(context.result, {}, Output)
        context["partial"] = True
    print("parsed json:", context["parsed"])


@main.mid_process
async def run_tools(context: ChainContext):
    actions = cast(dict, context["parsed"]).get("actions", [])

    if actions:
        loop = get_running_loop()
        for action in actions[slice(None, -1 if context.get("partial") else None)]:
            loop.create_task(call_tool(action["name"], action["body"]))
            print(f"start <{action['name']}> with {action['body']}")
