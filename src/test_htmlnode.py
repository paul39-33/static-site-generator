import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a test", props={'a': 'aaa', 'b': 'bbb'})
        node2 = HTMLNode("p", "This is a test", props={'a': 'aaa', 'b': 'bbb'})
        self.assertEqual(node, node2)

    def test_eq_none(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)

    def test_diff(self):
        node = HTMLNode("p", "This is a test", props={'a': 'aaa', 'b': 'bbb'})
        node2 = HTMLNode("p", "This is a test", props={'c': 'ccc', 'd': 'ddd'})
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()