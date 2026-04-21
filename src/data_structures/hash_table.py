class HashTable:
    def __init__(self, capacity=64):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _hash(self, key):
        return hash(key) % self._capacity

    def put(self, key, value):
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self._buckets[idx].append([key, value])
        self._size += 1

    def get(self, key, default=None):
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                return pair[1]
        return default

    def remove(self, key):
        idx = self._hash(key)
        for i, pair in enumerate(self._buckets[idx]):
            if pair[0] == key:
                self._buckets[idx].pop(i)
                self._size -= 1
                return True
        return False

    def contains(self, key):
        return self.get(key) is not None

    def __len__(self):
        return self._size

    def keys(self):
        result = []
        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair[0])
        return result

    def values(self):
        result = []
        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair[1])
        return result
