import json
import os
from typing import Optional
from domain.item import Item, item_from_dict

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "items.json")


class ItemRepository:
    def __init__(self, path: str = DATA_PATH):
        self._path = os.path.abspath(path)
        self._items: dict[str, Item] = {}
        self.load()

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            self._items = {d["item_id"]: item_from_dict(d) for d in data}

    def save(self):
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([i.to_dict() for i in self._items.values()], f, ensure_ascii=False, indent=2)

    def find_by_id(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def find_by_type(self, item_type: str) -> list[Item]:
        return [i for i in self._items.values() if i.item_type == item_type]

    def all(self) -> list[Item]:
        return list(self._items.values())

    def save_item(self, item: Item):
        self._items[item.item_id] = item
        self.save()
