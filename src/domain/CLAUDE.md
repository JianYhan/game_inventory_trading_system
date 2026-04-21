# 领域层模块

## 模块组成

```
domain/
├── __init__.py        # 统一导出
├── enums.py           # 枚举定义
├── models.py          # 数据模型
├── constants.py       # 游戏配置常量
├── messages.py        # 统一消息
└── exceptions.py      # 异常处理
```

---

## 枚举 (enums.py)

### Rarity 稀有度
```python
class Rarity(Enum):
    COMMON = ("Common", 1.0)      # 普通 ×1.0
    RARE = ("Rare", 2.0)          # 稀有 ×2.0
    EPIC = ("Epic", 4.0)          # 史诗 ×4.0
    LEGENDARY = ("Legendary", 8.0) # 传说 ×8.0
```

### ItemType 物品类型
```python
class ItemType(Enum):
    WEAPON = "Weapon"    # 武器
    POTION = "Potion"    # 药水
    ARMOR = "Armor"      # 防具
    MATERIAL = "Material" # 材料
```

### OrderStatus 挂单状态
```python
class OrderStatus(Enum):
    ON_SALE = "On Sale"      # 在售
    PARTIAL = "Partial"      # 部分售出
    SOLD_OUT = "Sold Out"   # 已售罄
    DELISTED = "Delisted"   # 已下架
```

### ResultStatus 操作结果
```python
class ResultStatus(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
```

---

## 模型 (models.py)

### ItemConfig 物品配置
```python
@dataclass
class ItemConfig:
    item_id: int
    name: str
    item_type: ItemType
    rarity: Rarity
    base_price: float
    # 属性: rarity_multiplier, sell_price
```

### BackpackItem 背包物品
```python
@dataclass
class BackpackItem:
    item_id: int
    name: str
    item_type: ItemType
    rarity: Rarity
    quantity: int
    sell_price: float
```

### Player 玩家
```python
@dataclass
class Player:
    player_id: str
    name: str
    gold: float
    created_at: float = field(default_factory=time.time)
    # 方法: add_gold(), deduct_gold()
```

### MarketOrder 市场挂单
```python
@dataclass
class MarketOrder:
    order_id: str
    seller_id: str
    item_id: int
    item_name: str
    unit_price: float
    total_quantity: int
    remaining_quantity: int
    status: OrderStatus
    list_time: float
```

### Response 统一返回
```python
@dataclass
class Response:
    status: ResultStatus
    message: str
    data: Any = None
    player: Optional[Player] = None

    @property
    def is_success(self) -> bool:
        return self.status == ResultStatus.SUCCESS

    @classmethod
    def ok(cls, message, data=None, player=None):
        return cls(ResultStatus.SUCCESS, message, data, player)

    @classmethod
    def fail(cls, message):
        return cls(ResultStatus.FAILURE, message)
```

---

## 常量 (constants.py)

### PlayerConfig 玩家配置
```python
class PlayerConfig:
    INITIAL_GOLD = 1000.0      # 初始金币
    MIN_NAME_LENGTH = 2         # 最小名字长度
    MAX_NAME_LENGTH = 12        # 最大名字长度
```

### PriceConfig 价格配置
```python
class PriceConfig:
    MIN_PRICE_FACTOR = 0.8     # 最低售价系数
    MAX_PRICE_FACTOR = 1.2     # 最高售价系数

    @classmethod
    def calculate_range(cls, base_price):      # -> (min, max)
    @classmethod
    def is_valid_price(cls, price, base_price): # -> bool
```

### MarketConfig 市场配置
```python
class MarketConfig:
    SYSTEM_SELLER_ID = "SYSTEM"     # 系统卖家ID
    RESTOCK_MIN_QTY = 1            # 上新最小数量
    RESTOCK_MAX_QTY = 5            # 上新最大数量
```

### RarityWeights 稀有度权重
```python
class RarityWeights:
    COMMON = 6      # 普通权重
    RARE = 3        # 稀有权重
    EPIC = 1        # 史诗权重
    LEGENDARY = 1   # 传说权重
```

---

## 消息 (messages.py)

### ErrorMessages 错误消息
```python
class ErrorMessages:
    EMPTY_NAME = "Name cannot be empty."
    INVALID_NAME_LENGTH = "Name must be {min}-{max} characters long."
    ITEM_NOT_FOUND = "Item not found in backpack."
    INSUFFICIENT_GOLD = "Insufficient gold. Need {need:.0f}, have {have:.0f}."
    ORDER_NOT_FOUND = "Order not found."
    # ... 更多见 messages.py
```

### SuccessMessages 成功消息
```python
class SuccessMessages:
    PLAYER_CREATED = "Player created successfully. Welcome to the game!"
    ITEM_SOLD = "Sold {quantity}x {item} for {gold:.0f} gold."
    ITEM_LISTED = "Listed {quantity}x {item} at {price:.0f} gold each."
    # ... 更多见 messages.py
```

---

## 异常 (exceptions.py)

### 异常类
```python
class GameException(Exception):         # 业务异常基类
class ValidationException(GameException):  # 验证异常
class InsufficientGoldException(GameException):  # 金币不足
class ItemNotFoundException(GameException):  # 物品不存在
class PlayerNotFoundException(GameException):  # 玩家不存在
```

### 装饰器
```python
@handle_exceptions  # 统一异常处理，自动捕获并返回 Response.fail()
```

使用示例：
```python
@handle_exceptions
def create_player(self, name: str) -> Response:
    if not name:
        raise ValidationException(ErrorMessages.EMPTY_NAME)
    # ... 业务逻辑
```

### 验证工具
```python
validate_non_empty(value, field_name)  # 验证非空
validate_range(value, min, max, name)  # 验证范围
```

---

## 导出 (\_\_init\_\_.py)

```python
from .domain import (
    # 枚举
    Rarity, ItemType, OrderStatus, ResultStatus,
    # 模型
    ItemConfig, BackpackItem, Player, MarketOrder,
    BuyRecord, SellRecord, GameSave, Response,
    # 常量
    PlayerConfig, PriceConfig, MarketConfig,
    RarityWeights, ValidationConfig, MenuConfig,
    # 消息
    ErrorMessages, SuccessMessages, InfoMessages,
    # 异常
    handle_exceptions, GameException, ValidationException,
    InsufficientGoldException, ItemNotFoundException, PlayerNotFoundException,
)
```

---

## 测试

```bash
# 运行领域层测试
pytest tests/unit/domain/ -v
```

### 测试文件
- `tests/unit/domain/test_enums.py` - 6 tests
- `tests/unit/domain/test_models.py` - 24 tests
