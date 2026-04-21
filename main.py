import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.repository import initialize
from src.service import PlayerService, InventoryService, MarketService, TradeService, SystemService
from src.presentation import show_entry_menu, show_main_menu


def main():
    initialize()

    player_service = PlayerService()
    inventory_service = InventoryService()
    market_service = MarketService(inventory_service)
    trade_service = TradeService()
    system_service = SystemService()

    player = show_entry_menu(player_service, system_service)
    if player is None:
        return

    show_main_menu(player, inventory_service, market_service, trade_service, system_service)


if __name__ == "__main__":
    main()
