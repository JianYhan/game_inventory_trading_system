class TreeNode:
    def __init__(self, value, data=None):
        self.value = value
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child


class Tree:
    def __init__(self, root_value, root_data=None):
        self.root = TreeNode(root_value, root_data)

    def insert(self, parent_value, value, data=None):
        parent = self.find(parent_value)
        if parent is None:
            raise ValueError(f"Parent node '{parent_value}' not found")
        return parent.add_child(TreeNode(value, data))

    def find(self, value):
        for node in self.traverse():
            if node.value == value:
                return node
        return None

    def traverse(self):
        yield from self._preorder(self.root)

    def _preorder(self, node):
        yield node
        for child in node.children:
            yield from self._preorder(child)

    def to_list(self):
        return [node.value for node in self.traverse()]

    def to_lines(self):
        lines = []
        self._collect_lines(self.root, 0, lines)
        return lines

    def _collect_lines(self, node, depth, lines):
        lines.append(f"{'  ' * depth}- {node.value}")
        for child in node.children:
            self._collect_lines(child, depth + 1, lines)
