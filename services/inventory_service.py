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
        # undo stack: stores (player_id, action, item_id, quantity)
        self._undo_stack: Stack = Stack()

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
            self._undo_stack.push((player.player_id, "remove", item_id, quantity))
            self._player_repo.save_player(player)
        return success

    def remove_item(self, player: Player, item_id: str, quantity: int = 1) -> bool:
        success = player.backpack.remove_item(item_id, quantity)
        if success:
            self._undo_stack.push((player.player_id, "add", item_id, quantity))
            self._player_repo.save_player(player)
        return success

    def undo_last(self, player: Player) -> Optional[str]:
        if self._undo_stack.is_empty():
            return None
        pid, action, item_id, qty = self._undo_stack.pop()
        if pid != player.player_id:
            # put it back, not for this player
            self._undo_stack.push((pid, action, item_id, qty))
            return None
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
