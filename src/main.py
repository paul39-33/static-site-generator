from textnode import *
from htmlnode import *
from blocks import *
import os
import shutil

def main():

    #delete public dir before remaking it
    source_dir = os.path.abspath("static")
    target_dir = os.path.abspath("public")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    os.mkdir(target_dir)
    copy_files(source_dir, target_dir)



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




    

        



if __name__ == "__main__":
    main()