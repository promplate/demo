from asyncio import gather, get_running_loop
from collections import defaultdict
from json import dumps
from typing import cast

from promplate import BaseCallback, ChainContext, Context, Loop, Message, Node
from promptools.extractors import extract_json

from ..templates.schema.output import Output
from ..utils.llm.openai import openai
from ..utils.load import load_template
from .tools import call_tool, tools

main = Node(load_template("main"), {"tools": tools}, llm=openai)

main_loop = Loop(main)


class EOC(Exception):
    "end of chain"

    def __init__(self, context: ChainContext):
        super().__init__(context)
        self.context = context


class Callback(BaseCallback):
    last = ""

    def on_enter(self, context: Context | None, config: Context):
        if context is None:
            context = {}

        if config.get("stream") != True:
            context["<end>"] = True

        return context, config

    def post_process(self, context: ChainContext):
        """A decorator used for post-processing. It takes a function as an argument and returns a new function that includes post-processing steps."""
        if context.get("<end>"):
            return

        if context.result != self.last:
            context["<end>"] = False
            self.last = context.result
        else:
            context["<end>"] = True


main.callbacks.append(Callback)


@main.post_process
async def run_tool(context: ChainContext):
    context["parsed"] = extract_json(context.result, {}, Output)
    res = defaultdict(lambda: None, context["parsed"])
    print(f"parsed json: {context['parsed']}")

    already_stop = context["<end>"]
    have_actions = isinstance(res["actions"], list) and len(res["actions"])

    if have_actions:
        loop = get_running_loop()
        actions = cast(list, res["actions"])

        for action in actions[slice(None, None if already_stop else -1)]:
            loop.create_task(call_tool(action["name"], action["body"]))
            print(f"running {action['name']} with {action['body']}")

    if already_stop:
        if not have_actions:
            raise EOC(context)

        assert isinstance(actions, list)  # type: ignore

        results = await gather(*(call_tool(i["name"], i["body"]) for i in actions))

        messages = cast(list[Message], context["messages"])

        messages.append({"role": "assistant", "content": context.result})

        messages.extend(
            [
                {
                    "role": "system",
                    "name": cast(str, action["name"]),
                    "content": (
                        str(result) if isinstance(result, (Exception, str)) else dumps(result, ensure_ascii=False, indent=2)
                    ),
                }
                for action, result in zip(actions, results)
            ]
        )
