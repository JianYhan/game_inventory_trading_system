import json
import os
import time
from ..domain import GameSave, Response
from ..data_structures import Tree
from ..repository import PlayerRepository, ItemRepository, ListingRepository, TradeRepository, ConfigRepository


SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "save.json")


class SystemService:
    def __init__(self):
        self._player_repo = PlayerRepository()
        self._item_repo = ItemRepository()
        self._listing_repo = ListingRepository()
        self._trade_repo = TradeRepository()
        self._config_repo = ConfigRepository()
        self._category_tree = self._build_category_tree()

    def _build_category_tree(self) -> Tree:
        """Build an item catalog tree grouped by item type and rarity."""
        tree = Tree("Item Catalog")

        for item in self._config_repo.find_all():
            type_name = item.item_type.value.lower()
            rarity_name = item.rarity.label
            item_label = f"{item.name} ({item.item_id})"

            if tree.find(type_name) is None:
                tree.insert("Item Catalog", type_name)
            rarity_key = f"{type_name} / {rarity_name}"
            if tree.find(rarity_key) is None:
                tree.insert(type_name, rarity_key)
            tree.insert(rarity_key, item_label, item)

        return tree

    def get_category_tree(self) -> Tree:
        self._category_tree = self._build_category_tree()
        return self._category_tree

    def print_category_tree(self) -> str:
        return "\n".join(self.get_category_tree().to_lines())

    def has_save(self) -> bool:
        return os.path.exists(SAVE_FILE)

    def load_save(self) -> Response:
        if not self.has_save():
            return Response.fail("No save file found.")
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        player = self._player_repo.find_by_id(raw["player_id"])
        if player is None:
            return Response.fail("Save file corrupted: player not found.")
        return Response.ok(data=raw, player=player)

    def save_game(self, player_id: str) -> Response:
        player = self._player_repo.find_by_id(player_id)
        if player is None:
            return Response.fail("Player not found.")
        backpack = self._item_repo.find_by_player(player_id)
        orders = self._listing_repo.find_by_seller(player_id)
        buy_records = self._trade_repo.find_buy_by_player(player_id)
        sell_records = self._trade_repo.find_sell_by_player(player_id)

        save_data = {
            "player_id": player.player_id,
            "player_name": player.name,
            "gold": player.gold,
            "save_time": time.time(),
        }
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        return Response.ok("Game saved.")
