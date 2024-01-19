import unittest

from src.utils.llm.chatglm import get_client, Chat


class TestChatGLM(unittest.TestCase):
        def test_get_client(self):
        client = get_client()
                client = get_client()
        self.assertIsInstance(client, Chat)


if __name__ == "__main__":
    unittest.main()
