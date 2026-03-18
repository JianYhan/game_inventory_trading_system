import json
import os
import uuid

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

DEFAULT_ITEMS = [
    {"item_id": "wpn_001", "name": "Iron Sword", "item_type": "weapon", "rarity": "common",
     "base_price": 50.0, "attack": 15, "durability": 100, "description": "A basic iron sword."},
    {"item_id": "wpn_002", "name": "Flame Blade", "item_type": "weapon", "rarity": "rare",
     "base_price": 300.0, "attack": 45, "durability": 80, "description": "A blade engulfed in flames."},
    {"item_id": "wpn_003", "name": "Shadow Dagger", "item_type": "weapon", "rarity": "uncommon",
     "base_price": 120.0, "attack": 25, "durability": 90, "description": "Swift and deadly."},
    {"item_id": "arm_001", "name": "Leather Armor", "item_type": "armor", "rarity": "common",
     "base_price": 40.0, "defense": 10, "durability": 120, "description": "Basic leather protection."},
    {"item_id": "arm_002", "name": "Dragon Scale", "item_type": "armor", "rarity": "epic",
     "base_price": 800.0, "defense": 80, "durability": 200, "description": "Forged from dragon scales."},
    {"item_id": "arm_003", "name": "Iron Shield", "item_type": "armor", "rarity": "common",
     "base_price": 60.0, "defense": 20, "durability": 150, "description": "A sturdy iron shield."},
    {"item_id": "pot_001", "name": "Health Potion", "item_type": "potion", "rarity": "common",
     "base_price": 20.0, "heal_amount": 50, "description": "Restores 50 HP."},
    {"item_id": "pot_002", "name": "Mega Potion", "item_type": "potion", "rarity": "uncommon",
     "base_price": 80.0, "heal_amount": 200, "description": "Restores 200 HP."},
    {"item_id": "mat_001", "name": "Iron Ore", "item_type": "material", "rarity": "common",
     "base_price": 5.0, "stack_size": 99, "description": "Raw iron ore for crafting."},
    {"item_id": "mat_002", "name": "Dragon Bone", "item_type": "material", "rarity": "rare",
     "base_price": 150.0, "stack_size": 10, "description": "Rare bone from a dragon."},
]

DEFAULT_PLAYERS = [
    {"player_id": "p001", "name": "Arthur", "gold": 2000.0, "level": 10,
     "backpack": {"capacity": 20, "items": [
         {"item_id": "wpn_001", "quantity": 1},
         {"item_id": "pot_001", "quantity": 5},
         {"item_id": "mat_001", "quantity": 20}
     ]}},
    {"player_id": "p002", "name": "Luna", "gold": 1500.0, "level": 7,
     "backpack": {"capacity": 20, "items": [
         {"item_id": "arm_001", "quantity": 1},
         {"item_id": "pot_002", "quantity": 3},
         {"item_id": "mat_002", "quantity": 5}
     ]}},
    {"player_id": "p003", "name": "Zephyr", "gold": 5000.0, "level": 25,
     "backpack": {"capacity": 30, "items": [
         {"item_id": "wpn_002", "quantity": 1},
         {"item_id": "arm_002", "quantity": 1},
         {"item_id": "mat_001", "quantity": 50}
     ]}},
]


class DataInitializer:
    def __init__(self, data_dir: str = DATA_DIR):
        self._dir = os.path.abspath(data_dir)

    def _path(self, filename: str) -> str:
        return os.path.join(self._dir, filename)

    def _is_empty(self, filename: str) -> bool:
        p = self._path(filename)
        if not os.path.exists(p):
            return True
        with open(p, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return len(data) == 0

    def initialize(self):
        os.makedirs(self._dir, exist_ok=True)
        if self._is_empty("items.json"):
            with open(self._path("items.json"), "w", encoding="utf-8") as f:
                json.dump(DEFAULT_ITEMS, f, ensure_ascii=False, indent=2)

        if self._is_empty("players.json"):
            with open(self._path("players.json"), "w", encoding="utf-8") as f:
                json.dump(DEFAULT_PLAYERS, f, ensure_ascii=False, indent=2)

        for fname in ("listings.json", "trades.json"):
            p = self._path(fname)
            if not os.path.exists(p):
                with open(p, "w", encoding="utf-8") as f:
                    json.dump([], f)
