class QueueNode:
    """队列节点 - 单向链表节点"""
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """队列 - 先进先出 (FIFO)
    使用单向链表实现，带尾指针，尾插/头删
    """
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        """入队 - 尾插法"""
        node = QueueNode(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        """出队 - 头删法"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return data

    def peek(self):
        """查看队首元素"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._head.data

    def is_empty(self):
        return self._head is None

    def __len__(self):
        return self._size

    def to_list(self):
        """导出为列表（用于遍历）"""
        result = []
        current = self._head
        while current:
            result.append(current.data)
            current = current.next
        return result
