from promplate import Node

from ..utils.load import load_template, TemplateNotFoundError

try:
    main = Node(load_template("Main"))
except TemplateNotFoundError as e:
    main = Node(lambda context: f"Template not found: {e}")
