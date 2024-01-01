"""
This file contains the logic for translating text using a specific model. It includes functions for parsing JSON data and configuring the translation model.
"""

from typing import Literal

from partial_json_parser import ARR
from promplate import ChainContext, Node, parse_chat_markup
from promplate_trace.auto import patch
from promptools.extractors import extract_json

from ..utils.llm.anthropic import raw_anthropic
from ..utils.load import load_template

translate = patch.node(Node)(load_template("translate"), llm=raw_anthropic)

translate.run_config["stop_sequences"] = ["\n```"]
translate.run_config["model"] = "claude-instant-1.2"
translate.run_config["temperature"] = 0


hint = parse_chat_markup(load_template("translate").text)[-1]["content"].removeprefix("```json").strip()


@translate.mid_process
def parse_json(context: ChainContext):
    """
    Parses JSON data from a given context.

    Parameters:
    context (ChainContext): The context from which to extract the JSON data.

    Returns:
    dict: A dictionary containing the parsed JSON data.
    """
    parsed = extract_json(hint + context.result, [], list[dict[Literal["original", "translated"], str]], allow_partial=ARR)
    return {"parsed": parsed}
