import unittest

from src.templates.schema.output import Output


class TestOutput(unittest.TestCase):
    def test_output_content(self):
        output = Output(content=[{'text': 'Hello', 'reference': 'Greeting'}], end=False, action={'name': 'say', 'body': 'Hello'})
        self.assertEqual(output.content, [{'text': 'Hello', 'reference': 'Greeting'}])

    def test_output_end(self):
        output = Output(content=[{'text': 'Goodbye', 'reference': 'Farewell'}], end=True, action={'name': 'say', 'body': 'Goodbye'})
        self.assertEqual(output.end, True)

    def test_output_action(self):
        output = Output(content=[{'text': 'Hello', 'reference': 'Greeting'}], end=False, action={'name': 'say', 'body': 'Hello'})
        self.assertEqual(output.action, {'name': 'say', 'body': 'Hello'})

if __name__ == '__main__':
    unittest.main()
