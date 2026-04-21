# 测试模块

## 目录结构

```
tests/
├── __init__.py
├── conftest.py              # 全局 fixtures
├── unit/                   # 单元测试
│   ├── __init__.py
│   ├── data_structures/     # 数据结构测试
│   │   ├── test_stack.py
│   │   ├── test_queue.py
│   │   ├── test_linked_list.py
│   │   ├── test_hash_table.py
│   │   └── test_bst.py
│   ├── domain/             # 领域层测试
│   │   ├── test_enums.py
│   │   └── test_models.py
│   ├── repository/         # 持久化层测试
│   │   └── test_repositories.py
│   └── service/            # 业务逻辑层测试
│       ├── test_player_service.py
│       ├── test_inventory_service.py
│       ├── test_market_service.py
│       └── test_trade_service.py
├── integration/            # 集成测试
│   └── test_trading_flow.py
└── e2e/                     # 端到端测试（预留）
    └── __init__.py
```

---

## 运行测试

### 基本命令
```bash
# 运行所有测试
pytest

# 运行所有测试（详细输出）
pytest -v

# 运行所有测试（并行加速）
pytest -n auto

# 运行特定目录
pytest tests/unit/data_structures/

# 运行特定文件
pytest tests/unit/data_structures/test_stack.py

# 运行特定测试类
pytest tests/unit/data_structures/test_stack.py::TestStackLIFO

# 运行特定测试函数
pytest tests/unit/data_structures/test_stack.py::TestStackLIFO::test_pop_order
```

### 测试覆盖率
```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 终端显示覆盖率
pytest --cov=src --cov-report=term-missing
```

---

## 测试文件清单

### 数据结构测试 (98 tests)

| 文件 | 测试数 | 内容 |
|------|--------|------|
| `test_stack.py` | 16 | 栈的 push/pop/peek/LIFO 特性 |
| `test_queue.py` | 19 | 队列的 enqueue/dequeue/FIFO 特性 |
| `test_linked_list.py` | 21 | 双向链表的 append/prepend/remove |
| `test_hash_table.py` | 19 | 哈希表的 put/get/remove/冲突处理 |
| `test_bst.py` | 23 | BST 的 insert/search/range_query |

### 领域层测试 (30 tests)

| 文件 | 测试数 | 内容 |
|------|--------|------|
| `test_enums.py` | 6 | 枚举值和属性 |
| `test_models.py` | 24 | 数据模型创建和方法 |

### 仓库层测试 (5 tests)

| 文件 | 测试数 | 内容 |
|------|--------|------|
| `test_repositories.py` | 5 | 配置加载、数据初始化 |

### 服务层测试 (27 tests)

| 文件 | 测试数 | 内容 |
|------|--------|------|
| `test_player_service.py` | 5 | 服务创建、缓存验证 |
| `test_inventory_service.py` | 9 | 物品查找、数量验证 |
| `test_market_service.py` | 8 | 市场服务基础方法 |
| `test_trade_service.py` | 5 | 交易记录服务 |

### 集成测试 (预留)

| 文件 | 内容 |
|------|------|
| `test_trading_flow.py` | 完整交易流程测试 |

---

## Fixtures (conftest.py)

### 数据结构 Fixtures
```python
@pytest.fixture
def empty_stack()           # 空栈

@pytest.fixture
def populated_stack()       # 栈 [3, 2, 1]

@pytest.fixture
def empty_queue()           # 空队列

@pytest.fixture
def populated_queue()       # 队列 ["a", "b", "c"]

@pytest.fixture
def empty_linked_list()     # 空双向链表

@pytest.fixture
def populated_linked_list()  # 双向链表 [10, 20, 30]

@pytest.fixture
def empty_hash_table()      # 空哈希表

@pytest.fixture
def populated_hash_table()  # 哈希表 {"name": "TestPlayer", ...}

@pytest.fixture
def empty_bst()             # 空二叉搜索树

@pytest.fixture
def populated_bst()         # BST [20, 30, 40, 50, 60, 70, 80]
```

### Domain Fixtures
```python
@pytest.fixture
def common_item_config()    # 普通物品配置 (id=1, 木剑)

@pytest.fixture
def rare_item_config()      # 稀有物品配置 (id=2, 铁剑)

@pytest.fixture
def sample_backpack_item()  # 背包物品

@pytest.fixture
def new_player()            # 新玩家 (金币 1000)

@pytest.fixture
def rich_player()           # 富有玩家 (金币 10000)

@pytest.fixture
def sample_market_order()   # 市场挂单

@pytest.fixture
def success_response()      # 成功响应

@pytest.fixture
def failure_response()      # 失败响应
```

### Service Fixtures
```python
@pytest.fixture
def player_service()        # PlayerService 实例

@pytest.fixture
def inventory_service()     # InventoryService 实例

@pytest.fixture
def market_service()         # MarketService 实例

@pytest.fixture
def trade_service()          # TradeService 实例

@pytest.fixture
def system_service()         # SystemService 实例 (临时目录)
```

### 集成测试 Fixtures
```python
@pytest.fixture
def initialized_game()      # 完整游戏环境

@pytest.fixture
def two_player_game()       # 两个玩家的游戏环境
```

---

## TDD 原则

1. **先写测试，再写实现**
   - 每次新功能先写测试
   - 测试驱动设计

2. **测试即文档**
   - 测试名称描述行为
   - docstring 说明意图

3. **分层测试，快速定位**
   - 单元测试：验证单个模块
   - 集成测试：验证模块协作

4. **Fixtures 复用**
   - 公共数据在 conftest.py 定义
   - 减少测试间重复

---

## 测试命名规范

```python
class TestClassName:
    """测试类名"""

    def test_method_name_scenario_expected(self):
        """
        测试方法名：描述性
        _scenario_: 测试场景
        _expected_: 期望结果
        """
        ...
```

### 示例
```python
class TestStackLIFO:
    """测试栈的后进先出特性"""

    def test_pop_order(self):
        """出栈顺序应该是 3, 2, 1"""
        ...
```
