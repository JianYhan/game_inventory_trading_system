"""
Domain Models 单元测试

测试数据模型的创建和行为
"""

import pytest
from datetime import datetime

from src.domain.enums import Rarity, ItemType, OrderStatus, ResultStatus, OrderStatus as OS
from src.domain.models import (
    ItemConfig, BackpackItem, Player, MarketOrder,
    BuyRecord, SellRecord, GameSave, Response
)


class TestItemConfig:
    """测试物品配置"""

    def test_item_config_creation(self, common_item_config):
        """创建物品配置"""
        assert common_item_config.item_id == 1
        assert common_item_config.name == "木剑"
        assert common_item_config.item_type == ItemType.WEAPON
        assert common_item_config.rarity == Rarity.COMMON
        assert common_item_config.base_price == 100.0

    def test_rarity_multiplier(self, common_item_config, rare_item_config):
        """测试稀有度系数"""
        assert common_item_config.rarity_multiplier == 1.0
        assert rare_item_config.rarity_multiplier == 2.0

    def test_sell_price_calculation(self, common_item_config, rare_item_config):
        """测试出售价格计算"""
        # 普通物品 = 基础价格 × 1.0
        assert common_item_config.sell_price == 100.0
        # 稀有物品 = 基础价格 × 2.0
        assert rare_item_config.sell_price == 400.0


class TestBackpackItem:
    """测试背包物品"""

    def test_backpack_item_creation(self, sample_backpack_item, common_item_config):
        """创建背包物品"""
        assert sample_backpack_item.item_id == common_item_config.item_id
        assert sample_backpack_item.name == common_item_config.name
        assert sample_backpack_item.quantity == 5
        assert sample_backpack_item.sell_price == 110.0

    def test_backpack_item_fields(self):
        """背包物品字段完整性"""
        item = BackpackItem(
            item_id=1, name="测试", item_type=ItemType.WEAPON,
            rarity=Rarity.COMMON, quantity=10, sell_price=100.0
        )
        assert item.item_id == 1
        assert item.item_type == ItemType.WEAPON
        assert item.rarity == Rarity.COMMON


class TestPlayer:
    """测试玩家"""

    def test_player_creation(self, new_player):
        """创建玩家"""
        assert new_player.player_id == "player-001"
        assert new_player.name == "TestPlayer"
        assert new_player.gold == 1000.0

    def test_player_add_gold(self, new_player):
        """增加金币"""
        new_player.add_gold(500)
        assert new_player.gold == 1500.0

    def test_player_deduct_gold_sufficient(self, new_player):
        """扣除金币（足够）"""
        result = new_player.deduct_gold(300)
        assert result is True
        assert new_player.gold == 700.0

    def test_player_deduct_gold_insufficient(self, new_player):
        """扣除金币（不足）"""
        result = new_player.deduct_gold(2000)
        assert result is False
        assert new_player.gold == 1000.0  # 不变

    def test_default_created_at(self):
        """默认创建时间"""
        import time
        before = time.time()
        player = Player(player_id="p1", name="Test", gold=100)
        after = time.time()
        assert before <= player.created_at <= after


class TestMarketOrder:
    """测试市场订单"""

    def test_market_order_creation(self, sample_market_order, new_player, common_item_config):
        """创建市场订单"""
        assert sample_market_order.order_id == "order-001"
        assert sample_market_order.seller_id == new_player.player_id
        assert sample_market_order.item_id == common_item_config.item_id
        assert sample_market_order.item_name == common_item_config.name
        assert sample_market_order.unit_price == 110.0
        assert sample_market_order.total_quantity == 3
        assert sample_market_order.remaining_quantity == 3
        assert sample_market_order.status == OrderStatus.ON_SALE

    def test_market_order_status(self, sample_market_order):
        """订单状态"""
        assert sample_market_order.status == OrderStatus.ON_SALE

        # 更改状态
        sample_market_order.status = OrderStatus.SOLD_OUT
        assert sample_market_order.status == OrderStatus.SOLD_OUT

    def test_default_list_time(self):
        """默认上架时间"""
        import time
        before = time.time()
        order = MarketOrder(
            order_id="o1", seller_id="s1", item_id=1, item_name="Test",
            unit_price=100.0, total_quantity=1, remaining_quantity=1,
            status=OrderStatus.ON_SALE
        )
        after = time.time()
        assert before <= order.list_time <= after


class TestTradeRecords:
    """测试交易记录"""

    def test_buy_record_creation(self):
        """创建购买记录"""
        record = BuyRecord(
            record_id="r1",
            buyer_id="buyer1",
            seller_id="seller1",
            item_id=1,
            item_name="木剑",
            quantity=2,
            unit_price=100.0,
            trade_time=1234567890.0
        )
        assert record.buyer_id == "buyer1"
        assert record.quantity == 2
        assert record.total_price == 200.0

    def test_sell_record_creation(self):
        """创建出售记录"""
        record = SellRecord(
            record_id="r1",
            seller_id="seller1",
            buyer_id="buyer1",
            item_id=1,
            item_name="木剑",
            quantity=2,
            unit_price=100.0,
            trade_time=1234567890.0
        )
        assert record.seller_id == "seller1"
        assert record.total_price == 200.0

    def test_record_total_price(self):
        """记录总价计算"""
        record = BuyRecord(
            record_id="r1", buyer_id="b1", seller_id="s1",
            item_id=1, item_name="剑", quantity=3, unit_price=150.0,
            trade_time=1.0
        )
        assert record.total_price == 450.0

    def test_default_trade_time(self):
        """默认交易时间"""
        import time
        before = time.time()
        record = BuyRecord(
            record_id="r1", buyer_id="b1", seller_id="s1",
            item_id=1, item_name="剑", quantity=1, unit_price=100.0
        )
        after = time.time()
        assert before <= record.trade_time <= after


class TestGameSave:
    """测试游戏存档"""

    def test_game_save_creation(self):
        """创建存档"""
        save = GameSave(
            player_id="p1",
            player_name="TestPlayer",
            gold=1000.0,
            backpack_items=[],
            my_orders=[],
            buy_records=[],
            sell_records=[],
            save_time=1234567890.0
        )
        assert save.player_id == "p1"
        assert save.gold == 1000.0
        assert save.backpack_items == []

    def test_default_save_time(self):
        """默认存档时间"""
        import time
        before = time.time()
        save = GameSave(
            player_id="p1", player_name="Test", gold=100,
            backpack_items=[], my_orders=[],
            buy_records=[], sell_records=[]
        )
        after = time.time()
        assert before <= save.save_time <= after


class TestResponse:
    """测试响应对象"""

    def test_success_response(self, success_response):
        """成功响应"""
        assert success_response.status == ResultStatus.SUCCESS
        assert success_response.message == "操作成功"
        assert success_response.data == {"id": 1}

    def test_failure_response(self, failure_response):
        """失败响应"""
        assert failure_response.status == ResultStatus.FAILURE
        assert failure_response.message == "操作失败"

    def test_ok_factory(self):
        """ok 工厂方法"""
        resp = Response.ok("保存成功", data={"player_id": "p1"})
        assert resp.status == ResultStatus.SUCCESS
        assert resp.message == "保存成功"
        assert resp.data == {"player_id": "p1"}

    def test_fail_factory(self):
        """fail 工厂方法"""
        resp = Response.fail("金币不足")
        assert resp.status == ResultStatus.FAILURE
        assert resp.message == "金币不足"

    def test_response_with_player(self, new_player):
        """响应包含玩家信息"""
        resp = Response.ok("欢迎", player=new_player)
        assert resp.player.name == "TestPlayer"
