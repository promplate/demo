import unittest
from unittest.mock import AsyncMock, patch

from src.utils.llm.openai import AsyncChatOpenAI


class TestAsyncChatOpenAI(unittest.TestCase):
    def setUp(self):
        self.mock_client = AsyncMock()
        self.openai = AsyncChatOpenAI(http_client=self.mock_client)

    async def test_successful_initialization(self):
        self.assertIsInstance(self.openai, AsyncChatOpenAI)

    @patch('src.utils.llm.openai.AsyncChatOpenAI.chat')
    async def test_successful_chat(self, mock_chat):
        mock_chat.return_value = {'choices': [{'message': {'content': 'Hello, world!'}}]}
        response = await self.openai.chat('Hello, world!')
        self.assertEqual(response, 'Hello, world!')

    @patch('src.utils.llm.openai.AsyncChatOpenAI.chat')
    async def test_failed_chat(self, mock_chat):
        mock_chat.side_effect = Exception('Chat failed')
        with self.assertRaises(Exception):
            await self.openai.chat('Hello, world!')

    @patch('src.utils.llm.openai.AsyncChatOpenAI.chat')
    async def test_empty_message_chat(self, mock_chat):
        mock_chat.return_value = {'choices': [{'message': {'content': ''}}]}
        response = await self.openai.chat('')
        self.assertEqual(response, '')

if __name__ == '__main__':
    unittest.main()
