import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_none(self):
        node = TextNode("This is a test node", TextType.BOLD, None)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_diff(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.LINK)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()