from promplate import Node

from ..utils.llm.openai import openai
from ..utils.load import Template, load_template
from .main import main


def get_node(template: Template):
    match template:
        case "main":
            return main
        case _:
            return Node(load_template(template), llm=openai)
