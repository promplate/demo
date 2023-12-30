from promplate import Node

from ..utils.load import Template, load_template
from .main import main_loop
from .translate import translate


def get_node(template: Template):
    match template:
        case "main":
            return main_loop
        case "translate":
            return translate
        case _:
            return Node(load_template(template))
