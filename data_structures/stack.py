from typing import Any, Optional


class Stack:
    """LIFO stack — used for undo/redo of inventory operations."""
    def __init__(self):
        self._data: list = []

    def push(self, item: Any):
        self._data.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __len__(self):
        return len(self._data)
