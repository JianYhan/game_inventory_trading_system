# Service 层 - 业务逻辑

## 模块组成

```
service/
├── __init__.py            # 统一导出
├── player_service.py      # 玩家服务
├── inventory_service.py   # 背包服务
├── market_service.py      # 市场服务
├── trade_service.py      # 交易记录服务
└── system_service.py      # 系统/存档服务
```

---

## PlayerService 玩家服务

### 职责
- 玩家创建、查询
- 金币管理
- 玩家缓存

### 核心方法
```python
class PlayerService:
    def create_player(self, name: str) -> Response
    def get_player(self, player_id: str) -> Response
    def update_gold(self, player_id: str, delta: float) -> Response
```

### 依赖
- `PlayerRepository` - 玩家持久化
- `ItemRepository` - 物品持久化
- `HashTable` - 玩家缓存、名称索引

---

## InventoryService 背包服务

### 职责
- 背包查看（列表/分组）
- 物品出售给系统
- 物品添加/扣除

### 核心方法
```python
class InventoryService:
    def get_backpack(self, player_id: str) -> Response
    def get_backpack_grouped(self, player_id: str) -> Response
    def sell_item(self, player_id, item_id, quantity, price) -> Response
    def add_item(self, player_id, item: BackpackItem) -> Response
    def deduct_item(self, player_id, item_id, quantity) -> Response
```

### 内部方法
```python
def _find_item(self, items, item_id) -> Optional[BackpackItem]
def _validate_quantity(self, quantity, max_qty) -> None
```

### 依赖
- `ItemRepository` - 物品持久化
- `DoublyLinkedList` - 背包列表
- `HashTable` - 物品索引
- `Stack` - 最近操作记录

---

## MarketService 市场服务

### 职责
- 物品上架/下架
- 市场浏览/搜索
- 购买处理
- 系统定时上新

### 核心方法
```python
class MarketService:
    def list_item(self, player_id, item_id, quantity, unit_price) -> Response
    def get_listings(self) -> Response
    def buy_item(self, buyer_id, order_id, quantity) -> Response
    def delist(self, player_id, order_id) -> Response
    def search_listings(self, keyword: str) -> Response
    def system_restock(self) -> None
```

### 内部方法
```python
def _find_item_in_backpack(self, player_id, item_id) -> Optional[BackpackItem]
def _create_item_from_config(self, item_id, quantity, name=None) -> Optional[BackpackItem]
def _validate_quantity(self, quantity, max_qty, field_name) -> None
```

### 依赖
- `ListingRepository` - 挂单持久化
- `TradeRepository` - 交易记录持久化
- `PlayerRepository` - 玩家数据
- `InventoryService` - 背包操作
- `DoublyLinkedList` - 市场挂单列表
- `HashTable` - 订单索引
- `Queue` - 上新队列

---

## TradeService 交易记录服务

### 职责
- 查询购买/出售记录
- 查询我的挂单

### 核心方法
```python
class TradeService:
    def get_my_buy_records(self, player_id) -> Response
    def get_my_sell_records(self, player_id) -> Response
    def get_my_listings(self, player_id) -> Response
```

### 依赖
- `TradeRepository` - 记录持久化
- `ListingRepository` - 挂单查询
- `DoublyLinkedList` - 记录列表
- `Queue` - 记录队列

---

## SystemService 系统/存档服务

### 职责
- 游戏存档保存/加载
- 检查存档是否存在

### 核心方法
```python
class SystemService:
    def has_save(self) -> bool
    def save_game(self, player_id) -> Response
    def load_save(self) -> Response
```

---

## 统一模式

### 异常处理
```python
@handle_exceptions
def some_method(self, ...) -> Response:
    # 异常自动捕获并返回 Response.fail()
    # 同时记录日志
```

### 日志记录
```python
logger = logging.getLogger(__name__)

def some_method(self):
    logger.info(f"Player {player_id} performed action")
    logger.error(f"Operation failed: {str(e)}", exc_info=True)
```

### 统一验证
```python
from ..domain import PriceConfig, ErrorMessages

if not PriceConfig.is_valid_price(price, base_price):
    raise ValidationException(...)
```

---

## 测试

```bash
# 运行服务层测试
pytest tests/unit/service/ -v
```

### 测试文件
- `tests/unit/service/test_player_service.py` - 5 tests
- `tests/unit/service/test_inventory_service.py` - 9 tests
- `tests/unit/service/test_market_service.py` - 8 tests
- `tests/unit/service/test_trade_service.py` - 5 tests
