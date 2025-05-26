from textnode import *
from htmlnode import *
from blocks import *
from generate_page import *
import os
import shutil
from pathlib import Path

def main():

    #delete public dir before remaking it
    source_dir = os.path.abspath("static")
    target_dir = os.path.abspath("public")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    os.mkdir(target_dir)
    copy_files(source_dir, target_dir)

    '''#get absolute path to the necessary files
    content_src = get_path("content", "index.md")
    template_path = get_path(None, "template.html")
    content_dest = get_path("public", "index.html")
    generate_page(content_src, template_path, content_dest)

    #blog glorfindel
    glorfindel_src = get_path("content/blog/glorfindel", "index.md")
    glorfindel_dest = get_path("public/blog/glorfindel", "index.html")

    #blog tom
    tom_src = get_path("content/blog/tom", "index.md")
    tom_dest = get_path("public/blog/tom", "index.html")

    #blog majesty
    majesty_src = get_path("content/blog/majesty", "index.md")
    majesty_dest = get_path("public/blog/majesty", "index.html")

    #contact
    contact_src = get_path("content/contact", "index.md")
    contact_dest = get_path("public/contact", "index.html")

    generate_page(glorfindel_src, template_path, glorfindel_dest)
    generate_page(tom_src, template_path, tom_dest)
    generate_page(majesty_src, template_path, majesty_dest)
    generate_page(contact_src, template_path, contact_dest)'''

    generate_pages_recursive(
        "/home/paulus/repos/bootdev/static-site-generator/content",
        "/home/paulus/repos/bootdev/static-site-generator/template.html",
        "/home/paulus/repos/bootdev/static-site-generator/public"
    )



def copy_files(source, target):
    path = source

    print(f"src : {source}, target: {target}")
    #Raise error if dir doesn't exist
    if not os.path.exists(source) or not os.path.exists(target):
        raise NameError("Path not exists!")
    
    print(f"src files: {os.listdir(source)}, target files: {os.listdir(target)}")

    for item in os.listdir(source):
        print(f"curr item: {item}")
    
        #if current item is a dir
        if os.path.isdir(os.path.join(source, item)):
            #new path for recursion, create new dir in target
            next_path = os.path.join(source, item)
            new_dir = os.path.join(target, item)
            os.mkdir(new_dir)
            copy_files(next_path, new_dir)
    
        else:
            #if current item is a file
            file_loc = os.path.join(source, item)
            shutil.copy(file_loc, target)
        
    return 

def get_path(dir_name=None, file_name=None):
    print(f"dir_name: {dir_name}, file_name: {file_name}")
    '''
    How to use:
        if current directory is in static-site/src/main.py and wants to target static-site/content/index.md
        then call get_path("content", "index.md")
    '''
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    if not dir_name:
        target_path = (script_dir.parent / file_name).resolve()
        return target_path
    target_path = (script_dir.parent / dir_name / file_name).resolve()
    return target_path


    

        



if __name__ == "__main__":
    main()