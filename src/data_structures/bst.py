class TreeNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self._root = None

    def insert(self, key, data=None):
        self._root = self._insert(self._root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            return TreeNode(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data
        return node

    def search(self, key):
        return self._search(self._root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder(self):
        """中序遍历，返回按key排序的 key 列表"""
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def inorder_items(self):
        """中序遍历，返回 (key, data) 列表"""
        result = []
        self._inorder_items(self._root, result)
        return result

    def _inorder_items(self, node, result):
        if node:
            self._inorder_items(node.left, result)
            result.append((node.key, node.data))
            self._inorder_items(node.right, result)

    def range_query(self, low, high):
        """范围查询，返回指定范围内的 data 列表"""
        result = []
        self._range(self._root, low, high, result)
        return result

    def _range(self, node, low, high, result):
        if node is None:
            return
        if low < node.key:
            self._range(node.left, low, high, result)
        if low <= node.key <= high:
            result.append(node.data)
        if node.key < high:
            self._range(node.right, low, high, result)
