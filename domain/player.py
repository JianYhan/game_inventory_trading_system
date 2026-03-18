from __future__ import annotations
from domain.backpack import Backpack


class Player:
    def __init__(self, player_id: str, name: str, gold: float = 1000.0, level: int = 1):
        self.player_id = player_id
        self.name = name
        self.gold = gold
        self.level = level
        self.backpack = Backpack()

    def earn_gold(self, amount: float):
        self.gold += amount

    def spend_gold(self, amount: float) -> bool:
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "gold": self.gold,
            "level": self.level,
            "backpack": self.backpack.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        p = cls(data["player_id"], data["name"], data.get("gold", 1000.0), data.get("level", 1))
        if "backpack" in data:
            p.backpack = Backpack.from_dict(data["backpack"])
        return p

    def __repr__(self):
        return f"Player({self.name}, Gold={self.gold:.1f}, Level={self.level})"
