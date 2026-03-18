from domain.player import Player
from domain.market_listing import MarketListing
from domain.trade import Trade
from repository.player_repository import PlayerRepository
from repository.listing_repository import ListingRepository
from repository.trade_repository import TradeRepository
from repository.data_initializer import DataInitializer
from data_structures.tree import Tree


class SystemService:
    def __init__(self, player_repo: PlayerRepository,
                 listing_repo: ListingRepository,
                 trade_repo: TradeRepository):
        self._player_repo = player_repo
        self._listing_repo = listing_repo
        self._trade_repo = trade_repo
        # Item category tree
        self._category_tree = self._build_category_tree()

    def _build_category_tree(self) -> Tree:
        tree = Tree("Items")
        tree.insert("Items", "weapon")
        tree.insert("Items", "armor")
        tree.insert("Items", "potion")
        tree.insert("Items", "material")
        tree.insert("weapon", "sword")
        tree.insert("weapon", "dagger")
        tree.insert("armor", "body")
        tree.insert("armor", "shield")
        tree.insert("potion", "healing")
        tree.insert("material", "ore")
        tree.insert("material", "bone")
        return tree

    def get_category_tree(self) -> Tree:
        return self._category_tree

    def print_category_tree(self) -> str:
        lines = []
        for depth, node in self._category_tree.traverse():
            lines.append("  " * depth + f"- {node.key}")
        return "\n".join(lines)

    def get_system_stats(self) -> dict:
        players = self._player_repo.all()
        listings = self._listing_repo.find_active()
        trades = self._trade_repo.all()
        return {
            "total_players": len(players),
            "active_listings": len(listings),
            "total_trades": len(trades),
            "total_trade_volume": sum(t.total_price for t in trades)
        }

    def initialize_data(self):
        DataInitializer().initialize()
