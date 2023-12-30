from partial_json_parser import Allow, loads
from promplate import ChainContext, Node, parse_chat_markup
from promplate_trace.auto import patch

from ..utils.llm.anthropic import raw_anthropic
from ..utils.load import load_template

translate = patch.node(Node)(load_template("translate"), llm=raw_anthropic)

translate.run_config["stop_sequences"] = ["```"]
translate.run_config["model"] = "claude-instant-1.2"
translate.run_config["temperature"] = 0


hint = parse_chat_markup(load_template("translate").text)[-1]["content"].removeprefix("```json").strip()


@translate.mid_process
def parse_json(context: ChainContext):
    parsed = loads(hint + context.result, Allow.COLLECTION)
    return {"parsed": parsed}
