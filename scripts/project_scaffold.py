#!/usr/bin/env python3



# To make the project_scaffold script executable and callable from any folder in a Linux-based system, you can do the following:

# Make the script executable by running the command chmod +x project_scaffold.py
# Move the script to a directory included in the system's PATH environment variable. This allows the script to be executed from any directory without having to specify the full path to the script. For example, you could move the script to /usr/local/bin using the command sudo mv project_scaffold.py /usr/local/bin/
# Once the script is in a directory included in the PATH, you can call it from any directory by simply running project_scaffold command followed by any arguments you want to pass to it.
# Alternatively you can use the environment variable $PATH in the shebang at the start of your script.


# #!/usr/bin/env python3
# This will allow the system to use the python3 in the environment variable $PATH.

import os
from treelib import Tree

def project_scaffold(structure):
    structure = structure.split(',')
    root_folder_path = ""
    for item in structure:
        item = item.strip()
        path = ""
        if '(' in item:
            sub_folders = item.split('(')
            parent = sub_folders[0]
            os.makedirs(parent, exist_ok=True)
            root_folder_path = os.path.abspath(parent)
            for sub_folder in sub_folders[1:]:
                sub_folder = sub_folder.strip(')')
                path += parent + '/' + sub_folder + '/'
                os.makedirs(path, exist_ok=True)
        elif ':' in item:
            sub_folders = item.split(':')
            parent = sub_folders[0]
            os.makedirs(parent, exist_ok=True)
            root_folder_path = os.path.abspath(parent)
            for sub_folder in sub_folders[1:]:
                path += parent + '/' + sub_folder + '/'
                os.makedirs(path, exist_ok=True)
                
        
        else:
            os.makedirs(item, exist_ok=True)
            root_folder_path = os.path.abspath(item)
            
        # view_structure(root_folder_path)
        
        
    # while True:
    #     response = input("Is this correct(yes/no): ")
    #     if response.strip().lower() == "yes":
            
    #         break
    #     elif response.strip().lower() == "no":
    #         structure = input("Enter the folder structure separated by commas and use ( and ) or : for subfolders: ")
    #         project_scaffold(structure)
    #         break
    #     else:
    #         print("Please enter 'yes' or 'no'.")

def view_structure(path):
    tree = Tree()
    tree.create_node("/", "root", data={"path": path})
    for root, dirs, files in os.walk(path):
        parent = tree.get_node(root).identifier
        for dir in dirs:
            tree.create_node(dir, parent=parent, data={"path": os.path.join(root, dir)})
        for file in files:
            tree.create_node(file, parent=parent, data={"path": os.path.join(root, file)})
    tree.show()

if __name__ == '__main__':
    structure = input("Enter the folder structure separated by commas and use ( and ) or : for subfolders: ")
    project_scaffold(structure)

