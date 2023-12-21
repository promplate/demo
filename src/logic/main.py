from asyncio import gather, get_running_loop
from json import JSONDecodeError, dumps, loads
from typing import cast

from promplate import ChainContext, Jump, Message, Node
from promplate.chain.node import Chain, ChainContext
from promplate.prompt.utils import AutoNaming
from promplate_trace.auto import patch
from promptools.extractors import extract_json
from rich import print

from ..templates.schema.output import Output
from ..utils.load import load_template
from .tools import call_tool, tools

main = patch.node(Node)(load_template("main"), {"tools": tools})


@patch.chain
class Loop(Chain, AutoNaming):
    __str__ = Node.__str__  # type: ignore


main_loop = Loop(main)


@main.end_process
async def collect_results(context: ChainContext):
    parsed = cast(dict, context["parsed"] or {"content": [{"text": context.result}]})
    actions = parsed.get("actions", [])

    if not actions:
        return

    results = await gather(*(call_tool(i["name"], i["body"]) for i in actions))

    messages = cast(list[Message], context["messages"])

    messages.append({"role": "assistant", "content": dumps(parsed, ensure_ascii=False)})

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
        print("parsed json:", context["parsed"])
    except JSONDecodeError:
        try:
            context["parsed"] = extract_json(context.result, context.get("parsed", {}), Output)
        except SyntaxError:
            context["parsed"] = {"content": [{"text": context.result}]}

        context["partial"] = True


@main.mid_process
async def run_tools(context: ChainContext):
    if actions := cast(dict, context["parsed"]).get("actions", []):
        loop = get_running_loop()
        for action in actions[slice(None, -1 if context.get("partial") else None)]:
            loop.create_task(call_tool(action["name"], action["body"]))
            print(f"start <{action['name']}> with {action['body']}")
