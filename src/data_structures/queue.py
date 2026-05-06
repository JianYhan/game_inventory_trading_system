class QueueNode:
    """队列里的一个节点"""

    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        new_node = QueueNode(item)

        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")

        data = self._head.data
        new_head = self._head.next
        self._head = new_head

        if self._head is None:
            self._tail = None

        self._size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")

        return self._head.data

    def is_empty(self):
        if self._head is None:
            return True
        return False

    def __len__(self):
        return self._size

    def to_list(self):
        result = []
        current = self._head

        while current is not None:
            result.append(current.data)
            current = current.next

        return result
