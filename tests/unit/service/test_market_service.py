"""
MarketService 单元测试

测试市场相关的业务逻辑
"""

import pytest
from src.service.market_service import MarketService
from src.service.inventory_service import InventoryService
from src.domain.models import ItemConfig, BackpackItem
from src.domain.enums import ItemType, Rarity, OrderStatus


class TestMarketServiceBasic:
    """基础测试"""

    def test_market_service_creation(self):
        """创建服务"""
        inv_service = InventoryService()
        service = MarketService(inv_service)
        assert service is not None

    def test_find_item_in_backpack(self):
        """测试在背包中查找物品"""
        inv_service = InventoryService()
        service = MarketService(inv_service)

        # 不存在的玩家应该返回 None
        found = service._find_item_in_backpack("non_existing_player", 1)
        assert found is None

    def test_create_item_from_config(self):
        """测试从配置创建物品"""
        inv_service = InventoryService()
        service = MarketService(inv_service)

        # 使用ITEM_CONFIG中存在的物品ID
        from src.repository import ITEM_CONFIG
        if ITEM_CONFIG:
            first_item_id = next(iter(ITEM_CONFIG.keys()))
            item = service._create_item_from_config(int(first_item_id), 5, "测试物品")
            assert item is not None
            assert item.quantity == 5
            assert item.name == "测试物品"

    def test_create_item_from_config_not_found(self):
        """测试从不存在配置创建物品返回None"""
        inv_service = InventoryService()
        service = MarketService(inv_service)

        item = service._create_item_from_config(99999, 5)
        assert item is None

    def test_validate_quantity(self):
        """测试数量验证"""
        inv_service = InventoryService()
        service = MarketService(inv_service)

        from src.domain import ValidationException

        # 合法数量
        service._validate_quantity(5, 10)

        # 非法数量 - 为零
        with pytest.raises(ValidationException):
            service._validate_quantity(0, 10)

        # 非法数量 - 超过最大
        with pytest.raises(ValidationException):
            service._validate_quantity(15, 10)

    def test_system_seller_id(self):
        """测试系统卖家ID"""
        from src.domain import MarketConfig
        assert MarketConfig.SYSTEM_SELLER_ID == "SYSTEM"
