import unittest

from htmlnode import HTMLNode, LeafNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_multiple_attributes(self):
        # Create a link with href, class, and id attributes
        node = LeafNode(
            "a", 
            "Visit Boot.dev", 
            {
                "href": "https://boot.dev",
                "class": "external-link primary-btn",
                "id": "learn-coding-link",
                "target": "_blank"
            }
        )
        
        # Check the rendered HTML
        expected_html = '<a href="https://boot.dev" class="external-link primary-btn" id="learn-coding-link" target="_blank">Visit Boot.dev</a>'
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()