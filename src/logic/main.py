from asyncio import Task, gather, get_running_loop

from box import Box
from promplate import ChainContext, JumpTo, Node
from promptools.extractors import extract_json

from ..templates.schema.output import Output
from ..utils.llm.openai import openai
from ..utils.load import load_template
from .tools.stub import Browser

tools = [Browser()]
tools_map = {tool.name: tool for tool in tools}


main = Node(load_template("main"), {"tools": tools}, llm=openai)


@main.post_process
async def parse_json(context: ChainContext):
    res = context["parsed"] = Box(extract_json(context.result, {}, Output), default_box=True, default_box_attr=None)

    if res["actions"]:
        loop = get_running_loop()

        jobs: dict[int, Task] = context.get("__jobs__", {})
        for i, action in enumerate(res["actions"]):  # todo: the last one is incomplete
            if i not in jobs:
                jobs[i] = loop.create_task(tools_map[action["name"]](**action["body"]))
                print(f"running {action['name']} with {action['body']}")

        if True:  # todo: support streaming
            await gather(*jobs.values())

        context["return_values"] = {i: job.result() or job.exception() for i, job in jobs.items() if job.done()}

        if True and not res["end"]:
            raise JumpTo(main)
