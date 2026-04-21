from domain.trade import Trade
from repository.trade_repository import TradeRepository


class TradeService:
    def __init__(self, trade_repo: TradeRepository):
        self._repo = trade_repo

    def get_all_trades(self) -> list[Trade]:
        return self._repo.all()

    def get_trades_for_player(self, player_id: str) -> list[Trade]:
        return self._repo.find_by_player(player_id)

    def get_purchases(self, player_id: str) -> list[Trade]:
        return self._repo.find_by_buyer(player_id)

    def get_sales(self, player_id: str) -> list[Trade]:
        return self._repo.find_by_seller(player_id)

    def get_trade_volume(self, player_id: str) -> float:
        return sum(t.total_price for t in self._repo.find_by_player(player_id))
