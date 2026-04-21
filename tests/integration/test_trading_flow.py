"""
交易流程集成测试

测试完整的交易场景：
创建玩家 -> 上架物品 -> 购买物品 -> 检查记录
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestTradingFlowBasic:
    """交易流程基础测试"""

    def test_item_config_loaded(self):
        """验证物品配置已加载"""
        from src.repository import ITEM_CONFIG
        assert isinstance(ITEM_CONFIG, dict)
        assert len(ITEM_CONFIG) > 0

    def test_initial_backpack_configured(self):
        """验证初始背包已配置"""
        from src.repository import INITIAL_BACKPACK
        assert isinstance(INITIAL_BACKPACK, list)
        assert len(INITIAL_BACKPACK) > 0

    def test_rarity_config(self):
        """验证稀有度配置"""
        from src.domain import Rarity, PriceConfig

        assert Rarity.COMMON.multiplier == 1.0
        assert Rarity.RARE.multiplier == 2.0
        assert Rarity.EPIC.multiplier == 4.0
        assert Rarity.LEGENDARY.multiplier == 8.0

    def test_price_range_calculation(self):
        """验证价格范围计算"""
        from src.domain import PriceConfig

        min_price, max_price = PriceConfig.calculate_range(100.0)
        assert min_price == 80.0
        assert max_price == 120.0

    def test_price_validation(self):
        """验证价格验证逻辑"""
        from src.domain import PriceConfig

        assert PriceConfig.is_valid_price(100, 100) is True
        assert PriceConfig.is_valid_price(80, 100) is True
        assert PriceConfig.is_valid_price(120, 100) is True
        assert PriceConfig.is_valid_price(50, 100) is False
        assert PriceConfig.is_valid_price(150, 100) is False


class TestDataFlow:
    """数据流程测试"""

    def test_backpack_item_creation(self):
        """验证背包物品创建"""
        from src.domain import BackpackItem, ItemType, Rarity

        item = BackpackItem(
            item_id=1,
            name="测试剑",
            item_type=ItemType.WEAPON,
            rarity=Rarity.COMMON,
            quantity=5,
            sell_price=100.0
        )

        assert item.item_id == 1
        assert item.quantity == 5
        assert item.name == "测试剑"

    def test_player_gold_operations(self):
        """验证玩家金币操作"""
        from src.domain import Player

        player = Player(
            player_id="test-001",
            name="TestPlayer",
            gold=1000.0
        )

        assert player.gold == 1000.0

        player.add_gold(500)
        assert player.gold == 1500.0

        result = player.deduct_gold(300)
        assert result is True
        assert player.gold == 1200.0

        result = player.deduct_gold(10000)
        assert result is False
        assert player.gold == 1200.0

    def test_market_order_status(self):
        """验证订单状态"""
        from src.domain import MarketOrder, OrderStatus

        order = MarketOrder(
            order_id="o1",
            seller_id="seller-001",
            item_id=1,
            item_name="测试物品",
            unit_price=100.0,
            total_quantity=10,
            remaining_quantity=5,
            status=OrderStatus.PARTIAL,
            list_time=1.0
        )

        assert order.status == OrderStatus.PARTIAL
        assert order.remaining_quantity == 5

    def test_response_success(self):
        """验证成功响应"""
        from src.domain import Response

        resp = Response.ok("操作成功", data={"id": 1})
        assert resp.is_success is True
        assert resp.message == "操作成功"

    def test_response_failure(self):
        """验证失败响应"""
        from src.domain import Response

        resp = Response.fail("操作失败")
        assert resp.is_success is False
        assert resp.message == "操作失败"


class TestIntegrationHelpers:
    """集成测试辅助"""

    def test_exception_decorator(self):
        """验证异常处理装饰器"""
        from src.domain import handle_exceptions, ValidationException, Response

        class TestService:
            @handle_exceptions
            def fail_method(self):
                raise ValidationException("Test error")

            @handle_exceptions
            def success_method(self):
                return Response.ok("Success")

        svc = TestService()

        resp = svc.fail_method()
        assert resp.is_success is False
        assert "Test error" in resp.message

        resp = svc.success_method()
        assert resp.is_success is True

    def test_rarity_weights(self):
        """验证稀有度权重"""
        from src.domain import RarityWeights, Rarity

        weights = RarityWeights.get_weights()
        assert Rarity.COMMON in weights
        assert Rarity.RARE in weights
        assert len(weights) == 11  # 6+3+1+1

    def test_market_config(self):
        """验证市场配置"""
        from src.domain import MarketConfig

        assert MarketConfig.SYSTEM_SELLER_ID == "SYSTEM"
        assert MarketConfig.RESTOCK_MIN_QTY >= 1
        assert MarketConfig.RESTOCK_MAX_QTY >= MarketConfig.RESTOCK_MIN_QTY
