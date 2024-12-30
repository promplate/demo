from asyncio import ensure_future, gather
from json import dumps
from typing import cast

from promplate import Chain, ChainContext, Jump, Message
from promplate.prompt.utils import AutoNaming
from promplate_trace.auto import patch
from promptools.extractors import extract_json
from pydantic import TypeAdapter, ValidationError
from rich import print

from ..templates.schema.output import Output
from ..utils.functional import compose
from ..utils.load import load_template
from ..utils.node import Node
from .tools import call_tool, tools


class TypedContext(ChainContext):
    partial = True
    parsed: Output = {}


main = Node(load_template("main"), TypedContext({"tools": tools}))


@patch.chain
class Loop(Chain, AutoNaming):
    __str__ = Node.__str__  # type: ignore


main_loop = Loop(main)


_validator = TypeAdapter(Output)
serialize = compose(_validator.dump_json, bytes.decode)
loads = _validator.validate_json


@main.end_process
async def collect_results(context: TypedContext):
    parsed = context.parsed or {"content": [{"text": context.result}]}
    actions = parsed.get("actions", [])

    if not actions:
        return

    results = await gather(*(call_tool(i["name"], i.get("body", {})) for i in actions))

    messages = cast(list[Message], context["messages"])

    messages.append({"role": "assistant", "content": serialize(parsed)})

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
def parse_json(context: TypedContext):
    try:
        context.parsed = loads(context.result)
        context.pop("partial", None)
        context.partial = False
        print("parsed json:", context.parsed)
    except ValidationError:
        context["partial"] = True
        try:
            context.parsed = extract_json(context.result, context.parsed, Output)
        except SyntaxError:
            context["parsed"] = {"content": [{"text": context.result}]}
    finally:
        context["parsed"] = context.parsed


@main.mid_process
async def run_tools(context: TypedContext):
    if actions := context.parsed.get("actions"):
        for action in actions[:-1] if context.partial else actions:
            ensure_future(call_tool(action["name"], body := action.get("body", {})))
            print(f"start <{action['name']}> with {body}")
