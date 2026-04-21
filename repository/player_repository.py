import json
import os
from typing import Optional
from domain.player import Player

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "players.json")


class PlayerRepository:
    def __init__(self, path: str = DATA_PATH):
        self._path = os.path.abspath(path)
        self._players: dict[str, Player] = {}
        self.load()

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            self._players = {p["player_id"]: Player.from_dict(p) for p in data}

    def save(self):
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self._players.values()], f, ensure_ascii=False, indent=2)

    def find_by_id(self, player_id: str) -> Optional[Player]:
        return self._players.get(player_id)

    def find_by_name(self, name: str) -> Optional[Player]:
        for p in self._players.values():
            if p.name == name:
                return p
        return None

    def all(self) -> list[Player]:
        return list(self._players.values())

    def save_player(self, player: Player):
        self._players[player.player_id] = player
        self.save()

    def delete(self, player_id: str) -> bool:
        if player_id in self._players:
            del self._players[player_id]
            self.save()
            return True
        return False
