from typing import Any, Optional


class HashTable:
    """Separate-chaining hash table — used for O(1) player/item lookup."""
    def __init__(self, capacity: int = 64):
        self._capacity = capacity
        self._buckets: list[list] = [[] for _ in range(capacity)]
        self._size = 0

    def _hash(self, key: str) -> int:
        return hash(key) % self._capacity

    def put(self, key: str, value: Any):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key: str) -> Optional[Any]:
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: str) -> bool:
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def keys(self):
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def values(self):
        for bucket in self._buckets:
            for _, v in bucket:
                yield v

    def items(self):
        for bucket in self._buckets:
            yield from bucket

    def size(self) -> int:
        return self._size

    def __len__(self):
        return self._size
