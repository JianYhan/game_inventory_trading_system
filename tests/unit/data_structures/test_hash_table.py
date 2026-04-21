"""
HashTable 单元测试

TDD 原则：
1. 测试空哈希表的行为
2. 测试 put/get/remove 操作
3. 测试哈希冲突处理
"""

import pytest
from src.data_structures.hash_table import HashTable


class TestHashTableCreation:
    """测试哈希表创建"""

    def test_default_capacity(self):
        """默认容量"""
        ht = HashTable()
        assert ht._buckets is not None

    def test_custom_capacity(self):
        """自定义容量"""
        ht = HashTable(capacity=32)
        assert len(ht._buckets) == 32

    def test_empty_table(self, empty_hash_table):
        """空哈希表"""
        assert empty_hash_table.get("any_key") is None
        assert empty_hash_table.keys() == []


class TestHashTablePutGet:
    """测试 put/get 操作"""

    def test_put_and_get(self, empty_hash_table):
        """存储和获取"""
        empty_hash_table.put("key", "value")
        assert empty_hash_table.get("key") == "value"

    def test_get_non_existing(self, empty_hash_table):
        """获取不存在的键"""
        assert empty_hash_table.get("non_existing") is None
        assert empty_hash_table.get("non_existing", "default") == "default"

    def test_put_multiple(self, populated_hash_table):
        """存储多个键值"""
        assert populated_hash_table.get("name") == "TestPlayer"
        assert populated_hash_table.get("level") == 10
        assert populated_hash_table.get("gold") == 1000.0

    def test_overwrite_existing(self, empty_hash_table):
        """覆盖已存在的键"""
        empty_hash_table.put("key", "old_value")
        empty_hash_table.put("key", "new_value")
        assert empty_hash_table.get("key") == "new_value"


class TestHashTableCollision:
    """测试哈希冲突处理"""

    def test_collision_handling(self, empty_hash_table):
        """拉链法处理冲突"""
        # 使用相同哈希的键（假设冲突发生）
        empty_hash_table.put("a", 1)
        empty_hash_table.put("b", 2)

        # 两个值都应该能获取到
        assert empty_hash_table.get("a") == 1
        assert empty_hash_table.get("b") == 2

    def test_collision_with_same_bucket(self):
        """强制冲突：相同哈希值的键"""
        ht = HashTable(capacity=1)  # 只有一个桶，必然冲突

        ht.put("key1", "value1")
        ht.put("key2", "value2")
        ht.put("key3", "value3")

        assert ht.get("key1") == "value1"
        assert ht.get("key2") == "value2"
        assert ht.get("key3") == "value3"


class TestHashTableRemove:
    """测试 remove 操作"""

    def test_remove_existing(self, populated_hash_table):
        """删除存在的键"""
        populated_hash_table.remove("name")
        assert populated_hash_table.get("name") is None

    def test_remove_non_existing(self, empty_hash_table):
        """删除不存在的键（不报错）"""
        empty_hash_table.remove("non_existing")  # 应该无异常
        assert empty_hash_table.get("non_existing") is None

    def test_remove_does_not_affect_others(self, populated_hash_table):
        """删除不影响其他键"""
        populated_hash_table.remove("name")
        assert populated_hash_table.get("level") == 10
        assert populated_hash_table.get("gold") == 1000.0


class TestHashTableKeysValues:
    """测试 keys/values 方法"""

    def test_keys(self, populated_hash_table):
        """获取所有键"""
        keys = populated_hash_table.keys()
        assert "name" in keys
        assert "level" in keys
        assert "gold" in keys

    def test_values(self, populated_hash_table):
        """获取所有值"""
        values = populated_hash_table.values()
        assert "TestPlayer" in values
        assert 10 in values
        assert 1000.0 in values

    def test_empty_keys_values(self, empty_hash_table):
        """空表的 keys/values"""
        assert empty_hash_table.keys() == []
        assert empty_hash_table.values() == []


class TestHashTableWithDifferentTypes:
    """测试不同类型键值"""

    def test_integer_keys(self, empty_hash_table):
        """整数键"""
        empty_hash_table.put(1, "one")
        empty_hash_table.put(2, "two")
        assert empty_hash_table.get(1) == "one"
        assert empty_hash_table.get(2) == "two"

    def test_mixed_types(self, empty_hash_table):
        """混合类型值"""
        empty_hash_table.put("string", "text")
        empty_hash_table.put("number", 42)
        empty_hash_table.put("list", [1, 2, 3])
        empty_hash_table.put("dict", {"a": 1})

        assert empty_hash_table.get("string") == "text"
        assert empty_hash_table.get("number") == 42
        assert empty_hash_table.get("list") == [1, 2, 3]
        assert empty_hash_table.get("dict") == {"a": 1}


class TestHashTableIntegration:
    """集成场景测试"""

    def test_sequence_operations(self):
        """连续操作序列"""
        ht = HashTable(capacity=4)

        # 插入 100 个键
        for i in range(100):
            ht.put(f"key{i}", i * 10)

        # 验证全部可读
        for i in range(100):
            assert ht.get(f"key{i}") == i * 10

        # 删除偶数键
        for i in range(0, 100, 2):
            ht.remove(f"key{i}")

        # 验证删除成功，奇数键还在
        for i in range(100):
            if i % 2 == 0:
                assert ht.get(f"key{i}") is None
            else:
                assert ht.get(f"key{i}") == i * 10

    def test_update_operations(self):
        """更新操作序列"""
        ht = HashTable()

        # 多次更新同一个键
        for i in range(10):
            ht.put("counter", i)

        assert ht.get("counter") == 9

    def test_with_complex_objects(self):
        """复杂对象存储"""
        ht = HashTable()

        player = {"id": "p1", "name": "Alice", "gold": 1000}
        items = [{"id": 1}, {"id": 2}]

        ht.put("player", player)
        ht.put("items", items)

        assert ht.get("player")["name"] == "Alice"
        assert len(ht.get("items")) == 2
