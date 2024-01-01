from partial_json_parser import Allow, loads
from promplate import ChainContext, Node, parse_chat_markup
from promplate_trace.auto import patch

from ..utils.llm.anthropic import raw_anthropic
from ..utils.load import load_template

translate = patch.node(Node)(load_template("translate"), llm=raw_anthropic)
"""
This function loads a template for translation, sets up some configurations, and returns a patched node.
It does not accept any parameters and does not return anything.
"""

translate.run_config["stop_sequences"] = ["\n```"]
translate.run_config["model"] = "claude-instant-1.2"
translate.run_config["temperature"] = 0


hint = parse_chat_markup(load_template("translate").text)[-1]["content"].removeprefix("```json").strip()


@translate.mid_process
def parse_json(context: ChainContext):
    """
    This function is a middleware function that parses JSON data from the context result.
    It accepts a `ChainContext` object as a parameter and does not return anything.
    """
    parsed = loads(hint + context.result, Allow.ARR)
    return {"parsed": parsed}
