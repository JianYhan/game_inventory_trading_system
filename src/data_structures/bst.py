class TreeNode:
    """定义节点"""
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self._root = None

    def insert(self, key, data=None):
        new_node = TreeNode(key, data)

        if self._root is None:
            self._root = new_node
            return

        current = self._root
        while current is not None:
            if key == current.key:
                current.data = data
                return

            if key < current.key:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def search(self, key):
        current = self._root

        while current is not None:
            if key == current.key:
                return current.data
            if key < current.key:
                current = current.left
            else:
                current = current.right

        return None

    def inorder(self):
        """先序遍历，用recursive tree"""
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return

        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    def inorder_items(self):
        result = []
        self._inorder_items(self._root, result)
        return result

    def _inorder_items(self, node, result):
        if node is None:
            return

        self._inorder_items(node.left, result)
        result.append((node.key, node.data))
        self._inorder_items(node.right, result)

    def range_query(self, low, high):
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
