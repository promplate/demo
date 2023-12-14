import unittest

from src.routes.prompts import show_raw_template


class TestShowRawTemplate(unittest.TestCase):
    def test_show_raw_template(self):
        # Test case 1: Valid input
        template = "valid_template"
        expected_output = "expected_output_for_valid_template"
        actual_output = show_raw_template(template)
        self.assertEqual(actual_output, expected_output)

        # Test case 2: Invalid input
        template = "invalid_template"
        expected_output = "expected_output_for_invalid_template"
        actual_output = show_raw_template(template)
        self.assertEqual(actual_output, expected_output)

        # Test case 3: Edge case (e.g., empty string)
        template = ""
        expected_output = "expected_output_for_empty_string"
        actual_output = show_raw_template(template)
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
