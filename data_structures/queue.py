from collections import deque
from typing import Any


class Queue:
    """FIFO queue — used for pending market orders."""
    def __init__(self):
        self._data: deque = deque()

    def enqueue(self, item: Any):
        self._data.append(item)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __len__(self):
        return len(self._data)

    def iter(self):
        return iter(self._data)
