import unittest

from .openai import OpenAI


class TestOpenAI(unittest.TestCase):
    def setUp(self):
        self.openai = OpenAI().bind(
            model="gpt-3.5-turbo-1106",
            temperature=0.7,
        )

    def test_complete_with_valid_input(self):
        prompt = "Hello, how are you?"
        config = {"max_tokens": 50}
        result = self.openai.complete(prompt, **config)
        self.assertIsInstance(result, str)

    def test_complete_with_empty_prompt(self):
        prompt = ""
        config = {"max_tokens": 50}
        result = self.openai.complete(prompt, **config)
        self.assertIsInstance(result, str)

    def test_complete_with_invalid_config(self):
        prompt = "Hello, how are you?"
        config = {"max_tokens": "fifty"}
        with self.assertRaises(TypeError):
            self.openai.complete(prompt, **config)

if __name__ == "__main__":
    unittest.main()
