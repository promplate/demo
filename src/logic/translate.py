from typing import Literal

from partial_json_parser import ARR
from promplate import ChainContext, Node
from promplate_trace.auto import patch
from promptools.extractors import extract_json

from ..utils.llm.openai import openai
from ..utils.load import load_template

translate = patch.node(Node)(load_template("translate"), llm=openai)

translate.run_config["stop"] = ["\n```"]
translate.run_config["temperature"] = 0


@translate.mid_process
def parse_json(context: ChainContext):
    parsed = extract_json(context.result, [], list[dict[Literal["original", "translated"], str]], allow_partial=ARR)
    return {"parsed": parsed}
