import unittest
from unittest.mock import patch

from src.utils.load import LazyLoader, load_template


class TestLoadTemplate(unittest.TestCase):
    @patch('src.utils.load.glob')
    def test_load_valid_template(self, mock_glob):
        mock_glob.return_value = {'valid_template': 'template_content'}
        result = load_template('valid_template')
        self.assertEqual(result, 'template_content')

    @patch('src.utils.load.glob')
    def test_load_invalid_template(self, mock_glob):
        mock_glob.return_value = {}
        with self.assertRaises(KeyError):
            load_template('invalid_template')

class TestGetAttr(unittest.TestCase):
    @patch('src.utils.load.root')
    def test_getattr_valid_dir(self, mock_root):
        mock_root.__truediv__.return_value.is_dir.return_value = True
        loader = LazyLoader()
        result = loader.__getattr__('valid_dir')
        self.assertIsInstance(result, LazyLoader)

    @patch('src.utils.load.root')
    def test_getattr_invalid_dir(self, mock_root):
        mock_root.__truediv__.return_value.is_dir.return_value = False
        loader = LazyLoader()
        with self.assertRaises(KeyError):
            loader.__getattr__('invalid_dir')

if __name__ == '__main__':
    unittest.main()
