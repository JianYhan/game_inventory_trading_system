from enum import Enum


class Rarity(Enum):
    COMMON = ("Common", 1.0)
    RARE = ("Rare", 2.0)
    EPIC = ("Epic", 4.0)
    LEGENDARY = ("Legendary", 8.0)

    def __init__(self, label: str, multiplier: float):
        self.label = label
        self.multiplier = multiplier


class ItemType(Enum):
    WEAPON = "Weapon"
    POTION = "Potion"
    ARMOR = "Armor"
    MATERIAL = "Material"


class OrderStatus(Enum):
    ON_SALE = "On Sale"
    PARTIAL = "Partial"
    SOLD_OUT = "Sold Out"
    DELISTED = "Delisted"


class ResultStatus(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
