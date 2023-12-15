import pytest
from promplate import ChainContext
from src.logic import Node, load_template, openai
from src.logic.main import Browser, main, parse_json
from src.templates.schema.output import Output


def test_main():
    assert isinstance(main, Node)
    assert main.template == load_template("main")
    assert isinstance(main.tools[0], Browser)
    assert main.llm == openai

def test_parse_json():
    context = ChainContext(result='{"content": [{"text": "Hello, world!"}]}')
    parse_json(context)
    assert context["parsed"] == Output(content=[Span(text="Hello, world!")])

def test_pre_processes():
    context = ChainContext()
    main.pre_processes[0](context)
    assert context.result is None

def test_post_process():
    context = ChainContext(result='{"content": [{"text": "Hello, world!"}]}')
    main.post_process(context)
    assert context["parsed"] == Output(content=[Span(text="Hello, world!")])
