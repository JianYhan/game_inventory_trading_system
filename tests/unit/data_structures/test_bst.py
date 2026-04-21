"""
BinarySearchTree 单元测试

TDD 原则：
1. 测试空树的行为
2. 测试插入/搜索的中序有序性
3. 测试范围查询
"""

import pytest
from src.data_structures.bst import BinarySearchTree, TreeNode


class TestBSTCreation:
    """测试树创建"""

    def test_empty_tree(self, empty_bst):
        """空树创建"""
        assert empty_bst.search(5) is None

    def test_node_creation(self):
        """节点创建"""
        node = TreeNode(10, "data")
        assert node.key == 10
        assert node.data == "data"
        assert node.left is None
        assert node.right is None


class TestBSTInsert:
    """测试插入操作"""

    def test_insert_single(self, empty_bst):
        """插入单个节点"""
        empty_bst.insert(50, "value50")
        assert empty_bst.search(50) == "value50"

    def test_insert_multiple(self, populated_bst):
        """插入多个节点"""
        assert populated_bst.search(30) == "data30"
        assert populated_bst.search(70) == "data70"
        assert populated_bst.search(20) == "data20"

    def test_insert_update(self, populated_bst):
        """更新已有节点"""
        populated_bst.insert(50, "updated50")
        assert populated_bst.search(50) == "updated50"


class TestBSTSearch:
    """测试搜索操作"""

    def test_search_existing(self, populated_bst):
        """搜索存在的键"""
        assert populated_bst.search(40) == "data40"
        assert populated_bst.search(60) == "data60"

    def test_search_non_existing(self, populated_bst):
        """搜索不存在的键"""
        assert populated_bst.search(100) is None
        assert populated_bst.search(0) is None

    def test_search_root(self, populated_bst):
        """搜索根节点"""
        assert populated_bst.search(50) == "data50"


class TestBSTInorder:
    """测试中序遍历"""

    def test_inorder_sorted(self, populated_bst):
        """中序遍历结果应该有序"""
        result = populated_bst.inorder()
        assert result == [20, 30, 40, 50, 60, 70, 80]

    def test_inorder_empty(self, empty_bst):
        """空树中序遍历"""
        assert empty_bst.inorder() == []

    def test_inorder_single(self, empty_bst):
        """单节点中序遍历"""
        empty_bst.insert(50, "only")
        assert empty_bst.inorder() == [50]

    def test_inorder_items(self, populated_bst):
        """中序遍历带数据"""
        result = populated_bst.inorder_items()
        assert result[0] == (20, "data20")
        assert result[-1] == (80, "data80")


class TestBSTRangeQuery:
    """测试范围查询"""

    def test_range_query_partial(self, populated_bst):
        """部分范围查询"""
        result = populated_bst.range_query(30, 70)
        assert result == ["data30", "data40", "data50", "data60", "data70"]

    def test_range_query_narrow(self, populated_bst):
        """窄范围查询"""
        result = populated_bst.range_query(35, 45)
        assert result == ["data40"]

    def test_range_query_no_match(self, populated_bst):
        """无匹配的范围查询"""
        result = populated_bst.range_query(100, 200)
        assert result == []

    def test_range_query_edges(self, populated_bst):
        """边界值查询"""
        result = populated_bst.range_query(20, 80)
        assert result == ["data20", "data30", "data40", "data50", "data60", "data70", "data80"]

    def test_range_query_single_point(self, populated_bst):
        """单点查询"""
        result = populated_bst.range_query(50, 50)
        assert result == ["data50"]

    def test_range_query_empty_tree(self, empty_bst):
        """空树范围查询"""
        assert empty_bst.range_query(0, 100) == []


class TestBSTStructure:
    """测试树的结构正确性"""

    def test_left_less_than_root(self, populated_bst):
        """左子树小于根"""
        # 中序遍历验证BST性质
        inorder = populated_bst.inorder()
        for i in range(1, len(inorder)):
            assert inorder[i] > inorder[i - 1]

    def test_right_greater_than_root(self, populated_bst):
        """右子树大于根"""
        # 根节点是 50
        right_side = populated_bst.range_query(51, 100)
        assert all(key > 50 for key in [60, 70, 80])


class TestBSTIntegration:
    """集成场景测试"""

    def test_sequence_insertions(self):
        """连续插入序列"""
        bst = BinarySearchTree()

        # 按顺序插入（最坏情况，应该还是平衡的吗？）
        for i in range(100):
            bst.insert(i, f"value{i}")

        # 验证全部可搜索
        for i in range(100):
            assert bst.search(i) == f"value{i}"

        # 验证有序
        inorder = bst.inorder()
        assert inorder == list(range(100))

    def test_random_insertions(self):
        """随机插入"""
        bst = BinarySearchTree()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

        for v in values:
            bst.insert(v, f"data{v}")

        # 验证范围查询 [20, 50] 包含 20, 25, 30, 35, 40, 45, 50
        result = bst.range_query(20, 50)
        assert len(result) == 7  # 20, 25, 30, 35, 40, 45, 50

    def test_with_float_keys(self):
        """浮点数键"""
        bst = BinarySearchTree()
        bst.insert(10.5, "a")
        bst.insert(5.2, "b")
        bst.insert(15.8, "c")

        assert bst.search(10.5) == "a"
        assert bst.range_query(5.0, 11.0) == ["b", "a"]

    def test_complex_data(self):
        """复杂数据存储"""
        bst = BinarySearchTree()

        items = [
            (100, {"name": "item1", "price": 100}),
            (200, {"name": "item2", "price": 200}),
            (150, {"name": "item3", "price": 150}),
        ]

        for price, data in items:
            bst.insert(price, data)

        result = bst.range_query(120, 180)
        assert len(result) == 1
        assert result[0]["name"] == "item3"
