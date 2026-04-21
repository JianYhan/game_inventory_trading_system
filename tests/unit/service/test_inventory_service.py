"""
InventoryService 单元测试

测试背包相关的业务逻辑
"""

import pytest
from src.service.inventory_service import InventoryService
from src.domain.models import ItemConfig, BackpackItem
from src.domain.enums import ItemType, Rarity


class TestInventoryServiceBasic:
    """基础测试"""

    def test_inventory_service_creation(self):
        """创建服务"""
        service = InventoryService()
        assert service is not None

    def test_find_item_method(self):
        """测试物品查找方法"""
        service = InventoryService()
        items = [
            BackpackItem(1, "剑", ItemType.WEAPON, Rarity.COMMON, 5, 100.0),
            BackpackItem(2, "盾", ItemType.ARMOR, Rarity.RARE, 3, 200.0),
        ]

        found = service._find_item(items, 1)
        assert found is not None
        assert found.name == "剑"

        not_found = service._find_item(items, 999)
        assert not_found is None

    def test_validate_quantity_valid(self):
        """验证合法数量"""
        service = InventoryService()
        # 不应该抛出异常
        service._validate_quantity(5, 10)

    def test_validate_quantity_zero(self):
        """验证零数量"""
        service = InventoryService()
        from src.domain import ValidationException
        with pytest.raises(ValidationException):
            service._validate_quantity(0, 10)

    def test_validate_quantity_exceeds(self):
        """验证超过最大数量"""
        service = InventoryService()
        from src.domain import ValidationException
        with pytest.raises(ValidationException):
            service._validate_quantity(15, 10)
