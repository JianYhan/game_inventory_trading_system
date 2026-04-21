from __future__ import annotations
from typing import Callable, Any, Optional


class Node:
    def __init__(self, data):
        self.data = data
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size = 0

    def append(self, data) -> Node:
        node = Node(data)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def prepend(self, data) -> Node:
        node = Node(data)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1
        return node

    def remove(self, node: Node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self._size -= 1

    def find(self, predicate: Callable[[Any], bool]) -> Optional[Node]:
        current = self.head
        while current:
            if predicate(current.data):
                return current
            current = current.next
        return None

    def size(self) -> int:
        return self._size

    def iter(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def to_list(self) -> list:
        return list(self.iter())

    def __len__(self):
        return self._size
