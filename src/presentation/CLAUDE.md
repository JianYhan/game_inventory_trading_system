# Presentation 层 - 交互界面

## 模块组成

```
presentation/
├── __init__.py          # 统一导出
├── utils.py            # 界面工具函数
├── main_menu.py        # 入口菜单、主菜单
├── inventory_menu.py    # 背包菜单
├── market_menu.py      # 市场菜单
└── profile_menu.py     # 个人中心菜单
```

---

## Utils 工具函数

### 屏幕操作
```python
def clear_screen()  # 跨平台清屏
```

### 信息显示
```python
def print_header(player)  # 打印顶部玩家信息栏
```

### 输入验证
```python
def prompt_choice(prompt, valid_choices) -> int | None
def prompt_int(prompt) -> int | None
def prompt_float(prompt) -> float | None
def confirm(prompt) -> bool  # Yes/No 确认
```

---

## 菜单流程

```
show_entry_menu()
    ├── 继续游戏 → 加载存档 → show_main_menu()
    ├── 新游戏 → 创建角色 → show_main_menu()
    └── 退出

show_main_menu()
    ├── [1] 背包 → show_inventory_menu()
    ├── [2] 市场 → show_market_menu()
    ├── [3] 个人中心 → show_profile_menu()
    └── [0] 保存退出

show_inventory_menu()
    └── 按类型分组展示物品，可出售

show_market_menu()
    ├── 查看市场挂单，可购买
    ├── 上架物品
    └── 搜索挂单

show_profile_menu()
    ├── 我的挂单
    ├── 购买记录
    └── 出售记录
```

---

## 全局交互规则

1. 所有界面支持 0 返回上一级
2. 输入容错：非数字/空输入拦截提示
3. 关键操作 Yes/No 确认
4. 交易后自动刷新顶部信息
5. 提示统一：成功/失败/确认前缀
6. 全部交互使用英文

---

## 入口菜单 (main_menu.py)

```python
def show_entry_menu(player_service, system_service)
    # 无存档: [1]新游戏 [2]退出
    # 有存档: [1]继续 [2]新游戏 [3]退出

def show_main_menu(player, inventory, market, trade, system)
    # [1]背包 [2]市场 [3]我的 [0]保存退出
```

---

## 背包菜单 (inventory_menu.py)

```python
def show_inventory_menu(player, inventory_service, market_service)
    # 按类型分组展示
    # 支持出售给系统
    # 支持上架到市场
```

---

## 市场菜单 (market_menu.py)

```python
def show_market_menu(player, inventory_service, market_service)
    # [1]查看市场 - 展示挂单，支持购买
    # [2]上架物品 - 从背包选择
    # [3]搜索 - 模糊匹配
```

---

## 个人中心菜单 (profile_menu.py)

```python
def show_profile_menu(player, trade_service, market_service)
    # [1]我的挂单 - 支持下架
    # [2]购买记录 - 按时间倒序
    # [3]出售记录 - 按时间倒序
```

---

## 测试

```bash
# 目前交互层主要通过集成测试验证
pytest tests/integration/ -v
```
