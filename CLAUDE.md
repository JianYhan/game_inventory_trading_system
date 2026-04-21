# Game Inventory System

命令行游戏背包交易系统，使用纯 Python 实现，包含自定义数据结构。

## 项目约束

- **禁止使用 Python 内置 `list/dict/set`**，所有数据结构必须为纯指针实现
- **分层架构**：presentation -> service -> repository -> domain -> data_structures
- **统一返回**：所有 Service 方法返回 `Response` 对象
- **统一异常**：使用 `@handle_exceptions` 装饰器

---

## 目录结构

```
game_inventory/
├── main.py                    # 程序入口
├── pyproject.toml            # 项目配置
├── README.md                 # 项目文档
├── CLAUDE.md                 # 本文件
│
├── src/                      # 源代码
│   ├── __init__.py
│   ├── data_structures/       # 纯指针数据结构
│   │   ├── stack.py         # 单向链表栈
│   │   ├── queue.py         # 单向链表队列
│   │   ├── linked_list.py   # 双向链表
│   │   ├── hash_table.py    # 哈希表
│   │   └── bst.py           # 二叉搜索树
│   │
│   ├── domain/               # 领域层
│   │   ├── constants.py     # 配置常量
│   │   ├── messages.py      # 统一消息
│   │   ├── exceptions.py    # 异常处理
│   │   ├── enums.py         # 枚举
│   │   └── models.py         # 数据模型
│   │
│   ├── repository/           # 持久化层
│   │   ├── data_initializer.py
│   │   └── repositories.py
│   │
│   ├── service/             # 业务逻辑层
│   │   ├── player_service.py
│   │   ├── inventory_service.py
│   │   ├── market_service.py
│   │   ├── trade_service.py
│   │   └── system_service.py
│   │
│   ├── presentation/        # 交互界面层
│   │   ├── utils.py
│   │   ├── main_menu.py
│   │   ├── inventory_menu.py
│   │   ├── market_menu.py
│   │   └── profile_menu.py
│   │
│   └── data/                # JSON 数据文件
│       ├── players.json
│       ├── items.json
│       ├── listings.json
│       ├── buy_records.json
│       ├── sell_records.json
│       ├── item_config.json
│       └── save.json
│
├── tests/                    # 测试目录
│   ├── conftest.py          # 全局 fixtures
│   ├── unit/                # 单元测试
│   ├── integration/         # 集成测试
│   └── CLAUDE.md           # 测试文档
│
├── docs/                     # 详细需求文档
└── 项目结构图.md
```

---

## 快速开始

```bash
# 运行游戏
python main.py

# 运行测试
pytest

# 运行数据结构测试（核心）
pytest tests/unit/data_structures/ -v
```

---

## 核心数据结构

| 类名 | 实现 | 关键操作 |
|------|------|----------|
| `Stack` | 单向链表 | push, pop, peek |
| `Queue` | 单向链表+尾指针 | enqueue, dequeue |
| `DoublyLinkedList` | 双向链表 | append, prepend, remove |
| `HashTable` | 拉链法 | put, get, remove |
| `BinarySearchTree` | 递归指针 | insert, search, range_query |

---

## 各层职责

| 层 | 职责 | 关键文件 |
|---|------|----------|
| presentation | 用户交互、输入验证 | main_menu.py, *_menu.py |
| service | 业务逻辑、异常处理 | player_service.py, market_service.py |
| repository | 数据持久化、JSON读写 | repositories.py |
| domain | 数据模型、配置常量、异常 | models.py, constants.py, messages.py |
| data_structures | 纯指针数据结构 | stack.py, queue.py, linked_list.py |

---

## 统一模式

### Service 方法返回
```python
@handle_exceptions
def method(self, ...) -> Response:
    if error:
        raise ValidationException(message)
    return Response.ok(message, data=data)
```

### 使用常量
```python
from src.domain import PlayerConfig, PriceConfig

PlayerConfig.INITIAL_GOLD  # 1000.0
PriceConfig.MIN_PRICE_FACTOR  # 0.8
```

### 使用统一消息
```python
from src.domain import ErrorMessages, SuccessMessages

ErrorMessages.ITEM_NOT_FOUND
SuccessMessages.ITEM_SOLD
```

---

## 测试覆盖

| 目录 | 测试数 | 覆盖范围 |
|------|--------|----------|
| `tests/unit/data_structures/` | 98 | 纯指针数据结构 |
| `tests/unit/domain/` | 30 | 数据模型、枚举 |
| `tests/unit/repository/` | 5 | 持久化层 |
| `tests/unit/service/` | 27 | 业务逻辑 |
| **总计** | **150+** | |

---

## 模块文档

详细文档见各层 CLAUDE.md：

- `src/data_structures/CLAUDE.md` - 数据结构详情
- `src/domain/CLAUDE.md` - 领域层详情
- `src/repository/CLAUDE.md` - 持久化层详情
- `src/service/CLAUDE.md` - 服务层详情
- `src/presentation/CLAUDE.md` - 界面层详情
- `tests/CLAUDE.md` - 测试详情
