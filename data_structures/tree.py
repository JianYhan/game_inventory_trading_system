from __future__ import annotations
from typing import Optional, Any


class TreeNode:
    def __init__(self, key: str, value: Any = None):
        self.key = key
        self.value = value
        self.children: list[TreeNode] = []

    def add_child(self, child: TreeNode):
        self.children.append(child)

    def __repr__(self):
        return f"TreeNode({self.key})"


class Tree:
    """General tree — used for category hierarchy of items."""
    def __init__(self, root_key: str, root_value: Any = None):
        self.root = TreeNode(root_key, root_value)

    def find(self, key: str, node: Optional[TreeNode] = None) -> Optional[TreeNode]:
        if node is None:
            node = self.root
        if node.key == key:
            return node
        for child in node.children:
            result = self.find(key, child)
            if result:
                return result
        return None

    def insert(self, parent_key: str, child_key: str, child_value: Any = None) -> bool:
        parent = self.find(parent_key)
        if parent is None:
            return False
        parent.add_child(TreeNode(child_key, child_value))
        return True

    def traverse(self, node: Optional[TreeNode] = None, depth: int = 0):
        if node is None:
            node = self.root
        yield (depth, node)
        for child in node.children:
            yield from self.traverse(child, depth + 1)
