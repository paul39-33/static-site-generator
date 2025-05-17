import unittest

from blocks import *

class TestTextNode(unittest.TestCase):
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

    def test_markdown_to_blocks3(self):
        md = "\n\nFirst block\n\n\n\nSecond block\n   \n\nThird block with   spaces\n\n"

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block with   spaces"
            ]
        )

    def test_block_to_block_type_heading(self):
        block = "# Welcome Adventurer"

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = """```
def roar():
    print("RAWR")
```"""
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_unordered(self):
        block = """- Sword
- Shield
- Potion"""
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered(self):
        block = """1. Enter cave
2. Find treasure
3. Escape"""
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is just some regular text about questing."

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()