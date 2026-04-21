import time
import uuid
from dataclasses import dataclass, field
from typing import Optional, Any
from .enums import Rarity, ItemType, OrderStatus, ResultStatus


@dataclass
class ItemConfig:
    item_id: int
    name: str
    item_type: ItemType
    rarity: Rarity
    base_price: float

    @property
    def rarity_multiplier(self) -> float:
        return self.rarity.multiplier

    @property
    def sell_price(self) -> float:
        return self.base_price * self.rarity_multiplier


@dataclass
class BackpackItem:
    item_id: int
    name: str
    item_type: ItemType
    rarity: Rarity
    quantity: int
    sell_price: float


@dataclass
class Player:
    player_id: str
    name: str
    gold: float
    created_at: float = field(default_factory=time.time)

    def add_gold(self, amount: float):
        self.gold += amount

    def deduct_gold(self, amount: float) -> bool:
        if self.gold < amount:
            return False
        self.gold -= amount
        return True


@dataclass
class MarketOrder:
    order_id: str
    seller_id: str
    item_id: int
    item_name: str
    unit_price: float
    total_quantity: int
    remaining_quantity: int
    status: OrderStatus
    list_time: float = field(default_factory=time.time)


@dataclass
class BuyRecord:
    record_id: str
    buyer_id: str
    seller_id: str
    item_id: int
    item_name: str
    quantity: int
    unit_price: float
    trade_time: float = field(default_factory=time.time)

    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity


@dataclass
class SellRecord:
    record_id: str
    seller_id: str
    buyer_id: str
    item_id: int
    item_name: str
    quantity: int
    unit_price: float
    trade_time: float = field(default_factory=time.time)

    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity


@dataclass
class GameSave:
    player_id: str
    player_name: str
    gold: float
    backpack_items: list
    my_orders: list
    buy_records: list
    sell_records: list
    save_time: float = field(default_factory=time.time)


@dataclass
class Response:
    status: ResultStatus
    message: str
    data: Any = None
    player: Optional[Player] = None

    @property
    def is_success(self) -> bool:
        """检查操作是否成功"""
        return self.status == ResultStatus.SUCCESS

    @classmethod
    def ok(cls, message: str = "Success", data=None, player=None):
        return cls(ResultStatus.SUCCESS, message, data, player)

    @classmethod
    def fail(cls, message: str):
        return cls(ResultStatus.FAILURE, message)
