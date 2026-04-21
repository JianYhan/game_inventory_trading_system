import logging
from typing import List, Optional
from ..domain import (
    BackpackItem, Response, ItemType,
    PriceConfig, ErrorMessages, SuccessMessages,
    handle_exceptions, ItemNotFoundException,
    PlayerNotFoundException, ValidationException
)
from ..data_structures import DoublyLinkedList, HashTable, Stack
from ..repository import ItemRepository, PlayerRepository

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self):
        self._item_repo = ItemRepository()
        self._player_repo = PlayerRepository()
        self._backpack_list: DoublyLinkedList = DoublyLinkedList()
        self._backpack_index: HashTable = HashTable()
        self._recent_actions: Stack = Stack()
        logger.info("InventoryService initialized")

    def _find_item(self, items: List[BackpackItem], item_id: int) -> Optional[BackpackItem]:
        """统一的物品查找方法"""
        return next((i for i in items if i.item_id == item_id), None)

    def _validate_quantity(self, quantity: int, max_qty: int) -> None:
        """统一的数量验证"""
        if quantity <= 0:
            raise ValidationException("Quantity must be positive.")
        if quantity > max_qty:
            raise ValidationException(
                ErrorMessages.NOT_ENOUGH_ITEMS.format(quantity=max_qty)
            )

    @handle_exceptions
    def get_backpack(self, player_id: str) -> Response:
        """获取背包物品列表"""
        items = self._item_repo.find_by_player(player_id)
        return Response.ok(data=items)

    @handle_exceptions
    def get_backpack_grouped(self, player_id: str) -> Response:
        """按类型分组的背包"""
        items = self._item_repo.find_by_player(player_id)
        groups: dict[str, list] = {}
        for item in items:
            key = item.item_type.value
            groups.setdefault(key, []).append(item)
        return Response.ok(data=groups)

    @handle_exceptions
    def sell_item(self, player_id: str, item_id: int, quantity: int, price: float) -> Response:
        """出售物品给系统"""
        logger.info(f"Player {player_id} selling {quantity}x item {item_id} at {price}")

        # 查找物品
        items = self._item_repo.find_by_player(player_id)
        target = self._find_item(items, item_id)
        if target is None:
            raise ItemNotFoundException(ErrorMessages.ITEM_NOT_FOUND)

        # 验证数量
        self._validate_quantity(quantity, target.quantity)

        # 验证价格范围
        if not PriceConfig.is_valid_price(price, target.sell_price):
            min_price, max_price = PriceConfig.calculate_range(target.sell_price)
            raise ValidationException(
                ErrorMessages.INVALID_PRICE_RANGE.format(min=min_price, max=max_price)
            )

        # 计算收益
        gold_earned = price * quantity

        # 更新玩家金币
        player = self._player_repo.find_by_id(player_id)
        if player is None:
            raise PlayerNotFoundException(ErrorMessages.PLAYER_NOT_FOUND)

        player.add_gold(gold_earned)
        self._player_repo.save(player)

        # 更新物品数量
        target.quantity -= quantity
        if target.quantity == 0:
            self._item_repo.remove_item(player_id, item_id)
        else:
            self._item_repo.save_item(player_id, target)

        # 记录操作
        action_msg = SuccessMessages.ITEM_SOLD.format(
            quantity=quantity, item=target.name, gold=gold_earned
        )
        self._recent_actions.push(action_msg)

        logger.info(f"Player {player_id} sold {quantity}x {target.name}")
        return Response.ok(action_msg, player=player)

    @handle_exceptions
    def add_item(self, player_id: str, item: BackpackItem) -> Response:
        """添加物品到背包（自动合并同类物品）"""
        logger.debug(f"Adding item {item.item_id} x{item.quantity} to player {player_id}")

        items = self._item_repo.find_by_player(player_id)
        existing = self._find_item(items, item.item_id)

        if existing:
            existing.quantity += item.quantity
            self._item_repo.save_item(player_id, existing)
            logger.debug(f"Merged item {item.item_id}, new quantity: {existing.quantity}")
        else:
            self._item_repo.save_item(player_id, item)
            logger.debug(f"Added new item {item.item_id}")

        return Response.ok(SuccessMessages.ITEM_ADDED)

    @handle_exceptions
    def deduct_item(self, player_id: str, item_id: int, quantity: int) -> Response:
        """从背包扣除物品"""
        logger.info(f"Deducting {quantity}x item {item_id} from player {player_id}")

        items = self._item_repo.find_by_player(player_id)
        target = self._find_item(items, item_id)

        if target is None:
            raise ItemNotFoundException(ErrorMessages.ITEM_NOT_FOUND_GENERIC)

        if target.quantity < quantity:
            raise ValidationException(
                ErrorMessages.NOT_ENOUGH_ITEMS.format(quantity=target.quantity)
            )

        target.quantity -= quantity
        if target.quantity == 0:
            self._item_repo.remove_item(player_id, item_id)
        else:
            self._item_repo.save_item(player_id, target)

        logger.info(f"Deducted {quantity}x item {item_id} from player {player_id}")
        return Response.ok(SuccessMessages.ITEM_DEDUCTED)
