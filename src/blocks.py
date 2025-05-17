from textnode import *
from split_functions import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

#Takes markdown texts and return a list of blocks
def markdown_to_blocks(markdown):
    clean_excess_newlines = re.sub(r'\n{3,}', '\n\n', markdown)
    split_the_newlines = clean_excess_newlines.split('\n\n')
    final_result = []
    for stuff in split_the_newlines:
        cleaned = stuff.strip()
        if cleaned:
            final_result.append(cleaned)

    return final_result

def block_to_block_type(block):
    lines = block.split('\n')
    
    if re.match(r"^#{1,6}\s", lines[0]):
        return BlockType.HEADING
    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(lines[i-1].startswith(f"{i}. ") for i in range(1, len(lines)+1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

#Takes text and return a list of HTMLNode(s) child for every block type except code type
def text_to_children(text):

    print(f"=========TEXT: {text}")
    #remove \n
    cleaned_text = text.replace('\n', ' ')

    #detect inline styling and returns a list of TextNodes
    child_nodes = text_to_textnodes(cleaned_text)

    print(f"=========CHILD_NODES BEFORE: {child_nodes}")
    child_html_nodes = []
    for node in child_nodes:
        new_node = text_node_to_html_node(node)
        child_html_nodes.append(new_node)
    
    print(f"=========CHILD_NODES AFTER: {child_html_nodes}")

    return child_html_nodes

def markdown_to_html_node(markdown):
    print(f"=========MARKDOWN: {markdown}")
    #turn markdown text into list of blocks
    markdown_blocks = markdown_to_blocks(markdown)
    print(f"=========MARKDOWN_BLOCKS: {markdown_blocks}")
    block_nodes = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            #check heading level (h1-h6)
            match = re.match(r"^(#{1,6})\s+(.*)", block)
            #Example "### My Title", then returns match.group(1) = "###"
            #and match.group(2) = "My Title"
            heading_level = len(match.group(1))
            block_node = HTMLNode(f'h{heading_level}', children=[text_to_children(match.group(2))])
            print(f"=========BLOCK_NODE_HEADING : {block_node}")
            block_nodes.append(block_node)

        if block_type == BlockType.CODE:
            lines = block.split("\n")
            print(f"code_lines_split: {lines}")
            content = "\n".join(lines[1:-1])
            content += "\n"
            code_text = HTMLNode('code', children=[LeafNode(None, content)])
            block_node = HTMLNode('pre', children=[code_text])
            #block_node = HTMLNode('code', children=[html_node])
            print(f"=========BLOCK_NODE_CODE : {block_node}")
            block_nodes.append(block_node)

        if block_type == BlockType.QUOTE:
            lines = block.split("\n")

            for line in lines:
                #remove the ">" and also a space after it
                if line.startswith(">"):
                    line = line[1:]
                    if line.startswith(" "):
                        line = line[1:]

            content = " ".join(lines)
            block_node = HTMLNode('blockquote', children=[text_to_children(content)])
            print(f"=========BLOCK_NODE_QUOTE : {block_node}")
            block_nodes.append(block_node)

        if block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            ul_child_nodes = []
            for line in lines:
                line = line[2:]
                line_node = HTMLNode('li', text_to_children(line))
                ul_child_nodes.append(line_node)
            block_node = HTMLNode('ul', children=[ul_child_nodes])
            print(f"=========BLOCK_NODE_UL : {block_node}")
            block_nodes.append(block_node)
        
        if block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            ol_child_nodes = []
            for line in lines:
                line = line[3:]
                line_node = HTMLNode('li', text_to_children(line))
                ol_child_nodes.append(line_node)
            block_node = HTMLNode('ol', children=[ol_child_nodes])
            print(f"=========BLOCK_NODE_OL : {block_node}")
            block_nodes.append(block_node)
        
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            content = ' '.join(lines)
            block_node = HTMLNode('p', children=text_to_children(content))
            print(f"=========BLOCK_NODE_PARAGRAPH : {block_node}")
            block_nodes.append(block_node)

    print(f"FINAL BLOCK_NODES: {HTMLNode('div', children=block_nodes)}")

    return HTMLNode('div', children=block_nodes)
            





    
    

