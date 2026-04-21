# Game Inventory System 游戏背包系统

一个基于命令行的游戏背包管理系统，使用纯 Python 实现，包含自定义数据结构。

## 功能简介

- 玩家注册与登录
- 背包物品管理（增删查）
- 市场交易系统
- 玩家间交易

## 项目特色

### 纯指针数据结构
不使用 Python 内置 `list/dict/set`，所有数据结构（Stack、Queue、LinkedList、HashTable、BST）均为纯指针实现。

### 分层架构
```
presentation/  →  service/  →  repository/  →  domain/
    界面层         业务层         持久化层        模型层
```

### 统一异常处理
- `@handle_exceptions` 装饰器统一捕获所有 Service 层异常
- 日志记录所有操作和错误

## 项目结构

```
game_inventory/
├── main.py              # 程序入口
├── src/
│   ├── data_structures/ # 纯指针数据结构
│   │   ├── stack.py     # 单向链表栈
│   │   ├── queue.py     # 单向链表队列
│   │   ├── linked_list.py  # 双向链表
│   │   ├── hash_table.py   # 哈希表
│   │   └── bst.py       # 二叉搜索树
│   ├── domain/          # 领域层
│   │   ├── constants.py # 游戏配置常量
│   │   ├── messages.py  # 统一消息
│   │   ├── exceptions.py # 异常处理
│   │   ├── enums.py     # 枚举定义
│   │   └── models.py    # 数据模型
│   ├── repository/      # 数据持久化
│   ├── service/         # 业务逻辑
│   └── presentation/    # 交互界面
├── tests/              # 测试目录
├── docs/               # 详细文档
└── pyproject.toml      # 项目配置
```

## 运行方式

```bash
# 确保已安装 Python 3.x
python main.py
```

## 依赖

本项目无第三方库依赖，仅使用 Python 标准库。

## 测试

使用 pytest 进行 TDD 测试，分层测试架构：

```bash
# 安装测试依赖
pip install pytest pytest-xdist

# 运行所有测试
pytest

# 只运行数据结构测试（核心）
pytest tests/unit/data_structures/

# 运行特定测试文件
pytest tests/unit/data_structures/test_stack.py -v

# 并行运行测试（加速）
pytest -n auto
```

### 测试覆盖

- **单元测试**: `tests/unit/`
  - `data_structures/` - 纯指针实现的数据结构（98 tests ✓）
  - `domain/` - 数据模型与枚举
  - `repository/` - 数据持久化层
  - `service/` - 业务逻辑层

- **集成测试**: `tests/integration/`
  - 完整交易流程测试

### TDD 原则

1. 先写测试，再写实现
2. 测试即文档
3. 使用 fixtures 共享测试数据
4. 分层测试，快速定位问题

## 代码质量改进

### 统一配置管理
所有魔法数字集中在 `constants.py`：

```python
from src.domain import PlayerConfig, PriceConfig, MarketConfig

# 初始金币
PlayerConfig.INITIAL_GOLD  # 1000.0

# 价格范围
PriceConfig.MIN_PRICE_FACTOR  # 0.8
PriceConfig.MAX_PRICE_FACTOR  # 1.2
```

### 统一异常处理
使用 `@handle_exceptions` 装饰器：

```python
from src.domain import handle_exceptions

@handle_exceptions
def create_player(self, name: str) -> Response:
    # 异常自动捕获并返回 Response.fail()
    ...
```

### 统一日志记录
所有 Service 层操作都有日志记录：

```python
logger.info(f"Player {player_id} sold {quantity}x {item_name}")
logger.error(f"Operation failed: {str(e)}", exc_info=True)
```

### 统一消息管理
用户Facing的消息集中在 `messages.py`：

```python
from src.domain import ErrorMessages, SuccessMessages

ErrorMessages.ITEM_NOT_FOUND  # "Item not found in backpack."
SuccessMessages.ITEM_SOLD     # "Sold {quantity}x {item} for {gold:.0f} gold."
```
