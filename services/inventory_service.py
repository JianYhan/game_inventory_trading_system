from typing import Optional
from domain.player import Player
from domain.item import Item
from repository.player_repository import PlayerRepository
from repository.item_repository import ItemRepository
from data_structures.stack import Stack


class InventoryService:
    def __init__(self, player_repo: PlayerRepository, item_repo: ItemRepository):
        self._player_repo = player_repo
        self._item_repo = item_repo
        # undo stack per player: dict[player_id, Stack]
        self._undo_stacks: dict[str, Stack] = {}

    def get_inventory(self, player: Player) -> list[tuple]:
        """Returns list of (item, quantity)."""
        result = []
        for item_id, qty in player.backpack.all_items():
            item = self._item_repo.find_by_id(item_id)
            if item:
                result.append((item, qty))
        return result

    def add_item(self, player: Player, item_id: str, quantity: int = 1) -> bool:
        item = self._item_repo.find_by_id(item_id)
        if not item:
            return False
        success = player.backpack.add_item(item_id, quantity)
        if success:
            if player.player_id not in self._undo_stacks:
                self._undo_stacks[player.player_id] = Stack()
            self._undo_stacks[player.player_id].push(("remove", item_id, quantity))
            self._player_repo.save_player(player)
        return success

    def remove_item(self, player: Player, item_id: str, quantity: int = 1) -> bool:
        success = player.backpack.remove_item(item_id, quantity)
        if success:
            if player.player_id not in self._undo_stacks:
                self._undo_stacks[player.player_id] = Stack()
            self._undo_stacks[player.player_id].push(("add", item_id, quantity))
            self._player_repo.save_player(player)
        return success

    def undo_last(self, player: Player) -> Optional[str]:
        if player.player_id not in self._undo_stacks or self._undo_stacks[player.player_id].is_empty():
            return None
        action, item_id, qty = self._undo_stacks[player.player_id].pop()
        if action == "add":
            player.backpack.add_item(item_id, qty)
        else:
            player.backpack.remove_item(item_id, qty)
        self._player_repo.save_player(player)
        return f"Undid: {action} {item_id} x{qty}"

    def sort_inventory_by_price(self, player: Player) -> list[tuple]:
        inventory = self.get_inventory(player)
        return sorted(inventory, key=lambda x: x[0].base_price, reverse=True)

    def search_item_in_inventory(self, player: Player, name: str) -> list[tuple]:
        inventory = self.get_inventory(player)
        return [(item, qty) for item, qty in inventory if name.lower() in item.name.lower()]
