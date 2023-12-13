import pytest
from fastapi.responses import JSONResponse, PlainTextResponse

from src import render_template
from src.utils.helpers import DotTemplate
from src.utils.load import Templates, load_template


@pytest.mark.parametrize("context", [{"key": "value"}, {}, None])
def test_render_template_text_sync(context):
    template = Templates["Main"]
    result = render_template(template, context, "text", True)
    assert isinstance(result, PlainTextResponse)

@pytest.mark.parametrize("context", [{"key": "value"}, {}, None])
def test_render_template_text_async(context):
    template = Templates["Main"]
    result = render_template(template, context, "text", False)
    assert isinstance(result, PlainTextResponse)

@pytest.mark.parametrize("context", [{"key": "value"}, {}, None])
def test_render_template_list_sync(context):
    template = Templates["Main"]
    result = render_template(template, context, "list", True)
    assert isinstance(result, JSONResponse)

@pytest.mark.parametrize("context", [{"key": "value"}, {}, None])
def test_render_template_list_async(context):
    template = Templates["Main"]
    result = render_template(template, context, "list", False)
    assert isinstance(result, JSONResponse)

@pytest.mark.parametrize("context", [{"key": "value"}, {}, None])
def test_render_template_script_sync(context):
    template = Templates["Main"]
    result = render_template(template, context, "script", True)
    assert isinstance(result, PlainTextResponse)

@pytest.mark.parametrize("context", [{"key": "value"}, {}, None])
def test_render_template_script_async(context):
    template = Templates["Main"]
    result = render_template(template, context, "script", False)
    assert isinstance(result, PlainTextResponse)
