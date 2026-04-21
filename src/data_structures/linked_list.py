class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self._head
        while current:
            yield current.data
            current = current.next

    def append(self, data):
        node = Node(data)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, data):
        node = Node(data)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def remove(self, data):
        current = self._head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self._head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self._tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def to_list(self):
        return list(self)

    def to_reversed_list(self):
        result = []
        current = self._tail
        while current:
            result.append(current.data)
            current = current.prev
        return result
