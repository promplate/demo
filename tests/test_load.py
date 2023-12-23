import unittest
from unittest.mock import patch

from src.utils.load import DotTemplate, load_template


class TestLoadTemplate(unittest.TestCase):

    @patch('src.utils.load.glob')
    @patch('src.utils.load.root')
    def test_load_template_from_global(self, mock_root, mock_glob):
        mock_glob.return_value = {'template': 'global_template'}
        mock_root.is_dir.return_value = False
        result = load_template('template')
        self.assertEqual(result, 'global_template')

    @patch('src.utils.load.glob')
    @patch('src.utils.load.root')
    @patch('src.utils.load.components')
    def test_load_template_from_directory(self, mock_components, mock_root, mock_glob):
        mock_glob.return_value = {}
        mock_root.is_dir.return_value = True
        mock_components.template = 'directory_template'
        result = load_template('template')
        self.assertEqual(result, 'directory_template')

    @patch('src.utils.load.glob')
    @patch('src.utils.load.root')
    def test_load_template_not_found(self, mock_root, mock_glob):
        mock_glob.return_value = {}
        mock_root.is_dir.return_value = False
        with self.assertRaises(KeyError):
            load_template('template')
