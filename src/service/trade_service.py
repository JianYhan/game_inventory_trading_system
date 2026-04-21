from ..domain import Response
from ..data_structures import DoublyLinkedList, Queue
from ..repository import TradeRepository, ListingRepository


class TradeService:
    def __init__(self):
        self._trade_repo = TradeRepository()
        self._listing_repo = ListingRepository()
        self._buy_records: DoublyLinkedList = DoublyLinkedList()
        self._sell_records: DoublyLinkedList = DoublyLinkedList()
        self._record_queue: Queue = Queue()

    def get_my_buy_records(self, player_id: str) -> Response:
        records = self._trade_repo.find_buy_by_player(player_id)
        return Response.ok(data=records)

    def get_my_sell_records(self, player_id: str) -> Response:
        records = self._trade_repo.find_sell_by_player(player_id)
        return Response.ok(data=records)

    def get_my_listings(self, player_id: str) -> Response:
        orders = self._listing_repo.find_by_seller(player_id)
        orders.sort(key=lambda o: o.list_time, reverse=True)
        return Response.ok(data=orders)
