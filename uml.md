# 游戏交易系统 UML（团队阅读版）

> 目标：给组员快速理解系统结构。  
> 原则：**一张图只讲一个主题**，复杂模块单独拆开。

---

## 1. 阅读顺序

建议按下面顺序看：

1. **系统总览图**：先看系统分层和主依赖关系  
2. **核心领域模型图**：理解核心业务对象  
3. **背包模块图**：理解库存与背包  
4. **市场模块图**：理解交易与检索  
5. **关键流程时序图**：理解买卖过程

---

## 2. 系统总览图

这张图只回答一个问题：**系统由哪些层组成，谁依赖谁。**

```mermaid
classDiagram
    class CLI

    class PlayerService
    class InventoryService
    class MarketService
    class TradeService
    class SystemService

    class PlayerRepository
    class ItemRepository
    class ListingRepository
    class TradeRepository

    CLI --> PlayerService
    CLI --> InventoryService
    CLI --> MarketService
    CLI --> TradeService
    CLI --> SystemService

    PlayerService --> PlayerRepository

    InventoryService --> PlayerRepository
    InventoryService --> ItemRepository

    MarketService --> PlayerRepository
    MarketService --> ItemRepository
    MarketService --> ListingRepository
    MarketService --> TradeRepository

    TradeService --> TradeRepository

    SystemService --> PlayerRepository
    SystemService --> ListingRepository
    SystemService --> TradeRepository
```

### 说明
- **CLI**：用户入口，负责菜单、输入输出
- **Service**：业务逻辑层
- **Repository**：数据持久化层
- 这张图故意不展开属性和方法，避免信息过载

---

## 3. 核心领域模型图

这张图只回答一个问题：**系统里有哪些核心业务对象，它们之间是什么关系。**

```mermaid
classDiagram
    class Item {
        <<abstract>>
        item_id
        name
        item_type
        rarity
        base_price
    }

    class Weapon {
        attack
        durability
    }

    class Armor {
        defense
        durability
    }

    class Potion {
        heal_amount
    }

    class Material {
        stack_size
    }

    class Player {
        player_id
        name
        gold
        level
    }

    class Backpack {
        capacity
    }

    class MarketListing {
        listing_id
        seller_id
        item_id
        quantity
        price_per_unit
        status
    }

    class Trade {
        trade_id
        listing_id
        buyer_id
        seller_id
        item_id
        quantity
        price_per_unit
        total_price
        traded_at
    }

    Item <|-- Weapon
    Item <|-- Armor
    Item <|-- Potion
    Item <|-- Material

    Player *-- Backpack
    MarketListing --> Item
    Trade --> MarketListing
```

### 说明
- **Item** 是抽象父类，不同物品类型继承它
- **Player 组合 Backpack**：玩家拥有自己的背包
- **MarketListing** 表示上架中的商品
- **Trade** 表示实际成交记录

---

## 4. 背包模块图

这张图只回答一个问题：**库存管理模块依赖什么，以及背包如何存储物品。**

```mermaid
classDiagram
    class InventoryService {
        get_inventory()
        add_item()
        remove_item()
        undo_last()
        sort_inventory_by_price()
        search_item_in_inventory()
    }

    class PlayerRepository
    class ItemRepository
    class Stack

    class Player
    class Backpack {
        capacity
        add_item()
        remove_item()
        has_item()
        get_quantity()
    }

    class DoublyLinkedList
    class Node

    InventoryService --> PlayerRepository
    InventoryService --> ItemRepository
    InventoryService --> Stack
    InventoryService --> Player
    Player *-- Backpack
    Backpack o-- DoublyLinkedList
    DoublyLinkedList o-- Node
```

### 说明
- **InventoryService** 负责库存增删查改
- **Stack** 用于撤销操作（undo），每个玩家独立维护一个栈
- **Backpack** 内部使用 **DoublyLinkedList** 存储条目
- **堆叠机制**：相同物品堆叠在同一槽位，不占用新槽位；只有新物品才需要新槽位
- 数据结构细节被限制在这个局部图里，不放到总览图中

---

## 5. 市场模块图

这张图只回答一个问题：**市场交易模块依赖哪些对象和数据结构。**

```mermaid
classDiagram
    class MarketService {
        list_item()
        cancel_listing()
        buy_item()
        enqueue_buy_order()
        process_order_queue()
        search_by_item()
        search_by_price_range()
    }

    class PlayerRepository
    class ItemRepository
    class ListingRepository
    class TradeRepository

    class MarketListing
    class Trade

    class Queue
    class HashTable

    MarketService --> PlayerRepository
    MarketService --> ItemRepository
    MarketService --> ListingRepository
    MarketService --> TradeRepository

    MarketService --> Queue
    MarketService --> HashTable

    ListingRepository ..> MarketListing
    TradeRepository ..> Trade
```

### 说明
- **ListingRepository**：管理上架单
- **TradeRepository**：管理成交记录
- **Queue**：处理买单队列（异步订单处理）
- **HashTable**：listing_id 快速查找（O(1) 复杂度）
- **价格索引**：使用 dict[price, list[listing_id]] 支持同价多商品和价格区间查询

---

## 6. 系统支撑模块图

这张图只回答一个问题：**系统统计、分类树、初始化功能如何组织。**

```mermaid
classDiagram
    class SystemService {
        get_category_tree()
        print_category_tree()
        get_system_stats()
        initialize_data()
    }

    class DataInitializer {
        initialize()
    }

    class Tree
    class TreeNode

    class PlayerRepository
    class ListingRepository
    class TradeRepository

    SystemService --> PlayerRepository
    SystemService --> ListingRepository
    SystemService --> TradeRepository
    SystemService --> Tree
    SystemService --> DataInitializer

    Tree o-- TreeNode
```

### 说明
- **SystemService**：偏系统管理和统计
- **Tree / TreeNode**：维护物品分类树
- **DataInitializer**：初始化种子数据

---

## 7. 关键流程时序图：购买商品

这张图只回答一个问题：**买家购买一个商品时，系统怎么协作。**

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant MarketService
    participant PlayerRepository
    participant ListingRepository
    participant TradeRepository
    participant Backpack

    User->>CLI: 选择购买商品
    CLI->>MarketService: buy_item(buyer, listing_id)
    MarketService->>ListingRepository: find_by_id(listing_id)
    ListingRepository-->>MarketService: MarketListing
    MarketService->>PlayerRepository: find buyer / seller
    PlayerRepository-->>MarketService: Player objects
    MarketService->>MarketService: 检查金币、验证非自买
    MarketService->>PlayerRepository: buyer.spend_gold() / seller.earn_gold()
    MarketService->>Backpack: buyer.backpack.add_item()
    Backpack-->>MarketService: success
    MarketService->>TradeRepository: add(trade)
    TradeRepository-->>MarketService: saved
    MarketService->>ListingRepository: update listing status
    MarketService-->>CLI: Trade result
    CLI-->>User: 显示购买结果
```

---

## 8. 关键流程时序图：背包加物品

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant InventoryService
    participant PlayerRepository
    participant ItemRepository
    participant Backpack

    User->>CLI: 添加物品
    CLI->>InventoryService: add_item(player, item_id, quantity)
    InventoryService->>ItemRepository: find_by_id(item_id)
    ItemRepository-->>InventoryService: Item
    InventoryService->>PlayerRepository: find_by_id(player_id)
    PlayerRepository-->>InventoryService: Player
    InventoryService->>Backpack: add_item(item_id, quantity)
    Backpack-->>InventoryService: success
    InventoryService-->>CLI: result
    CLI-->>User: 显示结果
```

---

## 9. 画图取舍说明

为保证清晰、易读，这份 UML 做了这些取舍：

- 去掉了大量 `to_dict()`、`from_dict()`、`save()` 之类实现细节
- 去掉了大部分简单 getter / utility 方法
- 把复杂数据结构从总图中拆出去，只在局部图中展示
- 保留了最关键的关系：继承、组合、依赖
- 把“总览”和“局部细化”分开，便于组员快速理解

---

## 10. 建议使用方式

组内分享时建议这样展示：

- 第 1 页：系统总览图
- 第 2 页：核心领域模型图
- 第 3 页：市场模块图
- 第 4 页：关键时序图

这样比把所有类堆在一张图里更容易读，也更方便讨论。

