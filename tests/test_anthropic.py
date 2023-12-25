import unittest.mock

import pytest
from src.utils.llm.anthropic import Anthropic


def test_complete_method():
    with unittest.mock.patch('src.utils.llm.anthropic.get_anthropic') as mock_get_anthropic:
        mock_get_anthropic.return_value.beta.messages.create.return_value = unittest.mock.MagicMock(content=[unittest.mock.MagicMock(text='test response')])
        result = pytest.run(Anthropic.complete('test prompt', config={'test': 'config'}))
        assert result == 'test response'

def test_generate_method():
    with unittest.mock.patch('src.utils.llm.anthropic.get_anthropic') as mock_get_anthropic:
        mock_get_anthropic.return_value.beta.messages.create.return_value.__aenter__.return_value.__aiter__.return_value = iter([unittest.mock.MagicMock(type='content_block_delta', delta=unittest.mock.MagicMock(text='test response'))])
        result = list(pytest.run(Anthropic.generate('test prompt', config={'test': 'config'})))
        assert result == ['test response']
