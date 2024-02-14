import unittest
from src.utils.llm.anthropic import Anthropic, RawAnthropic
from unittest.mock import MagicMock

from src.utils.llm.anthropic import Anthropic, RawAnthropic

from src.utils.llm.anthropic import Anthropic, RawAnthropic


class TestAnthropic(unittest.TestCase):
    def test_anthropic_split_prompt(self):
        # Test the complete method of Anthropic class
        anthropic = Anthropic()
        prompt = "Hello, world!"
        expected_response = "Completed prompt"
        anthropic.complete = MagicMock(return_value=expected_response)

        response = anthropic.complete(prompt)

        anthropic.complete.assert_called_once_with(prompt)
        self.assertEqual(response, expected_response)
        self.assertEqual(response, expected_response)

    def test_anthropic_complete_prompt(self):
        # Test the generate method of Anthropic class
        anthropic = Anthropic()
        prompt = "Hello, world!"
        expected_response = ["Generated text 1", "Generated text 2"]
        anthropic.generate = MagicMock(return_value=expected_response)

        response = anthropic.generate(prompt)

        anthropic.generate.assert_called_once_with(prompt)
        self.assertEqual(response, expected_response)
        self.assertEqual(response, expected_response)

    def test_raw_anthropic_split_prompt(self):
        # Test the complete method of RawAnthropic class
        raw_anthropic = RawAnthropic()
        prompt = "Hello, world!"
        expected_response = "Completed prompt"
        raw_anthropic.complete = MagicMock(return_value=expected_response)

        response = raw_anthropic.complete(prompt)

        raw_anthropic.complete.assert_called_once_with(prompt)
        self.assertEqual(response, expected_response)
        self.assertEqual(response, expected_response)

    def test_raw_anthropic_complete_prompt(self):
        # Test the generate method of RawAnthropic class
        raw_anthropic = RawAnthropic()
        prompt = "Hello, world!"
        expected_response = ["Generated text 1", "Generated text 2"]
        raw_anthropic.generate = MagicMock(return_value=expected_response)

        response = raw_anthropic.generate(prompt)

        raw_anthropic.generate.assert_called_once_with(prompt)
        self.assertEqual(response, expected_response)
        self.assertEqual(response, expected_response)


unittest.main()
