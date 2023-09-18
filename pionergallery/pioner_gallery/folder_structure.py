import os
import json

EXCLUDED_FOLDERS = ["vendor", "venv", "__pycache__"]


def create_structure(directory):
    structure = {}
    for item in os.listdir(directory):
        if item not in EXCLUDED_FOLDERS:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                structure[item] = None
            elif os.path.isdir(item_path):
                structure[item] = create_structure(item_path)
    return structure


# project_path = input("Enter the path to your Django project: ")
project_path = './'
project_structure = create_structure(project_path)
output = json.dumps(project_structure, indent=4)
print(output)
