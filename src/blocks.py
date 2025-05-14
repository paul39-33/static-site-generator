from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    clean_excess_newlines = re.sub(r'\n{3,}', '\n\n', markdown)
    split_the_newlines = clean_excess_newlines.split('\n\n')
    final_result = []
    for stuff in split_the_newlines:
        cleaned = stuff.strip()
        if cleaned:
            final_result.append(cleaned)
    print(f"result: {final_result}")
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

    
    

