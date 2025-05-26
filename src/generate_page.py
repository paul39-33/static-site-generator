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
    #print(f"*******MD_CONTENT: {md_content}")

    template_file = open(template_path, "r")
    template_content = template_file.read()
    #print(f"*******TEMPLATE_CONTENT: {template_content}\n\n")

    md_html = markdown_to_html_node(md_content).to_html()

    #print(f"md_html: {md_html}")

    title = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", md_html)

    print(f"=====TEMPLATE CONTENT: {template_content}")

    #get the result file name
    dest_path_dir = os.path.dirname(dest_path)
    print(f"dest_path: {dest_path}")
    print(f"dest_path_dir: {dest_path_dir}")
    file_name = Path(dest_path).name
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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"dir_path_cont: {dir_path_content}, dest_dir: {dest_dir_path}")

    for item in os.listdir(dir_path_content):
        print(f"curr_item: {item}")
        
        if os.path.isdir(os.path.join(dir_path_content, item)):
            next_dir_path = Path(dir_path_content) / item
            next_dest_path = Path(dest_dir_path) / item
            #check if dir of same name not exist in dest path
            if not os.path.exists(next_dest_path):
                os.mkdir(next_dest_path)
            generate_pages_recursive(next_dir_path, template_path, next_dest_path)
        
        else:
            src_file_path = Path(dir_path_content) / item
            file_name = src_file_path.name
            
            #change file name from .md to .html
            dest_file_name = file_name.replace(".md", ".html")
            dest_file_path = os.path.join(dest_dir_path, dest_file_name)
            
            #generate the html file from md file
            generate_page(src_file_path, template_path, dest_file_path)

    return
