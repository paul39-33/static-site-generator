from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
            
        if text.find(delimiter) == -1:
            new_nodes.append(node)
            continue
            
        start_index = text.find(delimiter)
        end_index = text.find(delimiter, start_index + len(delimiter))

        if end_index == -1:
            raise Exception("Closing delimiter not found.")

        start_text = text[:start_index]
        mid_text = text[start_index : end_index + len(delimiter)].replace(delimiter, '')
        end_text = text[end_index + len(delimiter):]

        if start_text:
            new_nodes.append(TextNode(start_text, TextType.TEXT))

        if mid_text:
            new_nodes.append(TextNode(mid_text, text_type))
        
        if end_text:
            next_node = split_nodes_delimiter([TextNode(end_text, TextType.TEXT)], delimiter, text_type)
            new_nodes.extend(next_node)

    return new_nodes



        
            
