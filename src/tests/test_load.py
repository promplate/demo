import unittest

from src.utils.load import load_template


class TestLoadTemplate(unittest.TestCase):
    def test_load_template(self):
        # Test case 1: Valid input
        stem = "valid_stem"
        expected_output = "expected_output_for_valid_stem"
        actual_output = load_template(stem)
        self.assertEqual(actual_output, expected_output)

        # Test case 2: Invalid input
        stem = "invalid_stem"
        expected_output = "expected_output_for_invalid_stem"
        actual_output = load_template(stem)
        self.assertEqual(actual_output, expected_output)

        # Test case 3: Edge case (e.g., empty string)
        stem = ""
        expected_output = "expected_output_for_empty_string"
        actual_output = load_template(stem)
        self.assertEqual(actual_output, expected_output)

if __name__ == "__main__":
    unittest.main()
