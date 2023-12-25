import unittest.mock

import pytest
from src.utils.llm.openai import complete, generate


def test_complete_function():
    with unittest.mock.patch('src.utils.llm.openai.client') as mock_client:
        mock_client.return_value = unittest.mock.MagicMock(content=[unittest.mock.MagicMock(text='test response')])
        result = complete('test prompt', config={'test': 'config'})
        assert result == 'test response'

def test_generate_function():
    with unittest.mock.patch('src.utils.llm.openai.client') as mock_client:
        mock_client.return_value.__aenter__.return_value.__aiter__.return_value = iter([unittest.mock.MagicMock(type='content_block_delta', delta=unittest.mock.MagicMock(text='test response'))])
        result = list(generate('test prompt', config={'test': 'config'}))
        assert result == ['test response']
