import unittest
from unittest.mock import patch

from src.logic import main


class TestMain(unittest.TestCase):

    @patch('src.utils.load.load_template')
    def test_main(self, mock_load_template):
        mock_load_template.return_value = 'Mock Template'
        result = main.main
        self.assertEqual(result, 'Mock Template')

    @patch('src.utils.load.load_template')
    def test_main_no_template(self, mock_load_template):
        mock_load_template.return_value = None
        with self.assertRaises(ValueError):
            main.main

    @patch('src.utils.load.load_template')
    def test_main_invalid_template(self, mock_load_template):
        mock_load_template.return_value = 123
        with self.assertRaises(TypeError):
            main.main

if __name__ == '__main__':
    unittest.main()
