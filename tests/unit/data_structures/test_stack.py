"""
Stack 单元测试

TDD 原则：
1. 测试空栈的行为
2. 测试入栈/出栈的 LIFO 特性
3. 测试边界情况
"""

import pytest
from src.data_structures.stack import Stack, StackNode


class TestStackBasic:
    """测试栈的基本功能"""

    def test_empty_stack_creation(self, empty_stack):
        """空栈创建后应该为空"""
        assert empty_stack.is_empty()
        assert len(empty_stack) == 0

    def test_push_single_item(self, empty_stack):
        """入栈单个元素"""
        empty_stack.push("item")
        assert not empty_stack.is_empty()
        assert len(empty_stack) == 1
        assert empty_stack.peek() == "item"

    def test_push_multiple_items(self, populated_stack):
        """入栈多个元素，验证 LIFO"""
        assert len(populated_stack) == 3
        # 栈顶应该是最后入栈的
        assert populated_stack.peek() == 3


class TestStackLIFO:
    """测试栈的后进先出特性"""

    def test_pop_order(self, populated_stack):
        """出栈顺序应该是 3, 2, 1"""
        assert populated_stack.pop() == 3
        assert populated_stack.pop() == 2
        assert populated_stack.pop() == 1
        assert populated_stack.is_empty()

    def test_push_then_pop(self, empty_stack):
        """入栈后立即出栈"""
        empty_stack.push("first")
        empty_stack.push("second")

        assert empty_stack.pop() == "second"
        assert empty_stack.pop() == "first"
        assert empty_stack.is_empty()


class TestStackPeek:
    """测试 peek 操作"""

    def test_peek_does_not_remove(self, populated_stack):
        """peek 不移除元素"""
        original_len = len(populated_stack)
        top = populated_stack.peek()

        assert top == 3
        assert len(populated_stack) == original_len  # 长度不变

    def test_peek_empty_stack_raises(self, empty_stack):
        """空栈 peek 应该抛出异常"""
        with pytest.raises(IndexError, match="empty"):
            empty_stack.peek()


class TestStackPop:
    """测试 pop 操作"""

    def test_pop_empty_stack_raises(self, empty_stack):
        """空栈 pop 应该抛出异常"""
        with pytest.raises(IndexError, match="empty"):
            empty_stack.pop()

    def test_pop_returns_correct_value(self, populated_stack):
        """pop 返回正确的值"""
        value = populated_stack.pop()
        assert value == 3
        assert len(populated_stack) == 2


class TestStackNode:
    """测试栈节点"""

    def test_node_creation(self):
        """节点创建"""
        node = StackNode("data")
        assert node.data == "data"
        assert node.next is None

    def test_node_linking(self):
        """节点链接"""
        node1 = StackNode("first")
        node2 = StackNode("second")
        node1.next = node2

        assert node1.next.data == "second"


class TestStackToList:
    """测试转换为列表"""

    def test_to_list_returns_correct_order(self, populated_stack):
        """to_list 返回从栈顶到栈底的顺序"""
        result = populated_stack.to_list()
        assert result == [3, 2, 1]

    def test_to_list_empty_stack(self, empty_stack):
        """空栈 to_list 返回空列表"""
        assert empty_stack.to_list() == []


class TestStackIntegration:
    """集成场景测试"""

    def test_sequence_operations(self, empty_stack):
        """连续操作序列"""
        # 压入 5 个元素: [0, 1, 2, 3, 4] (4在栈顶)
        for i in range(5):
            empty_stack.push(i)

        # 弹出 3 个: 移除 4, 3, 2，剩下 [0, 1]
        for _ in range(3):
            empty_stack.pop()

        # 再压入 2 个: 先压100，再压200
        empty_stack.push(100)
        empty_stack.push(200)

        # 最终应该是 [200, 100, 1, 0] (从栈顶到栈底)
        assert empty_stack.to_list() == [200, 100, 1, 0]

    def test_stack_with_complex_objects(self, empty_stack):
        """栈存储复杂对象"""
        obj1 = {"id": 1, "name": "item1"}
        obj2 = {"id": 2, "name": "item2"}

        empty_stack.push(obj1)
        empty_stack.push(obj2)

        assert empty_stack.pop() == obj2
        assert empty_stack.pop() == obj1
