# 数据结构模块

## 核心约束

**禁止使用 Python 内置 `list/dict/set`，所有数据结构必须为纯指针实现。**

---

## 数据结构一览

| 类名 | 实现方式 | 内部存储 | 关键操作 |
|------|----------|----------|----------|
| `Stack` | 单向链表 | `StackNode.next` | `push()`, `pop()`, `peek()` |
| `Queue` | 单向链表 + 尾指针 | `QueueNode.next` | `enqueue()`, `dequeue()`, `peek()` |
| `DoublyLinkedList` | 双向链表 + 头尾指针 | `Node.prev`, `Node.next` | `append()`, `prepend()`, `remove()` |
| `HashTable` | 拉链法 | `_buckets[]` + 链表 | `put()`, `get()`, `remove()`, `keys()` |
| `BinarySearchTree` | 递归指针 | `TreeNode.left`, `TreeNode.right` | `insert()`, `search()`, `inorder()`, `range_query()` |

---

## Stack 单向链表栈

### 节点定义
```python
class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None  # 指向下一个节点
```

### 核心方法
```python
class Stack:
    def push(self, item):      # O(1) 头插法
    def pop(self) -> item:      # O(1) 头删法
    def peek(self) -> item:     # O(1) 查看栈顶
    def is_empty(self) -> bool:
    def to_list(self) -> list:  # 导出列表
```

### 使用位置
- `InventoryService._recent_actions` - 记录最近操作历史

---

## Queue 单向链表队列

### 节点定义
```python
class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None
```

### 核心方法
```python
class Queue:
    def enqueue(self, item):     # O(1) 尾插法
    def dequeue(self) -> item:   # O(1) 头删法
    def peek(self) -> item:       # O(1) 查看队首
    def is_empty(self) -> bool:
    def to_list(self) -> list:
```

### 使用位置
- `MarketService._restock_queue` - 系统上新排队
- `TradeService._record_queue` - 交易记录排队

---

## DoublyLinkedList 双向链表

### 节点定义
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None  # 前驱
        self.next = None  # 后继
```

### 核心方法
```python
class DoublyLinkedList:
    def append(self, data):           # O(1) 尾插
    def prepend(self, data):          # O(1) 头插
    def remove(self, data) -> bool:   # O(n) 按值删除
    def to_list(self) -> list:        # 正向遍历
    def to_reversed_list(self) -> list:  # 反向遍历
```

### 使用位置
- `InventoryService._backpack_list` - 背包物品列表
- `MarketService._market_orders` - 市场挂单列表
- `TradeService._buy_records` - 购买记录列表
- `TradeService._sell_records` - 出售记录列表

---

## HashTable 哈希表（拉链法）

### 核心方法
```python
class HashTable:
    def __init__(self, capacity=64):  # 初始桶数
    def put(self, key, value):        # O(1) 平均
    def get(self, key, default=None):  # O(1) 平均
    def remove(self, key):              # O(1) 平均
    def keys(self) -> list:            # 获取所有键
    def values(self) -> list:          # 获取所有值
```

### 使用位置
- `PlayerService._player_table` - 玩家ID索引
- `PlayerService._name_table` - 玩家名称索引
- `InventoryService._backpack_index` - 背包物品索引
- `MarketService._order_index` - 市场订单索引

---

## BinarySearchTree 二叉搜索树

### 节点定义
```python
class TreeNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
```

### 核心方法
```python
class BinarySearchTree:
    def insert(self, key, data=None):          # 插入
    def search(self, key):                      # 搜索
    def inorder(self) -> list:                  # 中序遍历（有序）
    def inorder_items(self) -> list:            # 中序遍历带数据
    def range_query(self, low, high) -> list:   # 范围查询
```

### 使用位置
- `MarketService._price_bst` - 市场价格范围查询（当前未使用但已预留）

---

## 测试

```bash
# 运行所有数据结构测试
pytest tests/unit/data_structures/ -v

# 运行单个测试
pytest tests/unit/data_structures/test_stack.py -v
```

### 测试文件
- `tests/unit/data_structures/test_stack.py` - 16 tests
- `tests/unit/data_structures/test_queue.py` - 19 tests
- `tests/unit/data_structures/test_linked_list.py` - 21 tests
- `tests/unit/data_structures/test_hash_table.py` - 19 tests
- `tests/unit/data_structures/test_bst.py` - 23 tests

---

## 全局规范

- **禁止使用 `[]`、`{}`、`list()`、`dict()`、`set()`**
- 统一命名：`Stack`、`Queue`、`DoublyLinkedList`、`Node`、`HashTable`、`StackNode`、`QueueNode`、`BinarySearchTree`、`TreeNode`
- 所有 ID 为 int，价格/金币为 float，数量为 int，时间戳为 float
- 增删改操作必须同步主结构和索引
