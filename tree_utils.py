import json
from datetime import datetime
import os

from tree import Tree, TreeNode


def tree_as_dict(node: TreeNode, _temp_dict=None, _tree_dict=None) -> dict:
    """
    Reads a tree into a dictionary
    """
    if _temp_dict is None:  # this runs once at start of copy
        _temp_dict = {}
        _tree_dict = _temp_dict

    _temp_dict[node.page_title] = {}
    page_dict = _temp_dict[node.page_title]
    page_dict['url'] = node.url

    page_dict['links'] = {}
    links_dict = page_dict['links']
    for node in node.children:
        tree_as_dict(node, links_dict)

    return _tree_dict


def save_tree_json(tree: Tree, folder_path: str) -> None:
    """
    Converts the tree into a dictionary and then saves it as a JSON file.

    Creates a filename that uses the page_title of the tree's head node and a
    current timestamp.
    """
    node = tree.head_node

    # convert head node page title to PascalCase and remove non-alpha chars
    head_title: str = node.page_title.title()
    head_title = ''.join(filter(str.isalpha, head_title))

    # generate filename using node title and timestamp
    timestamp = datetime.now().strftime('%Y%b%d%H%M')
    file_name = f"{head_title[:25]}{timestamp}.json"

    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as outfile:
        json.dump(tree_as_dict(node), outfile, indent=3)
