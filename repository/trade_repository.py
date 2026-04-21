import json
import os
from domain.trade import Trade

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trades.json")


class TradeRepository:
    def __init__(self, path: str = DATA_PATH):
        self._path = os.path.abspath(path)
        self._trades: list[Trade] = []
        self.load()

    def load(self):
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            self._trades = [Trade.from_dict(d) for d in data]

    def save(self):
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self._trades], f, ensure_ascii=False, indent=2)

    def add(self, trade: Trade):
        self._trades.append(trade)
        self.save()

    def find_by_player(self, player_id: str) -> list[Trade]:
        return [t for t in self._trades if t.buyer_id == player_id or t.seller_id == player_id]

    def find_by_buyer(self, buyer_id: str) -> list[Trade]:
        return [t for t in self._trades if t.buyer_id == buyer_id]

    def find_by_seller(self, seller_id: str) -> list[Trade]:
        return [t for t in self._trades if t.seller_id == seller_id]

    def all(self) -> list[Trade]:
        return list(self._trades)
