import unittest

from textnode import *
from htmlnode import *
from split_functions import *

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text without !image"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a link [to fb](fb.com) and [to youtube](yt.com)"
        )
        print(f"matches : {matches}, type : {type(matches[0])}")
        self.assertListEqual([('to fb', 'fb.com'), ('to youtube', 'yt.com')], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )

    def test_split_image_basic(self):
        node = TextNode(
            "This is an ![image](https://example.com/img.png) in text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Test the result has 3 nodes: text before, image, text after

    def test_split_image_multiple(self):
        node = TextNode(
            "Text with ![first](img1.png) and ![second](img2.png) images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Test the result has 5 nodes

    def test_split_image_at_beginning(self):
        node = TextNode(
            "![start image](img.png) with text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Test the result (should have no text node before the image)

    def test_split_image_at_end(self):
        node = TextNode(
            "Text before ![end image](img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Test the result (should have no text node after the image)

    def test_split_image_empty_node(self):
        node = TextNode(
            "![](img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Test node with empty alt text

    def test_split_link_basic(self):
        node = TextNode(
            "Text with a [link](https://example.com) in the middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test the result has 3 nodes: text before, link, text after

    def test_split_link_multiple(self):
        node = TextNode(
            "This has [one link](https://example.com) and [another](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test the result has 5 nodes

    def test_split_link_at_beginning(self):
        node = TextNode(
            "[First thing](https://example.com) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test the result (should have no text node before the link)

    def test_split_link_at_end(self):
        node = TextNode(
            "Text ending with [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test the result (should have no text node after the link)

    def test_split_link_adjacent(self):
        node = TextNode(
            "Check these: [link1](url1)[link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test adjacent links with no text between

    def test_split_link_no_links(self):
        node = TextNode(
            "This text has no links in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Test that original node is returned unchanged

    def test_split_image_complex_cases(self):
        # Test 1: Multiple nodes in old_nodes - this is a valid test
        node1 = TextNode("First ![img1](url1.png) text", TextType.TEXT)
        node2 = TextNode("Second ![img2](url2.png) text", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        # This should process both nodes, not just the first one
        
        # Test 2: Double check the URL extraction works with extract_markdown_images
        test_text = "Image with ![nested](http://example.com/img(1).png) parentheses"
        images = extract_markdown_images(test_text)
        # Make sure extract_markdown_images correctly finds this image
        print(f"Extracted images: {images}")
        
        # Test 3: Use the actual extraction result for the test
        if images:
            alt_text, url = images[0]
            node = TextNode(test_text, TextType.TEXT)
            new_nodes = split_nodes_image([node])
            # Verify result based on what extract_markdown_images found

    def test_split_links_reliable(self):
        # Test processing multiple nodes
        node1 = TextNode("First [link1](url1.com) text", TextType.TEXT)
        node2 = TextNode("Second [link2](url2.com) text", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        
        
        # Test what extract_markdown_links actually returns
        links = extract_markdown_links(node1.text)
        
        # Basic check that should pass if your function processes all nodes
        self.assertTrue(len(new_nodes) > 3)  # At minimum we expect results from both nodes

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ], new_nodes
        )
    
    def test_text_to_textnodes_bold_url(self):
        text = "This is a [**bold link**](url)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("**bold link**", TextType.LINK, "url")
            ], new_nodes
        )

    def test_text_to_textnodes_multiple_adjacent(self):
        text = "This is a **bold**`code` so close to [link](url)_italic_ and ![img](url)**bold**"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("code", TextType.CODE),
                TextNode(" so close to ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
                TextNode("bold", TextType.BOLD)
            ], new_nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is a _italic_ paragraph





Soooo many spaces


-Ooooh



-Yeaaa
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a _italic_ paragraph",
                "Soooo many spaces",
                "-Ooooh",
                "-Yeaaa",
            ],
        )


if __name__ == "__main__":
    unittest.main()