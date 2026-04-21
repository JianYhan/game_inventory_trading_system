import json
import os
import time
import uuid
from typing import Optional
from ..domain import (
    ItemConfig, BackpackItem, Player, MarketOrder,
    BuyRecord, SellRecord, GameSave,
    Rarity, ItemType, OrderStatus,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def _load_json(filename: str) -> dict | list:
    path = _path(filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filename: str, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class PlayerRepository:
    _FILE = "players.json"

    def find_by_id(self, player_id: str) -> Optional[Player]:
        data = _load_json(self._FILE)
        raw = data.get(player_id)
        if raw is None:
            return None
        return Player(raw["player_id"], raw["name"], raw["gold"], raw["created_at"])

    def find_by_name(self, name: str) -> Optional[Player]:
        data = _load_json(self._FILE)
        for raw in data.values():
            if raw["name"] == name:
                return Player(raw["player_id"], raw["name"], raw["gold"], raw["created_at"])
        return None

    def save(self, player: Player):
        data = _load_json(self._FILE)
        data[player.player_id] = {
            "player_id": player.player_id,
            "name": player.name,
            "gold": player.gold,
            "created_at": player.created_at,
        }
        _save_json(self._FILE, data)

    def name_exists(self, name: str) -> bool:
        return self.find_by_name(name) is not None


class ItemRepository:
    _FILE = "items.json"

    def find_by_player(self, player_id: str) -> list[BackpackItem]:
        data = _load_json(self._FILE)
        items = []
        for raw in data.get(player_id, {}).values():
            items.append(self._deserialize(raw))
        return items

    def save_item(self, player_id: str, item: BackpackItem):
        data = _load_json(self._FILE)
        data.setdefault(player_id, {})
        data[player_id][str(item.item_id)] = self._serialize(item)
        _save_json(self._FILE, data)

    def remove_item(self, player_id: str, item_id: int):
        data = _load_json(self._FILE)
        data.setdefault(player_id, {}).pop(str(item_id), None)
        _save_json(self._FILE, data)

    def _serialize(self, item: BackpackItem) -> dict:
        return {
            "item_id": item.item_id,
            "name": item.name,
            "item_type": item.item_type.value,
            "rarity": item.rarity.name,
            "quantity": item.quantity,
            "sell_price": item.sell_price,
        }

    def _deserialize(self, raw: dict) -> BackpackItem:
        return BackpackItem(
            raw["item_id"], raw["name"],
            ItemType(raw["item_type"]),
            Rarity[raw["rarity"]],
            raw["quantity"], raw["sell_price"],
        )


class ListingRepository:
    _FILE = "listings.json"

    def find_all_active(self) -> list[MarketOrder]:
        data = _load_json(self._FILE)
        result = []
        for raw in data.values():
            if raw["status"] in (OrderStatus.ON_SALE.value, OrderStatus.PARTIAL.value):
                result.append(self._deserialize(raw))
        return result

    def find_by_seller(self, seller_id: str) -> list[MarketOrder]:
        data = _load_json(self._FILE)
        return [self._deserialize(r) for r in data.values() if r["seller_id"] == seller_id]

    def find_by_id(self, order_id: str) -> Optional[MarketOrder]:
        data = _load_json(self._FILE)
        raw = data.get(order_id)
        return self._deserialize(raw) if raw else None

    def save(self, order: MarketOrder):
        data = _load_json(self._FILE)
        data[order.order_id] = self._serialize(order)
        _save_json(self._FILE, data)

    def _serialize(self, order: MarketOrder) -> dict:
        return {
            "order_id": order.order_id,
            "seller_id": order.seller_id,
            "item_id": order.item_id,
            "item_name": order.item_name,
            "unit_price": order.unit_price,
            "total_quantity": order.total_quantity,
            "remaining_quantity": order.remaining_quantity,
            "status": order.status.value,
            "list_time": order.list_time,
        }

    def _deserialize(self, raw: dict) -> MarketOrder:
        status_map = {s.value: s for s in OrderStatus}
        return MarketOrder(
            raw["order_id"], raw["seller_id"],
            raw["item_id"], raw["item_name"],
            raw["unit_price"], raw["total_quantity"],
            raw["remaining_quantity"],
            status_map[raw["status"]], raw["list_time"],
        )


class TradeRepository:
    _BUY_FILE = "buy_records.json"
    _SELL_FILE = "sell_records.json"

    def save_buy(self, record: BuyRecord):
        data = _load_json(self._BUY_FILE)
        data[record.record_id] = {
            "record_id": record.record_id,
            "buyer_id": record.buyer_id,
            "seller_id": record.seller_id,
            "item_id": record.item_id,
            "item_name": record.item_name,
            "quantity": record.quantity,
            "unit_price": record.unit_price,
            "trade_time": record.trade_time,
        }
        _save_json(self._BUY_FILE, data)

    def save_sell(self, record: SellRecord):
        data = _load_json(self._SELL_FILE)
        data[record.record_id] = {
            "record_id": record.record_id,
            "seller_id": record.seller_id,
            "buyer_id": record.buyer_id,
            "item_id": record.item_id,
            "item_name": record.item_name,
            "quantity": record.quantity,
            "unit_price": record.unit_price,
            "trade_time": record.trade_time,
        }
        _save_json(self._SELL_FILE, data)

    def find_buy_by_player(self, player_id: str) -> list[BuyRecord]:
        data = _load_json(self._BUY_FILE)
        result = []
        for raw in data.values():
            if raw["buyer_id"] == player_id:
                result.append(BuyRecord(**raw))
        return sorted(result, key=lambda r: r.trade_time, reverse=True)

    def find_sell_by_player(self, player_id: str) -> list[SellRecord]:
        data = _load_json(self._SELL_FILE)
        result = []
        for raw in data.values():
            if raw["seller_id"] == player_id:
                result.append(SellRecord(**raw))
        return sorted(result, key=lambda r: r.trade_time, reverse=True)


class ConfigRepository:
    _FILE = "item_config.json"

    def find_all(self) -> list[ItemConfig]:
        data = _load_json(self._FILE)
        return [self._deserialize(r) for r in data.values()]

    def find_by_id(self, item_id: int) -> Optional[ItemConfig]:
        data = _load_json(self._FILE)
        raw = data.get(str(item_id))
        return self._deserialize(raw) if raw else None

    def _deserialize(self, raw: dict) -> ItemConfig:
        return ItemConfig(
            raw["item_id"], raw["name"],
            ItemType(raw["item_type"]),
            Rarity[raw["rarity"]],
            raw["base_price"],
        )
