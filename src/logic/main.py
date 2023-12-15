from promplate import ChainContext, Node
from promptools.extractors import extract_json

from ..templates.schema.output import Output
from ..utils.llm.openai import openai
from ..utils.load import load_template
from .tools.stub import Browser

main = Node(load_template("main"), {"tools": [Browser()]}, llm=openai)


main.add_pre_processes(print)


@main.post_process
def parse_json(context: ChainContext):
    context["parsed"] = extract_json(context.result, {}, Output)
