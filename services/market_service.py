import uuid
from typing import Optional
from domain.player import Player
from domain.market_listing import MarketListing
from domain.trade import Trade
from repository.player_repository import PlayerRepository
from repository.item_repository import ItemRepository
from repository.listing_repository import ListingRepository
from repository.trade_repository import TradeRepository
from data_structures.queue import Queue
from data_structures.hash_table import HashTable


class MarketService:
    def __init__(self, player_repo: PlayerRepository, item_repo: ItemRepository,
                 listing_repo: ListingRepository, trade_repo: TradeRepository):
        self._player_repo = player_repo
        self._item_repo = item_repo
        self._listing_repo = listing_repo
        self._trade_repo = trade_repo
        # pending buy orders queue
        self._order_queue: Queue = Queue()
        # hash table for O(1) listing lookup
        self._listing_cache: HashTable = HashTable()
        # price index: maps price -> list of listing_ids (supports multiple listings at same price)
        self._price_index: dict[float, list[str]] = {}
        self._rebuild_indexes()

    def _rebuild_indexes(self):
        self._listing_cache = HashTable()
        self._price_index = {}
        for listing in self._listing_repo.find_active():
            self._listing_cache.put(listing.listing_id, listing)
            if listing.price_per_unit not in self._price_index:
                self._price_index[listing.price_per_unit] = []
            self._price_index[listing.price_per_unit].append(listing.listing_id)

    def list_item(self, seller: Player, item_id: str, quantity: int, price_per_unit: float) -> Optional[MarketListing]:
        if not seller.backpack.has_item(item_id, quantity):
            return None
        item = self._item_repo.find_by_id(item_id)
        if not item:
            return None
        seller.backpack.remove_item(item_id, quantity)
        self._player_repo.save_player(seller)
        listing_id = "lst_" + uuid.uuid4().hex[:8]
        listing = MarketListing(listing_id, seller.player_id, item_id, quantity, price_per_unit)
        self._listing_repo.save_listing(listing)
        if price_per_unit not in self._price_index:
            self._price_index[price_per_unit] = []
        self._price_index[price_per_unit].append(listing_id)
        self._listing_cache.put(listing_id, listing)
        return listing

    def cancel_listing(self, seller: Player, listing_id: str) -> bool:
        listing = self._listing_cache.get(listing_id)
        if not listing or listing.seller_id != seller.player_id or listing.status != "active":
            return False
        listing.status = "cancelled"
        seller.backpack.add_item(listing.item_id, listing.quantity)
        self._player_repo.save_player(seller)
        self._listing_repo.save_listing(listing)
        self._listing_cache.delete(listing_id)
        # remove from price index
        if listing.price_per_unit in self._price_index:
            self._price_index[listing.price_per_unit] = [
                lid for lid in self._price_index[listing.price_per_unit] if lid != listing_id
            ]
            if not self._price_index[listing.price_per_unit]:
                del self._price_index[listing.price_per_unit]
        return True

    def buy_item(self, buyer: Player, listing_id: str) -> Optional[Trade]:
        listing = self._listing_cache.get(listing_id)
        if not listing or listing.status != "active":
            return None
        if listing.seller_id == buyer.player_id:
            return None
        total = listing.total_price()
        if not buyer.spend_gold(total):
            return None
        seller = self._player_repo.find_by_id(listing.seller_id)
        if seller:
            seller.earn_gold(total)
            self._player_repo.save_player(seller)
        buyer.backpack.add_item(listing.item_id, listing.quantity)
        self._player_repo.save_player(buyer)
        listing.status = "sold"
        self._listing_repo.save_listing(listing)
        self._listing_cache.delete(listing_id)
        # remove from price index
        if listing.price_per_unit in self._price_index:
            self._price_index[listing.price_per_unit] = [
                lid for lid in self._price_index[listing.price_per_unit] if lid != listing_id
            ]
            if not self._price_index[listing.price_per_unit]:
                del self._price_index[listing.price_per_unit]
        trade = Trade(
            trade_id="trd_" + uuid.uuid4().hex[:8],
            listing_id=listing_id,
            buyer_id=buyer.player_id,
            seller_id=listing.seller_id,
            item_id=listing.item_id,
            quantity=listing.quantity,
            price_per_unit=listing.price_per_unit,
            total_price=total
        )
        self._trade_repo.add(trade)
        return trade

    def enqueue_buy_order(self, buyer_id: str, item_id: str, max_price: float):
        self._order_queue.enqueue({"buyer_id": buyer_id, "item_id": item_id, "max_price": max_price})

    def process_order_queue(self) -> list[Trade]:
        trades = []
        while not self._order_queue.is_empty():
            order = self._order_queue.dequeue()
            buyer = self._player_repo.find_by_id(order["buyer_id"])
            if not buyer:
                continue
            listings = self._listing_repo.find_by_item(order["item_id"])
            affordable = [l for l in listings if l.price_per_unit <= order["max_price"]]
            if not affordable:
                continue
            best = min(affordable, key=lambda l: l.price_per_unit)
            trade = self.buy_item(buyer, best.listing_id)
            if trade:
                trades.append(trade)
        return trades

    def get_active_listings(self) -> list[MarketListing]:
        return self._listing_repo.find_active()

    def search_by_item(self, item_id: str) -> list[MarketListing]:
        return self._listing_repo.find_by_item(item_id)

    def search_by_price_range(self, low: float, high: float) -> list[MarketListing]:
        results = []
        for price in sorted(self._price_index.keys()):
            if low <= price <= high:
                for listing_id in self._price_index[price]:
                    listing = self._listing_cache.get(listing_id)
                    if listing:
                        results.append(listing)
        return results
