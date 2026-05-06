class HashPair:
    """保存"""

    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, capacity=64):
        self._capacity = capacity
        self._buckets = []
        self._size = 0

        for i in range(capacity):
            self._buckets.append([])

    def _hash(self, key):
        return hash(key) % self._capacity

    def put(self, key, value):
        index = self._hash(key)
        bucket = self._buckets[index]

        for pair in bucket:
            if pair.key == key:
                pair.value = value
                return

        bucket.append(HashPair(key, value))
        self._size += 1

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self._buckets[index]

        for pair in bucket:
            if pair.key == key:
                return pair.value

        return default

    def remove(self, key):
        index = self._hash(key)
        bucket = self._buckets[index]

        i = 0
        while i < len(bucket):
            if bucket[i].key == key:
                bucket.pop(i)
                self._size -= 1
                return True
            i += 1

        return False

    def contains(self, key):
        index = self._hash(key)
        bucket = self._buckets[index]

        for pair in bucket:
            if pair.key == key:
                return True

        return False

    def size(self):
        return self._size

    def __len__(self):
        return self._size

    def keys(self):
        result = []

        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair.key)

        return result

    def values(self):
        result = []

        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair.value)

        return result
