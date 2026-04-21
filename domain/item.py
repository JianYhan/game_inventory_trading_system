from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, item_id: str, name: str, item_type: str, rarity: str, base_price: float, description: str = ""):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.rarity = rarity
        self.base_price = base_price
        self.description = description

    @abstractmethod
    def get_stats(self) -> dict:
        pass

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "item_type": self.item_type,
            "rarity": self.rarity,
            "base_price": self.base_price,
            "description": self.description,
            **self.get_stats()
        }

    def __repr__(self):
        return f"{self.name} [{self.rarity}] (${self.base_price})"


class Weapon(Item):
    def __init__(self, item_id, name, rarity, base_price, attack: int, durability: int, description=""):
        super().__init__(item_id, name, "weapon", rarity, base_price, description)
        self.attack = attack
        self.durability = durability

    def get_stats(self) -> dict:
        return {"attack": self.attack, "durability": self.durability}


class Armor(Item):
    def __init__(self, item_id, name, rarity, base_price, defense: int, durability: int, description=""):
        super().__init__(item_id, name, "armor", rarity, base_price, description)
        self.defense = defense
        self.durability = durability

    def get_stats(self) -> dict:
        return {"defense": self.defense, "durability": self.durability}


class Potion(Item):
    def __init__(self, item_id, name, rarity, base_price, heal_amount: int, description=""):
        super().__init__(item_id, name, "potion", rarity, base_price, description)
        self.heal_amount = heal_amount

    def get_stats(self) -> dict:
        return {"heal_amount": self.heal_amount}


class Material(Item):
    def __init__(self, item_id, name, rarity, base_price, stack_size: int = 99, description=""):
        super().__init__(item_id, name, "material", rarity, base_price, description)
        self.stack_size = stack_size

    def get_stats(self) -> dict:
        return {"stack_size": self.stack_size}


def item_from_dict(data: dict) -> Item:
    t = data.get("item_type")
    if t == "weapon":
        return Weapon(data["item_id"], data["name"], data["rarity"], data["base_price"],
                      data.get("attack", 0), data.get("durability", 100), data.get("description", ""))
    elif t == "armor":
        return Armor(data["item_id"], data["name"], data["rarity"], data["base_price"],
                     data.get("defense", 0), data.get("durability", 100), data.get("description", ""))
    elif t == "potion":
        return Potion(data["item_id"], data["name"], data["rarity"], data["base_price"],
                      data.get("heal_amount", 0), data.get("description", ""))
    elif t == "material":
        return Material(data["item_id"], data["name"], data["rarity"], data["base_price"],
                        data.get("stack_size", 99), data.get("description", ""))
    raise ValueError(f"Unknown item type: {t}")
