import uuid
from typing import Optional
from domain.player import Player
from repository.player_repository import PlayerRepository
from data_structures.hash_table import HashTable


class PlayerService:
    def __init__(self, player_repo: PlayerRepository):
        self._repo = player_repo
        self._cache: HashTable = HashTable()
        for p in self._repo.all():
            self._cache.put(p.player_id, p)

    def get_player(self, player_id: str) -> Optional[Player]:
        cached = self._cache.get(player_id)
        if cached:
            return cached
        player = self._repo.find_by_id(player_id)
        if player:
            self._cache.put(player_id, player)
        return player

    def get_by_name(self, name: str) -> Optional[Player]:
        for p in self._cache.values():
            if p.name == name:
                return p
        return None

    def list_players(self) -> list[Player]:
        return list(self._cache.values())

    def create_player(self, name: str, gold: float = 1000.0) -> Player:
        player_id = "p" + uuid.uuid4().hex[:6]
        player = Player(player_id, name, gold)
        self._repo.save_player(player)
        self._cache.put(player_id, player)
        return player

    def save_player(self, player: Player):
        self._repo.save_player(player)
        self._cache.put(player.player_id, player)

    def delete_player(self, player_id: str) -> bool:
        self._cache.delete(player_id)
        return self._repo.delete(player_id)
