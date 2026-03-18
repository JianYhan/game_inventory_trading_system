from repository.data_initializer import DataInitializer
from repository.player_repository import PlayerRepository
from repository.item_repository import ItemRepository
from repository.listing_repository import ListingRepository
from repository.trade_repository import TradeRepository
from services.player_service import PlayerService
from services.inventory_service import InventoryService
from services.market_service import MarketService
from services.trade_service import TradeService
from services.system_service import SystemService
from presentation.cli import CLI


def main():
    # Seed default data if files are empty
    DataInitializer().initialize()

    # Repositories
    player_repo = PlayerRepository()
    item_repo = ItemRepository()
    listing_repo = ListingRepository()
    trade_repo = TradeRepository()

    # Services
    player_svc = PlayerService(player_repo)
    inventory_svc = InventoryService(player_repo, item_repo)
    market_svc = MarketService(player_repo, item_repo, listing_repo, trade_repo)
    trade_svc = TradeService(trade_repo)
    system_svc = SystemService(player_repo, listing_repo, trade_repo)

    # Launch CLI
    cli = CLI(player_svc, inventory_svc, market_svc, trade_svc, system_svc, item_repo)
    cli.run()


if __name__ == "__main__":
    main()
