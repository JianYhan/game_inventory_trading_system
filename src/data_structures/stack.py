class StackNode:
    """栈里一个node"""

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, item):
        new_node = StackNode(item)

        old_top = self._top
        new_node.next = old_top
        self._top = new_node

        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")

        data = self._top.data
        new_top = self._top.next
        self._top = new_top

        self._size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")

        return self._top.data

    def is_empty(self):
        if self._top is None:
            return True
        return False

    def __len__(self):
        return self._size

    def to_list(self):
        result = []
        current = self._top

        while current is not None:
            result.append(current.data)
            current = current.next

        return result
