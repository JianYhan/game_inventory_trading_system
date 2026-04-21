"""
DoublyLinkedList 单元测试

TDD 原则：
1. 测试空链表的行为
2. 测试 append/prepend/remove 操作
3. 测试双向链接完整性
"""

import pytest
from src.data_structures.linked_list import DoublyLinkedList, Node


class TestLinkedListCreation:
    """测试链表创建"""

    def test_empty_list(self, empty_linked_list):
        """空链表创建"""
        assert len(empty_linked_list) == 0
        assert list(empty_linked_list) == []

    def test_node_creation(self):
        """节点创建"""
        node = Node("data")
        assert node.data == "data"
        assert node.prev is None
        assert node.next is None


class TestLinkedListAppend:
    """测试尾部添加"""

    def test_append_to_empty(self, empty_linked_list):
        """添加到空链表"""
        empty_linked_list.append("first")
        assert len(empty_linked_list) == 1
        assert list(empty_linked_list) == ["first"]

    def test_append_multiple(self, populated_linked_list):
        """添加多个元素"""
        assert len(populated_linked_list) == 3
        assert list(populated_linked_list) == [10, 20, 30]

    def test_append_updates_tail(self, empty_linked_list):
        """append 更新尾指针"""
        empty_linked_list.append(1)
        empty_linked_list.append(2)
        # 应该可以通过尾指针反向遍历
        assert empty_linked_list.to_reversed_list() == [2, 1]


class TestLinkedListPrepend:
    """测试头部添加"""

    def test_prepend_to_empty(self, empty_linked_list):
        """前置添加到空链表"""
        empty_linked_list.prepend("first")
        assert len(empty_linked_list) == 1
        assert list(empty_linked_list) == ["first"]

    def test_prepend_updates_head(self, populated_linked_list):
        """prepend 更新头指针"""
        populated_linked_list.prepend(5)
        assert list(populated_linked_list) == [5, 10, 20, 30]

    def test_prepend_and_append_mixed(self, empty_linked_list):
        """混合使用 prepend 和 append"""
        empty_linked_list.append(20)    # [20]
        empty_linked_list.prepend(10)   # [10, 20]
        empty_linked_list.append(30)    # [10, 20, 30]
        empty_linked_list.prepend(5)    # [5, 10, 20, 30]

        assert list(empty_linked_list) == [5, 10, 20, 30]


class TestLinkedListRemove:
    """测试删除操作"""

    def test_remove_existing(self, populated_linked_list):
        """删除存在的元素"""
        removed = populated_linked_list.remove(20)
        assert removed is True
        assert len(populated_linked_list) == 2
        assert list(populated_linked_list) == [10, 30]

    def test_remove_non_existing(self, populated_linked_list):
        """删除不存在的元素"""
        removed = populated_linked_list.remove(999)
        assert removed is False
        assert len(populated_linked_list) == 3

    def test_remove_head(self, populated_linked_list):
        """删除头节点"""
        populated_linked_list.remove(10)
        assert list(populated_linked_list) == [20, 30]

    def test_remove_tail(self, populated_linked_list):
        """删除尾节点"""
        populated_linked_list.remove(30)
        assert list(populated_linked_list) == [10, 20]
        assert populated_linked_list.to_reversed_list() == [20, 10]

    def test_remove_only_element(self, empty_linked_list):
        """删除唯一元素"""
        empty_linked_list.append("only")
        empty_linked_list.remove("only")
        assert len(empty_linked_list) == 0


class TestLinkedListBidirectional:
    """测试双向链接完整性"""

    def test_reverse_traversal(self, populated_linked_list):
        """反向遍历"""
        reversed_list = populated_linked_list.to_reversed_list()
        assert reversed_list == [30, 20, 10]

    def test_links_after_append(self, empty_linked_list):
        """append 后链接正确"""
        empty_linked_list.append(1)
        empty_linked_list.append(2)
        empty_linked_list.append(3)

        # 正向遍历
        assert empty_linked_list.to_list() == [1, 2, 3]
        # 反向遍历
        assert empty_linked_list.to_reversed_list() == [3, 2, 1]

    def test_links_after_prepend(self, empty_linked_list):
        """prepend 后链接正确"""
        empty_linked_list.prepend(3)
        empty_linked_list.prepend(2)
        empty_linked_list.prepend(1)

        assert empty_linked_list.to_list() == [1, 2, 3]
        assert empty_linked_list.to_reversed_list() == [3, 2, 1]

    def test_links_after_remove(self, populated_linked_list):
        """remove 后链接正确"""
        populated_linked_list.remove(20)

        assert populated_linked_list.to_list() == [10, 30]
        assert populated_linked_list.to_reversed_list() == [30, 10]


class TestLinkedListIteration:
    """测试迭代器"""

    def test_iteration_order(self, populated_linked_list):
        """迭代顺序正确"""
        items = list(populated_linked_list)
        assert items == [10, 20, 30]

    def test_iteration_empty(self, empty_linked_list):
        """空链表迭代"""
        items = list(empty_linked_list)
        assert items == []

    def test_manual_iteration(self, populated_linked_list):
        """手动迭代"""
        it = iter(populated_linked_list)
        assert next(it) == 10
        assert next(it) == 20
        assert next(it) == 30

        with pytest.raises(StopIteration):
            next(it)


class TestLinkedListIntegration:
    """集成场景测试"""

    def test_complex_sequence(self):
        """复杂操作序列"""
        dll = DoublyLinkedList()

        # 添加 10 个元素
        for i in range(10):
            dll.append(i)

        # 删除偶数
        for i in range(0, 10, 2):
            dll.remove(i)

        # 添加 5 个元素到头部
        for i in range(5):
            dll.prepend(i * 100)

        # 验证正向和反向
        forward = dll.to_list()
        backward = dll.to_reversed_list()

        assert forward == [400, 300, 200, 100, 0, 1, 3, 5, 7, 9]
        assert backward == [9, 7, 5, 3, 1, 0, 100, 200, 300, 400]

    def test_with_complex_objects(self):
        """复杂对象存储"""
        dll = DoublyLinkedList()

        obj1 = {"id": 1, "data": "first"}
        obj2 = {"id": 2, "data": "second"}
        obj3 = {"id": 3, "data": "third"}

        dll.append(obj1)
        dll.append(obj2)
        dll.prepend(obj3)

        assert list(dll) == [obj3, obj1, obj2]
        dll.remove(obj1)
        assert list(dll) == [obj3, obj2]
