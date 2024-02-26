import unittest
from unittest.mock import MagicMock

from src.utils.llm.qwen import Qwen


class TestQwen(unittest.TestCase):
    def setUp(self):
        self.qwen = Qwen()

    def test_complete(self):
        # Implement test cases for the complete method of Qwen
        pass

    def test_generate(self):
        # Implement test cases for the generate method of Qwen
        pass

if __name__ == "__main__":
    unittest.main()
