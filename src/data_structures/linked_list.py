class Node:
    """定义node"""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class LinkedListIterator:
    """简单的iterator"""

    def __init__(self, start_node):
        self.current = start_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration

        data = self.current.data
        self.current = self.current.next
        return data


class DoublyLinkedList:
    """简单的双向列表"""

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        return LinkedListIterator(self._head)

    def append(self, data):
        new_node = Node(data)

        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def prepend(self, data):
        new_node = Node(data)

        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node

        self._size += 1

    def remove(self, data):
        current = self._head

        while current is not None:
            if current.data == data:
                previous_node = current.prev
                next_node = current.next

                if previous_node is None:
                    self._head = next_node
                else:
                    previous_node.next = next_node

                if next_node is None:
                    self._tail = previous_node
                else:
                    next_node.prev = previous_node

                self._size -= 1
                return True

            current = current.next

        return False

    def to_list(self):
        result = []
        current = self._head

        while current is not None:
            result.append(current.data)
            current = current.next

        return result

    def to_reversed_list(self):
        result = []
        current = self._tail

        while current is not None:
            result.append(current.data)
            current = current.prev

        return result
