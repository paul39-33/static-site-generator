from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        return self.text == target.text and self.text_type == target.text_type and self.url == target.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return HTMLNode(None, text_node.text, [])
        case TextType.BOLD:
            return HTMLNode('b', children=[LeafNode(None, text_node.text)])
        case TextType.ITALIC:
            return HTMLNode('i', children=[LeafNode(None, text_node.text)])
        case TextType.CODE:
            return HTMLNode('code', children=[LeafNode(None, text_node.text)])
        case TextType.LINK:
            return HTMLNode('a', children=[LeafNode(None, text_node.text)], props={'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', None, {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception("Unknown text type.")


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


    