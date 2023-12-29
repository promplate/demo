import asyncio
import unittest

from src.utils.llm.octoai import OctoAI


class TestOctoAIComplete(unittest.TestCase):
    def setUp(self):
        self.octoai = OctoAI().bind(model="mixtral-8x7b-instruct-fp16")

    def test_complete_with_string_prompt(self):
        result = asyncio.run(self.octoai.complete("Hello, how are you?"))
        self.assertIsInstance(result, str)

    def test_complete_with_list_prompt(self):
        result = asyncio.run(self.octoai.complete(["Hello, how are you?", "I'm fine, thank you."]))
        self.assertIsInstance(result, str)

class TestOctoAIGenerate(unittest.TestCase):
    def setUp(self):
        self.octoai = OctoAI().bind(model="mixtral-8x7b-instruct-fp16")

    def test_generate_with_string_prompt(self):
        result = asyncio.run(self.octoai.generate("Hello, how are you?"))
        self.assertIsInstance(result, str)

    def test_generate_with_list_prompt(self):
        result = asyncio.run(self.octoai.generate(["Hello, how are you?", "I'm fine, thank you."]))
        self.assertIsInstance(result, str)

class TestOctoAIBind(unittest.TestCase):
    def setUp(self):
        self.octoai = OctoAI()

    def test_bind_updates_run_config(self):
        self.octoai.bind(model="mixtral-8x7b-instruct-fp16")
        self.assertEqual(self.octoai._run_config["model"], "mixtral-8x7b-instruct-fp16")

    def test_bind_returns_self(self):
        result = self.octoai.bind(model="mixtral-8x7b-instruct-fp16")
        self.assertEqual(result, self.octoai)

if __name__ == "__main__":
    unittest.main()
