import unittest

from src.logic.translate import translate


class TestTranslate(unittest.TestCase):

    def test_translate_with_valid_input(self):
        valid_input = 'valid input'
        expected_output = 'expected output'
        actual_output = translate(valid_input)
        self.assertEqual(actual_output, expected_output)

    def test_translate_with_invalid_input(self):
        invalid_input = 'invalid input'
        with self.assertRaises(Exception):
            translate(invalid_input)

if __name__ == '__main__':
    unittest.main()
