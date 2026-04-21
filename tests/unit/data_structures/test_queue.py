"""
Queue 单元测试

TDD 原则：
1. 测试空队列的行为
2. 测试入队/出队的 FIFO 特性
3. 测试边界情况
"""

import pytest
from src.data_structures.queue import Queue, QueueNode


class TestQueueBasic:
    """测试队列的基本功能"""

    def test_empty_queue_creation(self, empty_queue):
        """空队列创建后应该为空"""
        assert empty_queue.is_empty()
        assert len(empty_queue) == 0

    def test_enqueue_single_item(self, empty_queue):
        """入队单个元素"""
        empty_queue.enqueue("item")
        assert not empty_queue.is_empty()
        assert len(empty_queue) == 1

    def test_enqueue_multiple_items(self, populated_queue):
        """入队多个元素"""
        assert len(populated_queue) == 3
        assert populated_queue.peek() == "a"


class TestQueueFIFO:
    """测试队列的先进先出特性"""

    def test_dequeue_order(self, populated_queue):
        """出队顺序应该是 a, b, c"""
        assert populated_queue.dequeue() == "a"
        assert populated_queue.dequeue() == "b"
        assert populated_queue.dequeue() == "c"
        assert populated_queue.is_empty()

    def test_enqueue_then_dequeue(self, empty_queue):
        """入队后立即出队"""
        empty_queue.enqueue("first")
        empty_queue.enqueue("second")
        empty_queue.enqueue("third")

        assert empty_queue.dequeue() == "first"
        assert empty_queue.dequeue() == "second"
        assert empty_queue.dequeue() == "third"
        assert empty_queue.is_empty()


class TestQueuePeek:
    """测试 peek 操作"""

    def test_peek_does_not_remove(self, populated_queue):
        """peek 不移除元素"""
        original_len = len(populated_queue)
        front = populated_queue.peek()

        assert front == "a"
        assert len(populated_queue) == original_len

    def test_peek_empty_queue_raises(self, empty_queue):
        """空队列 peek 应该抛出异常"""
        with pytest.raises(IndexError, match="empty"):
            empty_queue.peek()


class TestQueueDequeue:
    """测试 dequeue 操作"""

    def test_dequeue_empty_queue_raises(self, empty_queue):
        """空队列 dequeue 应该抛出异常"""
        with pytest.raises(IndexError, match="empty"):
            empty_queue.dequeue()

    def test_dequeue_updates_head(self, populated_queue):
        """dequeue 后头指针应该更新"""
        populated_queue.dequeue()
        assert populated_queue.peek() == "b"


class TestQueueNode:
    """测试队列节点"""

    def test_node_creation(self):
        """节点创建"""
        node = QueueNode("data")
        assert node.data == "data"
        assert node.next is None

    def test_node_linking(self):
        """节点链接形成链表"""
        node1 = QueueNode("first")
        node2 = QueueNode("second")
        node1.next = node2

        assert node1.next.data == "second"


class TestQueueTailManagement:
    """测试尾指针管理"""

    def test_single_element_queue(self, empty_queue):
        """单元素队列的头尾应该相同"""
        empty_queue.enqueue("only")
        # 出队后队列应该为空
        empty_queue.dequeue()
        assert empty_queue.is_empty()

    def test_dequeue_until_empty(self, populated_queue):
        """全部出队后队列为空"""
        while not populated_queue.is_empty():
            populated_queue.dequeue()
        assert populated_queue.is_empty()
        assert len(populated_queue) == 0


class TestQueueToList:
    """测试转换为列表"""

    def test_to_list_returns_correct_order(self, populated_queue):
        """to_list 返回从队首到队尾的顺序"""
        result = populated_queue.to_list()
        assert result == ["a", "b", "c"]

    def test_to_list_empty_queue(self, empty_queue):
        """空队列 to_list 返回空列表"""
        assert empty_queue.to_list() == []


class TestQueueIntegration:
    """集成场景测试"""

    def test_mixed_operations(self, empty_queue):
        """混合操作序列"""
        # 入队 5 个
        for i in range(5):
            empty_queue.enqueue(i)

        # 出队 2 个
        assert empty_queue.dequeue() == 0
        assert empty_queue.dequeue() == 1

        # 再入队 3 个
        empty_queue.enqueue(100)
        empty_queue.enqueue(200)
        empty_queue.enqueue(300)

        # 最终队列应该是 [2, 3, 4, 100, 200, 300]
        assert empty_queue.to_list() == [2, 3, 4, 100, 200, 300]

    def test_queue_with_complex_objects(self, empty_queue):
        """队列存储复杂对象"""
        obj1 = {"id": 1, "task": "task1"}
        obj2 = {"id": 2, "task": "task2"}

        empty_queue.enqueue(obj1)
        empty_queue.enqueue(obj2)

        assert empty_queue.dequeue() == obj1
        assert empty_queue.dequeue() == obj2
