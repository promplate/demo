import unittest
from unittest.mock import MagicMock, patch

from src.utils.load import generate_pyi


class TestGeneratePyi(unittest.TestCase):

    @patch('src.utils.load.Path')
    def test_generate_pyi(self, mock_path):
        mock_source = MagicMock()
        mock_target = MagicMock()
        mock_path.return_value = mock_source
        mock_source.with_suffix.return_value = mock_target
        mock_source.read_text.return_value = 'source text'

        generate_pyi()

        mock_source.with_suffix.assert_called_once_with('.pyi')
        mock_target.write_text.assert_called_once_with('source text')

    @patch('src.utils.load.Path')
    def test_generate_pyi_no_debug(self, mock_path):
        mock_source = MagicMock()
        mock_target = MagicMock()
        mock_path.return_value = mock_source
        mock_source.with_suffix.return_value = mock_target

        with patch('src.utils.load.__debug__', new=False):
            generate_pyi()

        mock_source.with_suffix.assert_not_called()
        mock_target.write_text.assert_not_called()

if __name__ == '__main__':
    unittest.main()
