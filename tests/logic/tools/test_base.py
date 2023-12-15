import pytest
from src.logic.tools.base import AbstractTool


class MockTool(AbstractTool):
    name = "mock_tool"
    description = "This is a mock tool for testing."

    def __call__(self, **kwargs):
        return kwargs

def test_abstract_tool():
    tool = MockTool()
    assert tool.name == "mock_tool"
    assert tool.description == "This is a mock tool for testing."
    assert tool(arg1="test", arg2=123) == {"arg1": "test", "arg2": 123}
