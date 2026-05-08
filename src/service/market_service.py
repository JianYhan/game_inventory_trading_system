import uuid
import time
import random
import logging
from typing import Optional
from ..domain import (
    MarketOrder, BuyRecord, SellRecord, BackpackItem, Response,
    OrderStatus, Rarity, ItemType,
    PriceConfig, MarketConfig, RarityWeights,
    ErrorMessages, SuccessMessages,
    handle_exceptions, ItemNotFoundException,
    PlayerNotFoundException, ValidationException,
    InsufficientGoldException
)
from ..data_structures import BinarySearchTree, HashTable, Queue
from ..repository import ListingRepository, TradeRepository, PlayerRepository, ItemRepository, ITEM_CONFIG
from .inventory_service import InventoryService

logger = logging.getLogger(__name__)


class MarketService:
    def __init__(self, inventory_service: InventoryService):
        self._listing_repo = ListingRepository()
        self._trade_repo = TradeRepository()
        self._player_repo = PlayerRepository()
        self._item_repo = ItemRepository()
        self._inventory = inventory_service
        self._restock_queue: Queue = Queue()
        self._listing_index: HashTable = HashTable()
        self._price_bst: BinarySearchTree = BinarySearchTree()
        logger.info("MarketService initialized")

    def _price_key(self, order: MarketOrder):
        return (order.unit_price, order.list_time, order.order_id)

    def _rebuild_market_structures(self) -> None:
        """Load active listings into hash and BST indexes."""
        self._listing_index = HashTable()
        self._price_bst = BinarySearchTree()

        for order in self._listing_repo.find_all_active():
            self._listing_index.put(order.order_id, order)
            self._price_bst.insert(self._price_key(order), order)

    def _get_order_fast(self, order_id: str) -> Optional[MarketOrder]:
        self._rebuild_market_structures()
        order = self._listing_index.get(order_id)
        if order is not None:
            return order
        return self._listing_repo.find_by_id(order_id)

    def _get_sorted_active_listings(self) -> list[MarketOrder]:
        self._rebuild_market_structures()
        return [order for _, order in self._price_bst.inorder_items()]

    def _find_item_in_backpack(self, player_id: str, item_id: int) -> Optional[BackpackItem]:
        """在玩家背包中查找物品"""
        items = self._item_repo.find_by_player(player_id)
        return next((i for i in items if i.item_id == item_id), None)

    def _create_item_from_config(self, item_id: int, quantity: int, item_name: str = None) -> Optional[BackpackItem]:
        """从配置创建物品"""
        cfg = ITEM_CONFIG.get(item_id)
        if not cfg:
            return None

        rarity = Rarity[cfg["rarity"]]
        item_type = ItemType(cfg["item_type"])
        sell_price = cfg["base_price"] * rarity.multiplier
        name = item_name or cfg["name"]

        return BackpackItem(item_id, name, item_type, rarity, quantity, sell_price)

    def _validate_quantity(self, quantity: int, max_qty: int, field_name: str = "quantity") -> None:
        """验证数量"""
        if quantity <= 0:
            raise ValidationException(f"{field_name} must be positive.")
        if quantity > max_qty:
            raise ValidationException(
                ErrorMessages.INVALID_QUANTITY.format(available=max_qty)
            )

    @handle_exceptions
    def list_item(self, player_id: str, item_id: int, quantity: int, unit_price: float) -> Response:
        """上架物品到市场"""
        logger.info(f"Player {player_id} listing {quantity}x item {item_id} at {unit_price}")

        # 查找物品
        target = self._find_item_in_backpack(player_id, item_id)
        if target is None:
            raise ItemNotFoundException(ErrorMessages.ITEM_NOT_FOUND)

        # 验证数量
        self._validate_quantity(quantity, target.quantity)

        # 验证价格
        if not PriceConfig.is_valid_price(unit_price, target.sell_price):
            min_price, max_price = PriceConfig.calculate_range(target.sell_price)
            raise ValidationException(
                ErrorMessages.INVALID_PRICE_RANGE.format(min=min_price, max=max_price)
            )

        # 扣除物品
        deduct_resp = self._inventory.deduct_item(player_id, item_id, quantity)
        if not deduct_resp.is_success:
            return deduct_resp

        # 创建订单
        order = MarketOrder(
            order_id=str(uuid.uuid4()),
            seller_id=player_id,
            item_id=item_id,
            item_name=target.name,
            unit_price=unit_price,
            total_quantity=quantity,
            remaining_quantity=quantity,
            status=OrderStatus.ON_SALE,
            list_time=time.time()
        )
        self._listing_repo.save(order)
        self._listing_index.put(order.order_id, order)
        self._price_bst.insert(self._price_key(order), order)

        logger.info(f"Player {player_id} listed order {order.order_id}")
        return Response.ok(
            SuccessMessages.ITEM_LISTED.format(
                quantity=quantity, item=target.name, price=unit_price
            )
        )

    @handle_exceptions
    def get_listings(self) -> Response:
        """获取所有在售挂单"""
        listings = self._get_sorted_active_listings()
        return Response.ok(data=listings)

    @handle_exceptions
    def buy_item(self, buyer_id: str, order_id: str, quantity: int) -> Response:
        """购买市场物品"""
        logger.info(f"Player {buyer_id} buying {quantity} from order {order_id}")

        order = self._get_order_fast(order_id)
        if order is None:
            raise ItemNotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        if order.status not in (OrderStatus.ON_SALE, OrderStatus.PARTIAL):
            raise ValidationException(ErrorMessages.ORDER_NOT_AVAILABLE)

        self._validate_quantity(quantity, order.remaining_quantity, "quantity")

        if buyer_id == order.seller_id:
            raise ValidationException(ErrorMessages.CANNOT_BUY_OWN)

        # 计算费用
        total_cost = order.unit_price * quantity

        # 检查并扣除买家金币
        buyer = self._player_repo.find_by_id(buyer_id)
        if buyer is None:
            raise PlayerNotFoundException(ErrorMessages.PLAYER_NOT_FOUND)

        if not buyer.deduct_gold(total_cost):
            raise InsufficientGoldException(
                ErrorMessages.INSUFFICIENT_GOLD.format(
                    need=total_cost, have=buyer.gold
                )
            )

        self._player_repo.save(buyer)

        # 给卖家加金币
        if order.seller_id != MarketConfig.SYSTEM_SELLER_ID:
            seller = self._player_repo.find_by_id(order.seller_id)
            if seller:
                seller.add_gold(total_cost)
                self._player_repo.save(seller)
                logger.info(f"Seller {order.seller_id} earned {total_cost} gold")

        # 给买家物品
        item = self._create_item_from_config(order.item_id, quantity, order.item_name)
        if item:
            self._inventory.add_item(buyer_id, item)

        # 更新订单状态
        order.remaining_quantity -= quantity
        if order.remaining_quantity == 0:
            order.status = OrderStatus.SOLD_OUT
        else:
            order.status = OrderStatus.PARTIAL
        self._listing_repo.save(order)
        self._rebuild_market_structures()

        # 创建交易记录
        record_id = str(uuid.uuid4())
        buy_record = BuyRecord(
            record_id=record_id,
            buyer_id=buyer_id,
            seller_id=order.seller_id,
            item_id=order.item_id,
            item_name=order.item_name,
            quantity=quantity,
            unit_price=order.unit_price,
            trade_time=time.time()
        )
        sell_record = SellRecord(
            record_id=record_id,
            seller_id=order.seller_id,
            buyer_id=buyer_id,
            item_id=order.item_id,
            item_name=order.item_name,
            quantity=quantity,
            unit_price=order.unit_price,
            trade_time=time.time()
        )
        self._trade_repo.save_buy(buy_record)
        self._trade_repo.save_sell(sell_record)

        logger.info(f"Player {buyer_id} bought {quantity}x {order.item_name}")
        return Response.ok(
            SuccessMessages.ITEM_BOUGHT.format(
                quantity=quantity, item=order.item_name
            ),
            player=buyer
        )

    @handle_exceptions
    def delist(self, player_id: str, order_id: str) -> Response:
        """下架自己的挂单"""
        logger.info(f"Player {player_id} delisting order {order_id}")

        order = self._get_order_fast(order_id)
        if order is None:
            raise ItemNotFoundException(ErrorMessages.ORDER_NOT_FOUND)

        if order.seller_id != player_id:
            raise ValidationException("You can only delist your own orders.")

        if order.status not in (OrderStatus.ON_SALE, OrderStatus.PARTIAL):
            raise ValidationException("Order is not active.")

        # 返还物品
        item = self._create_item_from_config(
            order.item_id, order.remaining_quantity, order.item_name
        )
        if item:
            self._inventory.add_item(player_id, item)

        order.status = OrderStatus.DELISTED
        self._listing_repo.save(order)
        self._rebuild_market_structures()

        logger.info(f"Player {player_id} delisted order {order_id}")
        return Response.ok(SuccessMessages.ITEM_DELISTED)

    @handle_exceptions
    def search_listings(self, keyword: str) -> Response:
        """搜索市场挂单"""
        keyword = keyword.strip()
        if not keyword:
            raise ValidationException(ErrorMessages.EMPTY_KEYWORD)

        if len(keyword) > 50:
            raise ValidationException("Search keyword too long (max 50 characters).")

        listings = self._get_sorted_active_listings()
        results = [o for o in listings if keyword.lower() in o.item_name.lower()]

        if not results:
            return Response.fail(f"No listings found for '{keyword}'.")

        return Response.ok(data=results)

    def system_restock(self):
        """系统定时上新"""
        weights = RarityWeights.get_weights()
        chosen = random.choice(weights)

        pool = [cfg for cfg in ITEM_CONFIG.values() if Rarity[cfg["rarity"]] == chosen]
        if not pool:
            logger.warning("No items found for restock")
            return

        item_cfg = random.choice(pool)
        from ..domain.constants import MarketConfig
        quantity = random.randint(
            MarketConfig.RESTOCK_MIN_QTY,
            MarketConfig.RESTOCK_MAX_QTY
        )
        price = item_cfg["base_price"] * chosen.multiplier

        self._restock_queue.enqueue((item_cfg, quantity, price))

        while not self._restock_queue.is_empty():
            cfg, qty, unit_price = self._restock_queue.dequeue()
            rarity = Rarity[cfg["rarity"]]

            order = MarketOrder(
                order_id=str(uuid.uuid4()),
                seller_id=MarketConfig.SYSTEM_SELLER_ID,
                item_id=cfg["item_id"],
                item_name=cfg["name"],
                unit_price=unit_price,
                total_quantity=qty,
                remaining_quantity=qty,
                status=OrderStatus.ON_SALE,
                list_time=time.time()
            )
            self._listing_repo.save(order)
            self._listing_index.put(order.order_id, order)
            self._price_bst.insert(self._price_key(order), order)
            logger.info(f"System restocked: {cfg['name']} x{qty}")
