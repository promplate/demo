import unittest

from src.utils.config import Config


class TestConfig(unittest.TestCase):
    def test_minimax_api_key(self):
        config = Config()
        self.assertNotEqual(config.minimax_api_key, "")
