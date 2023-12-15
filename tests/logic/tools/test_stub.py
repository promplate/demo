import pytest
from src.logic.tools.stub import Browser


def test_browser_call():
    browser = Browser()
    url = "https://example.com"
    assert browser(url) == url
