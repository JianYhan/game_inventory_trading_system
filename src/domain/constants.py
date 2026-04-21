"""
游戏常量配置

集中管理所有魔法数字和业务规则配置
"""

from typing import Tuple
from .enums import Rarity


class PlayerConfig:
    """玩家相关配置"""
    INITIAL_GOLD = 1000.0
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 12


class PriceConfig:
    """价格相关配置"""
    MIN_PRICE_FACTOR = 0.8
    MAX_PRICE_FACTOR = 1.2

    @classmethod
    def calculate_range(cls, base_price: float) -> Tuple[float, float]:
        """计算价格范围"""
        return base_price * cls.MIN_PRICE_FACTOR, base_price * cls.MAX_PRICE_FACTOR

    @classmethod
    def is_valid_price(cls, price: float, base_price: float) -> bool:
        """检查价格是否在有效范围内"""
        min_price, max_price = cls.calculate_range(base_price)
        return min_price <= price <= max_price

    @classmethod
    def format_price_range(cls, base_price: float) -> str:
        """格式化价格范围提示"""
        min_price, max_price = cls.calculate_range(base_price)
        return f"{min_price:.0f} - {max_price:.0f}"


class MarketConfig:
    """市场相关配置"""
    SYSTEM_SELLER_ID = "SYSTEM"
    RESTOCK_MIN_QTY = 1
    RESTOCK_MAX_QTY = 5


class RarityWeights:
    """稀有度权重配置（用于系统上新）"""
    COMMON = 6
    RARE = 3
    EPIC = 1
    LEGENDARY = 1

    @classmethod
    def get_weights(cls) -> list:
        """获取权重列表"""
        return [Rarity.COMMON] * cls.COMMON + \
               [Rarity.RARE] * cls.RARE + \
               [Rarity.EPIC] * cls.EPIC + \
               [Rarity.LEGENDARY] * cls.LEGENDARY


class ValidationConfig:
    """验证相关配置"""
    MIN_QUANTITY = 1
    MAX_QUANTITY_DISPLAY = 9999


class MenuConfig:
    """菜单相关配置"""
    BACK_OPTION = "0"
    EXIT_OPTION = "0"
