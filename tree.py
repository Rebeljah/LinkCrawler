
class TreeNode:
    def __init__(self, page_title, page_url, parent_node, depth: int):
        self.depth = depth
        self.page_title = page_title
        self.url = page_url

        if parent_node:
            parent_node.children.append(self)
        self.children = []


class Tree:
    def __init__(self, branching: int, max_depth: int):
        self.branching = branching  # how many urls to crawl on each page
        self.max_depth = max_depth  # how deep the tree should go

        self.nodes: set[TreeNode] = set()
        self.head_node = None

    def add_head_node(self, title, url) -> TreeNode:
        self.head_node = TreeNode(title, url, None, 0)
        self.nodes.add(self.head_node)
        return self.head_node

    def add_child_node(self, title, url, parent_node) -> TreeNode:
        node = TreeNode(title, url, parent_node, parent_node.depth + 1)
        self.nodes.add(node)
        return node
