import unittest
from unittest.mock import patch

from src.utils.config import Config


class TestConfig(unittest.TestCase):

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'mock_api_key'})
    def test_openai_api_key(self):
        config = Config()
        self.assertEqual(config.openai_api_key, 'mock_api_key')

    @patch.dict('os.environ', {'OPENAI_BASE_URL': 'mock_base_url'})
    def test_openai_base_url(self):
        config = Config()
        self.assertEqual(config.openai_base_url, 'mock_base_url')

    @patch.dict('os.environ', {'MODEL_CONFIG': 'mock_model_config'})
    def test_model_config(self):
        config = Config()
        self.assertEqual(config.model_config, 'mock_model_config')

if __name__ == '__main__':
    unittest.main()
