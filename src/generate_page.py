from blocks import *
from split_functions import *
from htmlnode import *
from textnode import *
import os
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    md_file = open(from_path, "r")
    md_content = md_file.read()
    print(f"*******MD_CONTENT: {md_content}")

    template_file = open(template_path, "r")
    template_content = template_file.read()
    print(f"*******TEMPLATE_CONTENT: {template_content}\n\n")

    md_html = markdown_to_html_node(md_content).to_html()

    print(f"md_html: {md_html}")

    title = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", md_html)

    print(f"=====TEMPLATE CONTENT: {template_content}")

    #get the result file name
    dest_path_dir = os.path.dirname(dest_path)
    print(f"dest_path: {dest_path}")
    print(f"dest_path_dir: {dest_path_dir}")
    file_name = dest_path.name
    print(f"file_name: {file_name}")

    #if there is no old file with similar name
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
        with open(dest_path, 'x') as f:
            f.write(template_content)
            print(f"new file new dir created: {file_name}")
            return

    #if there is a file with similar name
    if os.path.exists(dest_path_dir):
        if not os.path.exists(dest_path):
            with open(dest_path, 'x') as f:
                f.write(template_content)
                print(f"new file created: {file_name}")
                return
        else:
            with open(dest_path, 'w') as f:
                f.write(template_content)
                print(f"file overwrote: {file_name}")
                return

    
    