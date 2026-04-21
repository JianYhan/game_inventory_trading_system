from __future__ import annotations
from data_structures.doubly_linked_list import DoublyLinkedList


class Backpack:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self._items = DoublyLinkedList()  # stores (item_id, quantity) tuples

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        # check if item already exists — stacking never needs a new slot
        node = self._items.find(lambda x: x[0] == item_id)
        if node:
            node.data = (item_id, node.data[1] + quantity)
            return True
        # new slot required — check capacity first
        if self.total_slots() >= self.capacity:
            return False
        self._items.append((item_id, quantity))
        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        node = self._items.find(lambda x: x[0] == item_id)
        if not node:
            return False
        current_qty = node.data[1]
        if current_qty < quantity:
            return False
        if current_qty == quantity:
            self._items.remove(node)
        else:
            node.data = (item_id, current_qty - quantity)
        return True

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        node = self._items.find(lambda x: x[0] == item_id)
        return node is not None and node.data[1] >= quantity

    def get_quantity(self, item_id: str) -> int:
        node = self._items.find(lambda x: x[0] == item_id)
        return node.data[1] if node else 0

    def total_slots(self) -> int:
        return self._items.size()

    def all_items(self) -> list:
        return list(self._items.iter())

    def to_dict(self) -> dict:
        return {
            "capacity": self.capacity,
            "items": [{"item_id": iid, "quantity": qty} for iid, qty in self._items.iter()]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Backpack":
        bp = cls(data.get("capacity", 20))
        for entry in data.get("items", []):
            bp.add_item(entry["item_id"], entry["quantity"])
        return bp
