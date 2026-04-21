import json
import os
import time
from ..domain import GameSave, Response
from ..repository import PlayerRepository, ItemRepository, ListingRepository, TradeRepository


SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "save.json")


class SystemService:
    def __init__(self):
        self._player_repo = PlayerRepository()
        self._item_repo = ItemRepository()
        self._listing_repo = ListingRepository()
        self._trade_repo = TradeRepository()

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
