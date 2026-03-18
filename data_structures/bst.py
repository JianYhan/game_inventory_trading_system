from __future__ import annotations
from typing import Optional, Any


class BSTNode:
    def __init__(self, key: float, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BinarySearchTree:
    """BST keyed on price — used for market price-sorted search."""
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: float, value: Any = None):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node: Optional[BSTNode], key: float, value: Any) -> BSTNode:
        if node is None:
            return BSTNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value  # update
        return node

    def search(self, key: float) -> Optional[Any]:
        node = self._search(self.root, key)
        return node.value if node else None

    def _search(self, node: Optional[BSTNode], key: float) -> Optional[BSTNode]:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key: float):
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[BSTNode], key: float) -> Optional[BSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # replace with in-order successor
            successor = self._min_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete(node.right, successor.key)
        return node

    def _min_node(self, node: BSTNode) -> BSTNode:
        while node.left:
            node = node.left
        return node

    def inorder(self):
        yield from self._inorder(self.root)

    def _inorder(self, node: Optional[BSTNode]):
        if node:
            yield from self._inorder(node.left)
            yield (node.key, node.value)
            yield from self._inorder(node.right)

    def range_query(self, low: float, high: float):
        """Yield all (key, value) where low <= key <= high."""
        yield from self._range(self.root, low, high)

    def _range(self, node: Optional[BSTNode], low: float, high: float):
        if node is None:
            return
        if low < node.key:
            yield from self._range(node.left, low, high)
        if low <= node.key <= high:
            yield (node.key, node.value)
        if high > node.key:
            yield from self._range(node.right, low, high)
