import unittest

from src.logic import get_node
from src.logic.main import Loop


class TestLoop(unittest.TestCase):
    def setUp(self):
        self.loop = Loop()

    def test_str(self):
        expected_str = str(self.loop)
        self.assertEqual(str(self.loop), expected_str)

    def test_main_loop(self):
        self.assertTrue(isinstance(self.loop.main_loop, Loop))

    def test_get_node_with_loop(self):
        node = get_node(self.loop)
        self.assertEqual(node, self.loop)

    def test_get_node_with_other_input(self):
        node = get_node("other")
        self.assertNotEqual(node, self.loop)


if __name__ == '__main__':
    unittest.main()
