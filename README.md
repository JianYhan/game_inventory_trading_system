# 📦 游戏库存与交易系统（Game Inventory & Trading System）

## 📖 项目简介

本项目是一个基于 **Python 面向对象编程（OOP）** 开发的游戏库存与交易系统。

系统模拟一个简单的游戏环境，用户可以：

- 创建玩家
- 管理背包物品
- 在市场中进行交易
- 查看交易记录

系统支持数据持久化（JSON 文件），保证数据在多次运行之间保持一致。

------

## 🧩 系统功能

### 👤 玩家管理

- 创建玩家
- 查看玩家信息

### 🎒 背包管理

- 添加物品
- 删除物品
- 查看库存

### 🛒 市场交易

- 上架物品
- 浏览市场
- 购买物品

### 📜 交易记录

- 记录交易历史
- 查询历史交易

### 💾 数据存储

- 自动保存数据到文件
- 程序重启后数据仍然存在

------

## 🏗️ 系统结构

本项目采用 **分层架构（Layered Architecture）**，主要由以下部分组成：

### 1️⃣ 表现层（Presentation Layer）

负责用户交互（CLI界面）

- 主菜单
- 玩家菜单
- 背包菜单
- 市场菜单

------

### 2️⃣ 业务层（Service Layer）

负责系统核心逻辑

- PlayerService
- InventoryService
- MarketService
- TradeService

------

### 3️⃣ 领域层（Domain Layer）

定义系统核心对象

- Player（玩家）
- Backpack（背包）
- Item（抽象类）
  - Weapon
  - Armor
  - Potion
  - Material
- MarketListing（市场物品）
- Trade（交易记录）

------

### 4️⃣ 数据结构层（Data Structures）

实现并使用以下结构：

- Doubly Linked List（背包存储）
- Stack（操作管理）
- Queue（交易处理）
- Tree（层级结构）
- Binary Search Tree（搜索）
- Hash Table（快速查找）

------

### 5️⃣ 持久化层（Repository）

负责数据读写：

- PlayerRepository
- ItemRepository
- TradeRepository

------

### 6️⃣ 文件存储（File Storage）

- players.json
- items.json
- listings.json
- trades.json

------

## 🧠 技术特点

本项目体现以下技术点：

- 面向对象设计（封装、继承、多态、抽象类、组合）
- 自定义数据结构实现
- 分层架构设计
- JSON 文件持久化
- 基本设计模式（Factory / Repository）

------

## 👥 团队分工

- 👑 项目负责人：系统架构 + 代码整合 + Git管理
- 👤 数据结构负责人：Linked List / Stack / Queue / Tree
- 👤 Inventory负责人：Backpack + Item系统
- 👤 数据存储负责人：JSON + Repository
- 👤 CLI负责人：菜单与用户交互
- 👤 Testing负责人：单元测试

------

## 🚀 运行方式

```bash
python main.py
```

程序将自动：

1. 初始化数据（首次运行）
2. 加载已有数据
3. 启动系统菜单

------

## 📂 项目结构（示意）

```
project/
├── presentation/
├── services/
├── domain/
├── data_structures/
├── repository/
├── data/
└── main.py
```

------

## 🔮 后续扩展（可选）

- GUI 图形界面
- 更复杂的交易系统
- 在线多人功能
- 更高效搜索算法

------

## 📊 UML类图

完整的UML类图请查看 [uml.md](uml.md)

------

## 📝 说明

本项目用于展示一个完整的软件系统设计，强调：

- 清晰的结构
- 合理的模块划分
- 可扩展性与可维护性

所有数据结构均为自定义实现，展示了对基础数据结构的深入理解。
