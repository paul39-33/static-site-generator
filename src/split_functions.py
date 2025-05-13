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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        text = node.text 

        images = extract_markdown_images(text)

        if images == []:
            new_nodes.append(node)
            continue

        for alt_text, image_url in images:

            image_markdown = f"![{alt_text}]({image_url})"
            parts = text.split(image_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            if len(parts) > 1:
                text = parts[1]
            else:
                text = ''

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        text = node.text 

        links = extract_markdown_links(text)

        if links == []:
            new_nodes.append(node)
            continue

        for alt_text, link_url in links:

            link_markdown = f"[{alt_text}]({link_url})"
            parts = text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.LINK, link_url))

            if len(parts) > 1:
                text = parts[1]
            else:
                text = ''

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes



        
            
