# Repository 层 - 数据持久化

## 模块组成

```
repository/
├── __init__.py              # 统一导出
├── data_initializer.py       # 数据初始化
└── repositories.py           # 各表仓库
```

---

## 数据初始化 (data_initializer.py)

### 数据目录
```python
DATA_DIR = "src/data"  # 相对路径，基于项目根目录
```

### 初始化文件
- `players.json` - 玩家数据
- `items.json` - 背包物品
- `listings.json` - 市场挂单
- `buy_records.json` - 购买记录
- `sell_records.json` - 出售记录
- `item_config.json` - 物品配置（只读）
- `save.json` - 当前存档

### 物品配置 (item_config.json)
```json
{
  "1001": {
    "item_id": 1001,
    "name": "Wooden Sword",
    "item_type": "WEAPON",
    "rarity": "COMMON",
    "base_price": 100.0
  }
}
```

### 初始背包
```python
INITIAL_BACKPACK = [
    {"item_id": 1001, "quantity": 1},  # 木剑
    {"item_id": 2001, "quantity": 5},  # 小红药水
    {"item_id": 2002, "quantity": 3},  # 中红药水
    {"item_id": 3001, "quantity": 1},  # 皮革护甲
]
```

### 初始化函数
```python
def initialize():
    """初始化所有数据文件，确保目录和文件存在"""
    ...
```

---

## 仓库 (repositories.py)

### PlayerRepository 玩家仓库
```python
class PlayerRepository:
    def save(self, player: Player):           # 保存/更新玩家
    def find_by_id(self, player_id) -> Player | None  # 按ID查找
    def name_exists(self, name) -> bool:      # 检查名字是否存在
    def find_all(self) -> list:               # 查找所有玩家
    def delete(self, player_id):              # 删除玩家
```

### ItemRepository 物品仓库
```python
class ItemRepository:
    def save_item(self, player_id, item):     # 保存物品
    def find_by_player(self, player_id) -> list  # 查找玩家物品
    def remove_item(self, player_id, item_id): # 删除物品
```

### ListingRepository 挂单仓库
```python
class ListingRepository:
    def save(self, order: MarketOrder):            # 保存挂单
    def find_by_id(self, order_id) -> MarketOrder | None  # 按ID查找
    def find_all_active(self) -> list:              # 查找所有在售挂单
    def find_by_seller(self, seller_id) -> list:  # 按卖家查找
    def delete(self, order_id):                    # 删除挂单
```

### TradeRepository 交易记录仓库
```python
class TradeRepository:
    def save_buy(self, record: BuyRecord):         # 保存购买记录
    def save_sell(self, record: SellRecord):      # 保存出售记录
    def find_buy_by_player(self, player_id) -> list:   # 查找玩家购买记录
    def find_sell_by_player(self, player_id) -> list: # 查找玩家出售记录
```

---

## JSON 结构

### players.json
```json
{
  "player_uuid": {
    "player_id": "uuid",
    "name": "PlayerName",
    "gold": 1000.0,
    "created_at": 1234567890.0
  }
}
```

### items.json
```json
{
  "player_uuid": [
    {
      "item_id": 1001,
      "name": "Wooden Sword",
      "item_type": "WEAPON",
      "rarity": "COMMON",
      "quantity": 5,
      "sell_price": 100.0
    }
  ]
}
```

---

## 测试

```bash
# 运行仓库层测试
pytest tests/unit/repository/ -v
```

### 测试文件
- `tests/unit/repository/test_repositories.py` - 5 tests

---

## 全局规范

- JSON 文件路径基于 `DATA_DIR`
- Repository 层不处理业务逻辑，只负责序列化/反序列化
- 配置表（item_config.json）只读，运行时不修改
- 记录表只增不改，保留历史
