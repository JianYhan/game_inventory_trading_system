"""
Pytest 全局配置和共享 Fixtures

TDD 原则：先写测试，再写实现
每个 fixture 提供测试所需的依赖对象
"""

import pytest
import tempfile
import shutil
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.data_structures import Stack, Queue, DoublyLinkedList, HashTable, BinarySearchTree
from src.domain.enums import Rarity, ItemType, OrderStatus, ResultStatus
from src.domain.models import (
    ItemConfig, BackpackItem, Player, MarketOrder,
    BuyRecord, SellRecord, GameSave, Response
)


# ========== 数据结构 Fixtures ==========

@pytest.fixture
def empty_stack():
    """空栈"""
    return Stack()


@pytest.fixture
def populated_stack():
    """包含数据的栈 [3, 2, 1]（3在栈顶）"""
    stack = Stack()
    for i in [1, 2, 3]:
        stack.push(i)
    return stack


@pytest.fixture
def empty_queue():
    """空队列"""
    return Queue()


@pytest.fixture
def populated_queue():
    """包含数据的队列 [a, b, c]（a在队首）"""
    queue = Queue()
    for item in ["a", "b", "c"]:
        queue.enqueue(item)
    return queue


@pytest.fixture
def empty_linked_list():
    """空双向链表"""
    return DoublyLinkedList()


@pytest.fixture
def populated_linked_list():
    """包含数据的双向链表 [10, 20, 30]"""
    dll = DoublyLinkedList()
    for val in [10, 20, 30]:
        dll.append(val)
    return dll


@pytest.fixture
def empty_hash_table():
    """空哈希表"""
    return HashTable(capacity=16)


@pytest.fixture
def populated_hash_table():
    """包含数据的哈希表"""
    ht = HashTable(capacity=8)
    ht.put("name", "TestPlayer")
    ht.put("level", 10)
    ht.put("gold", 1000.0)
    return ht


@pytest.fixture
def empty_bst():
    """空二叉搜索树"""
    return BinarySearchTree()


@pytest.fixture
def populated_bst():
    """包含数据的BST，keys: [50, 30, 70, 20, 40, 60, 80]"""
    bst = BinarySearchTree()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(key, f"data{key}")
    return bst


# ========== Domain Fixtures ==========

@pytest.fixture
def common_item_config():
    """普通物品配置"""
    return ItemConfig(
        item_id=1,
        name="木剑",
        item_type=ItemType.WEAPON,
        rarity=Rarity.COMMON,
        base_price=100.0
    )


@pytest.fixture
def rare_item_config():
    """稀有物品配置"""
    return ItemConfig(
        item_id=2,
        name="铁剑",
        item_type=ItemType.WEAPON,
        rarity=Rarity.RARE,
        base_price=200.0
    )


@pytest.fixture
def sample_backpack_item(common_item_config):
    """背包物品"""
    return BackpackItem(
        item_id=common_item_config.item_id,
        name=common_item_config.name,
        item_type=common_item_config.item_type,
        rarity=common_item_config.rarity,
        quantity=5,
        sell_price=110.0
    )


@pytest.fixture
def new_player():
    """新玩家"""
    return Player(
        player_id="player-001",
        name="TestPlayer",
        gold=1000.0,
        created_at=1234567890.0
    )


@pytest.fixture
def rich_player():
    """富有的玩家"""
    return Player(
        player_id="player-rich",
        name="RichPlayer",
        gold=10000.0,
        created_at=1234567890.0
    )


@pytest.fixture
def sample_market_order(common_item_config, new_player):
    """市场挂单"""
    return MarketOrder(
        order_id="order-001",
        seller_id=new_player.player_id,
        item_id=common_item_config.item_id,
        item_name=common_item_config.name,
        unit_price=110.0,
        total_quantity=3,
        remaining_quantity=3,
        status=OrderStatus.ON_SALE,
        list_time=1234567890.0
    )


@pytest.fixture
def success_response():
    """成功响应"""
    return Response.ok("操作成功", data={"id": 1})


@pytest.fixture
def failure_response():
    """失败响应"""
    return Response.fail("操作失败")


# ========== Service Fixtures ==========

@pytest.fixture
def player_service():
    """玩家服务实例"""
    from src.service.player_service import PlayerService
    return PlayerService()


@pytest.fixture
def inventory_service():
    """背包服务实例"""
    from src.service.inventory_service import InventoryService
    return InventoryService()


@pytest.fixture
def market_service(inventory_service):
    """市场服务实例（依赖背包服务）"""
    from src.service.market_service import MarketService
    return MarketService(inventory_service)


@pytest.fixture
def trade_service():
    """交易记录服务实例"""
    from src.service.trade_service import TradeService
    return TradeService()


@pytest.fixture
def system_service(tmp_path):
    """系统服务实例，使用临时目录"""
    from src.service.system_service import SystemService
    # 临时修改数据目录
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    service = SystemService()
    os.chdir(original_dir)
    return service


# ========== 集成测试 Fixtures ==========

@pytest.fixture
def initialized_game(tmp_path):
    """
    初始化完整游戏环境
    返回所有服务实例，用于集成测试
    """
    # 使用临时目录作为数据目录
    data_dir = tmp_path / "src" / "data"
    data_dir.mkdir(parents=True)

    original_dir = os.getcwd()
    os.chdir(tmp_path)

    # 初始化数据
    from src.repository import initialize
    from src.repository import DATA_DIR as REPO_DATA_DIR
    import src.repository.data_initializer as di
    import src.repository.repositories as repos

    # 修改数据目录指向临时目录
    di.DATA_DIR = str(data_dir)
    repos.DATA_DIR = str(data_dir)

    initialize()

    # 创建服务
    from src.service import (
        PlayerService, InventoryService, MarketService,
        TradeService, SystemService
    )
    player_svc = PlayerService()
    inv_svc = InventoryService()
    market_svc = MarketService(inv_svc)
    trade_svc = TradeService()
    sys_svc = SystemService()

    os.chdir(original_dir)

    return {
        "player": player_svc,
        "inventory": inv_svc,
        "market": market_svc,
        "trade": trade_svc,
        "system": sys_svc,
        "data_dir": str(data_dir)
    }


@pytest.fixture
def two_player_game(initialized_game):
    """
    创建两个玩家的游戏环境
    返回 (买家, 卖家) 和两个玩家对象
    """
    services = initialized_game

    # 创建买家（富有）
    buyer_resp = services["player"].create_player("Buyer")
    buyer = buyer_resp.player
    # 给买家更多金币
    for _ in range(5):
        services["player"].update_gold(buyer.player_id, 1000)

    # 创建卖家
    seller_resp = services["player"].create_player("Seller")
    seller = seller_resp.player

    # 给卖家添加物品
    from src.domain.models import ItemConfig, BackpackItem
    from src.domain.enums import ItemType, Rarity

    item_config = ItemConfig(
        item_id=1, name="测试物品", item_type=ItemType.WEAPON,
        rarity=Rarity.COMMON, base_price=100.0
    )
    backpack_item = BackpackItem(
        item_id=1, name="测试物品", item_type=ItemType.WEAPON,
        rarity=Rarity.COMMON, quantity=10, sell_price=100.0
    )
    services["inventory"].add_item(seller.player_id, backpack_item)

    return {
        **services,
        "buyer": buyer,
        "seller": seller
    }
