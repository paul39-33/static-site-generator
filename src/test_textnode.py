import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import *
from split_delimiter import *

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("This is an image", TextType.IMAGE, "facebook.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "facebook.com", "alt": "This is an image"})
    
    def test_split_delimiter1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_multiple_occurrences(self):
        # Create a node with multiple code blocks
        node = TextNode("This is `code1` and `code2` and `code3` in one string", TextType.TEXT)
        
        # Split it by the backtick delimiter for code
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # We should get 7 nodes: text, code, text, code, text, code, text
        assert len(result) == 7
        
        # Check the content and types of each node
        assert result[0].text == "This is "
        assert result[0].text_type == TextType.TEXT
        
        assert result[1].text == "code1"
        assert result[1].text_type == TextType.CODE
        
        assert result[2].text == " and "
        assert result[2].text_type == TextType.TEXT
        
        assert result[3].text == "code2"
        assert result[3].text_type == TextType.CODE
        
        assert result[4].text == " and "
        assert result[4].text_type == TextType.TEXT
        
        assert result[5].text == "code3"
        assert result[5].text_type == TextType.CODE
        
        assert result[6].text == " in one string"
        assert result[6].text_type == TextType.TEXT

    def test_split_nodes_delimiter_different_delimiters(self):
        # Create a node with bold text
        node = TextNode("Normal text with **bold text** in the middle", TextType.TEXT)
        
        # Split it by the ** delimiter for bold
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # We should get 3 nodes: text, bold, text
        assert len(result) == 3
        
        # Check the content and types of each node
        assert result[0].text == "Normal text with "
        assert result[0].text_type == TextType.TEXT
        
        assert result[1].text == "bold text"
        assert result[1].text_type == TextType.BOLD
        
        assert result[2].text == " in the middle"
        assert result[2].text_type == TextType.TEXT
        
        # Try a more complex example with italic
        node2 = TextNode("This has _one italic_ and _another italic_ phrases", TextType.TEXT)
        result2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        
        # We should get 5 nodes: text, italic, text, italic, text
        assert len(result2) == 5
        
        assert result2[0].text == "This has "
        assert result2[0].text_type == TextType.TEXT
        
        assert result2[1].text == "one italic"
        assert result2[1].text_type == TextType.ITALIC
        
        assert result2[2].text == " and "
        assert result2[2].text_type == TextType.TEXT
        
        assert result2[3].text == "another italic"
        assert result2[3].text_type == TextType.ITALIC
        
        assert result2[4].text == " phrases"
        assert result2[4].text_type == TextType.TEXT


if __name__ == "__main__":
    unittest.main()