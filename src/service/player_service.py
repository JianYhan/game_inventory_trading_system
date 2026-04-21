import uuid
import time
import logging
from ..domain import (
    Player, BackpackItem, Response, Rarity, ItemType,
    PlayerConfig, ErrorMessages, SuccessMessages,
    handle_exceptions, PlayerNotFoundException, ValidationException
)
from ..data_structures import HashTable
from ..repository import PlayerRepository, ItemRepository, ConfigRepository, ITEM_CONFIG, INITIAL_BACKPACK

logger = logging.getLogger(__name__)


class PlayerService:
    def __init__(self):
        self._player_repo = PlayerRepository()
        self._item_repo = ItemRepository()
        self._config_repo = ConfigRepository()
        self._player_table: HashTable = HashTable()
        self._name_table: HashTable = HashTable()
        logger.info("PlayerService initialized")

    @handle_exceptions
    def create_player(self, name: str) -> Response:
        """创建玩家"""
        logger.info(f"Attempting to create player with name: {name}")

        # 验证名称
        name = name.strip()
        if not name:
            raise ValidationException(ErrorMessages.EMPTY_NAME)

        if not (PlayerConfig.MIN_NAME_LENGTH <= len(name) <= PlayerConfig.MAX_NAME_LENGTH):
            raise ValidationException(
                ErrorMessages.INVALID_NAME_LENGTH.format(
                    min=PlayerConfig.MIN_NAME_LENGTH,
                    max=PlayerConfig.MAX_NAME_LENGTH
                )
            )

        if self._player_repo.name_exists(name):
            raise ValidationException(ErrorMessages.NAME_EXISTS.format(name=name))

        # 创建玩家
        player_id = str(uuid.uuid4())
        player = Player(
            player_id, name,
            PlayerConfig.INITIAL_GOLD,
            time.time()
        )

        # 保存并初始化
        self._player_repo.save(player)
        self._give_initial_items(player_id)
        self._player_table.put(player_id, player)
        self._name_table.put(name, player_id)

        logger.info(f"Player created: {player_id} ({name})")
        return Response.ok(SuccessMessages.PLAYER_CREATED, player=player)

    def _give_initial_items(self, player_id: str):
        """给予初始物品"""
        for entry in INITIAL_BACKPACK:
            cfg = ITEM_CONFIG[entry["item_id"]]
            rarity = Rarity[cfg["rarity"]]
            item_type = ItemType(cfg["item_type"])
            sell_price = cfg["base_price"] * rarity.multiplier
            item = BackpackItem(
                cfg["item_id"], cfg["name"],
                item_type, rarity,
                entry["quantity"], sell_price
            )
            self._item_repo.save_item(player_id, item)
            logger.debug(f"Given initial item {cfg['name']} to player {player_id}")

    @handle_exceptions
    def get_player(self, player_id: str) -> Response:
        """获取玩家信息"""
        # 先查缓存
        cached = self._player_table.get(player_id)
        if cached:
            return Response.ok(data=cached, player=cached)

        # 查数据库
        player = self._player_repo.find_by_id(player_id)
        if player is None:
            raise PlayerNotFoundException(ErrorMessages.PLAYER_NOT_FOUND)

        # 更新缓存
        self._player_table.put(player_id, player)
        return Response.ok(data=player, player=player)

    @handle_exceptions
    def update_gold(self, player_id: str, delta: float) -> Response:
        """更新金币（正数增加，负数减少）"""
        logger.info(f"Updating gold for player {player_id}: delta={delta}")

        player = self._player_repo.find_by_id(player_id)
        if player is None:
            raise PlayerNotFoundException(ErrorMessages.PLAYER_NOT_FOUND)

        # 扣除金币
        if delta < 0:
            if not player.deduct_gold(-delta):
                from ..domain import InsufficientGoldException
                raise InsufficientGoldException(ErrorMessages.INSUFFICIENT_GOLD_SHORT)

        # 增加金币
        if delta > 0:
            player.add_gold(delta)

        # 保存更新
        self._player_repo.save(player)
        self._player_table.put(player_id, player)

        logger.info(f"Gold updated for player {player_id}: new_gold={player.gold}")
        return Response.ok(SuccessMessages.GOLD_UPDATED, player=player)
