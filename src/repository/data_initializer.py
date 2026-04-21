import json
import os
from ..domain import Rarity, ItemType

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

ITEM_CONFIG = {
    1001: {"item_id": 1001, "name": "Wooden Sword", "item_type": ItemType.WEAPON.value, "rarity": Rarity.COMMON.name, "base_price": 50},
    1002: {"item_id": 1002, "name": "Iron Sword", "item_type": ItemType.WEAPON.value, "rarity": Rarity.RARE.name, "base_price": 120},
    1003: {"item_id": 1003, "name": "Silver Blade", "item_type": ItemType.WEAPON.value, "rarity": Rarity.EPIC.name, "base_price": 300},
    1004: {"item_id": 1004, "name": "Dragon Slayer", "item_type": ItemType.WEAPON.value, "rarity": Rarity.LEGENDARY.name, "base_price": 800},
    2001: {"item_id": 2001, "name": "Small Red Potion", "item_type": ItemType.POTION.value, "rarity": Rarity.COMMON.name, "base_price": 30},
    2002: {"item_id": 2002, "name": "Medium Red Potion", "item_type": ItemType.POTION.value, "rarity": Rarity.RARE.name, "base_price": 80},
    2003: {"item_id": 2003, "name": "Large Red Potion", "item_type": ItemType.POTION.value, "rarity": Rarity.EPIC.name, "base_price": 200},
    2004: {"item_id": 2004, "name": "Elixir of Life", "item_type": ItemType.POTION.value, "rarity": Rarity.LEGENDARY.name, "base_price": 600},
    3001: {"item_id": 3001, "name": "Leather Armor", "item_type": ItemType.ARMOR.value, "rarity": Rarity.COMMON.name, "base_price": 60},
    3002: {"item_id": 3002, "name": "Iron Armor", "item_type": ItemType.ARMOR.value, "rarity": Rarity.RARE.name, "base_price": 150},
    3003: {"item_id": 3003, "name": "Mithril Plate", "item_type": ItemType.ARMOR.value, "rarity": Rarity.EPIC.name, "base_price": 400},
    3004: {"item_id": 3004, "name": "Dragon Scale Mail", "item_type": ItemType.ARMOR.value, "rarity": Rarity.LEGENDARY.name, "base_price": 1000},
    4001: {"item_id": 4001, "name": "Iron Ore", "item_type": ItemType.MATERIAL.value, "rarity": Rarity.COMMON.name, "base_price": 20},
    4002: {"item_id": 4002, "name": "Magic Crystal", "item_type": ItemType.MATERIAL.value, "rarity": Rarity.RARE.name, "base_price": 70},
    4003: {"item_id": 4003, "name": "Dragon Heart", "item_type": ItemType.MATERIAL.value, "rarity": Rarity.EPIC.name, "base_price": 250},
    4004: {"item_id": 4004, "name": "Phoenix Feather", "item_type": ItemType.MATERIAL.value, "rarity": Rarity.LEGENDARY.name, "base_price": 700},
}

INITIAL_BACKPACK = [
    {"item_id": 1001, "quantity": 1},
    {"item_id": 2001, "quantity": 1},
    {"item_id": 2002, "quantity": 1},
    {"item_id": 3001, "quantity": 1},
]


def initialize():
    os.makedirs(DATA_DIR, exist_ok=True)
    config_path = os.path.join(DATA_DIR, "item_config.json")
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in ITEM_CONFIG.items()}, f, ensure_ascii=False, indent=2)

    for filename in ("players.json", "items.json", "listings.json", "buy_records.json", "sell_records.json"):
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f)
