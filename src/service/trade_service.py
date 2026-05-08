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

    def _load_records(self, records, target_list: DoublyLinkedList) -> DoublyLinkedList:
        """Process records through a FIFO queue into a linked-list store."""
        self._record_queue = Queue()
        target_list = DoublyLinkedList()

        for record in records:
            self._record_queue.enqueue(record)

        while not self._record_queue.is_empty():
            target_list.append(self._record_queue.dequeue())

        return target_list

    def get_my_buy_records(self, player_id: str) -> Response:
        records = self._trade_repo.find_buy_by_player(player_id)
        self._buy_records = self._load_records(records, self._buy_records)
        return Response.ok(data=self._buy_records.to_list())

    def get_my_sell_records(self, player_id: str) -> Response:
        records = self._trade_repo.find_sell_by_player(player_id)
        self._sell_records = self._load_records(records, self._sell_records)
        return Response.ok(data=self._sell_records.to_list())

    def get_my_listings(self, player_id: str) -> Response:
        orders = self._listing_repo.find_by_seller(player_id)
        orders.sort(key=lambda o: o.list_time, reverse=True)
        return Response.ok(data=orders)
