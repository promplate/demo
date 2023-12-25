import pytest
from src.utils.llm.common import ensure_safe


def test_ensure_safe_function():
    test_prompt = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "system", "content": "System message"}
    ]
    expected_result = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "user", "content": "System message"}
    ]
    assert ensure_safe(test_prompt) == expected_result
