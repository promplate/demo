from promplate import Node

from ..utils.llm.openai import openai
from ..utils.load import load_template

main = Node(load_template("main"), llm=openai)


main.add_pre_processes(print)
