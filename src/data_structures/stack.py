class StackNode:
    """栈节点 - 单向链表节点"""
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """栈 - 后进先出 (LIFO)
    使用单向链表实现，头插/头删
    """
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, item):
        """入栈 - 头插法"""
        node = StackNode(item)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self):
        """出栈 - 头删法"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data

    def peek(self):
        """查看栈顶元素"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._top.data

    def is_empty(self):
        return self._top is None

    def __len__(self):
        return self._size

    def to_list(self):
        """导出为列表（用于遍历）"""
        result = []
        current = self._top
        while current:
            result.append(current.data)
            current = current.next
        return result
