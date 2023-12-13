import pytest
from src import render_template
from src.utils.load import Context, Templates


def test_render_template_text_async():
    template = Templates.MAIN
    context = Context({"name": "Test"})
    format = "text"
    sync = False
    expected_output = "Hello, Test"
    assert render_template(template, context, format, sync) == expected_output

def test_render_template_text_sync():
    template = Templates.MAIN
    context = Context({"name": "Test"})
    format = "text"
    sync = True
    expected_output = "Hello, Test"
    assert render_template(template, context, format, sync) == expected_output

def test_render_template_script_async():
    template = Templates.MAIN
    context = Context({"name": "Test"})
    format = "script"
    sync = False
    expected_output = "print('Hello, Test')"
    assert render_template(template, context, format, sync) == expected_output

def test_render_template_script_sync():
    template = Templates.MAIN
    context = Context({"name": "Test"})
    format = "script"
    sync = True
    expected_output = "print('Hello, Test')"
    assert render_template(template, context, format, sync) == expected_output

def test_render_template_exception():
    template = Templates.MAIN
    context = Context({"name": "Test"})
    format = "invalid_format"
    sync = False
    with pytest.raises(Exception):
        render_template(template, context, format, sync)
