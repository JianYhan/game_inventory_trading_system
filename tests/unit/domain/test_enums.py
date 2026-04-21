"""
Domain Enums 单元测试

测试枚举类型的值和属性
"""

import pytest
from src.domain.enums import Rarity, ItemType, OrderStatus, ResultStatus


class TestRarity:
    """测试稀有度枚举"""

    def test_rarity_values(self):
        """测试稀有度值"""
        assert Rarity.COMMON.value == ("Common", 1.0)
        assert Rarity.RARE.value == ("Rare", 2.0)
        assert Rarity.EPIC.value == ("Epic", 4.0)
        assert Rarity.LEGENDARY.value == ("Legendary", 8.0)

    def test_rarity_label(self):
        """测试显示名称"""
        assert Rarity.COMMON.label == "Common"
        assert Rarity.LEGENDARY.label == "Legendary"

    def test_rarity_multiplier(self):
        """测试价格系数"""
        assert Rarity.COMMON.multiplier == 1.0
        assert Rarity.RARE.multiplier == 2.0
        assert Rarity.EPIC.multiplier == 4.0
        assert Rarity.LEGENDARY.multiplier == 8.0


class TestItemType:
    """测试物品类型枚举"""

    def test_item_type_values(self):
        """测试物品类型值"""
        assert ItemType.WEAPON.value == "Weapon"
        assert ItemType.POTION.value == "Potion"
        assert ItemType.ARMOR.value == "Armor"
        assert ItemType.MATERIAL.value == "Material"


class TestOrderStatus:
    """测试订单状态枚举"""

    def test_order_status_values(self):
        """测试订单状态值"""
        assert OrderStatus.ON_SALE.value == "On Sale"
        assert OrderStatus.PARTIAL.value == "Partial"
        assert OrderStatus.SOLD_OUT.value == "Sold Out"
        assert OrderStatus.DELISTED.value == "Delisted"


class TestResultStatus:
    """测试结果状态枚举"""

    def test_result_status_values(self):
        """测试结果状态"""
        assert ResultStatus.SUCCESS.value == "Success"
        assert ResultStatus.FAILURE.value == "Failure"
