import os
from typing import Optional
from domain.player import Player
from services.player_service import PlayerService
from services.inventory_service import InventoryService
from services.market_service import MarketService
from services.trade_service import TradeService
from services.system_service import SystemService
from repository.item_repository import ItemRepository


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def header(title: str):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


class CLI:
    def __init__(self,
                 player_svc: PlayerService,
                 inventory_svc: InventoryService,
                 market_svc: MarketService,
                 trade_svc: TradeService,
                 system_svc: SystemService,
                 item_repo: ItemRepository):
        self._player_svc = player_svc
        self._inventory_svc = inventory_svc
        self._market_svc = market_svc
        self._trade_svc = trade_svc
        self._system_svc = system_svc
        self._item_repo = item_repo
        self._current_player: Optional[Player] = None

    # ------------------------------------------------------------------ helpers
    def _select_player(self) -> Optional[Player]:
        players = self._player_svc.list_players()
        if not players:
            print("No players found.")
            return None
        print("\nSelect a player:")
        for i, p in enumerate(players, 1):
            print(f"  {i}. {p.name}  (Gold: {p.gold:.1f}, Level: {p.level})")
        choice = input("Enter number: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(players):
                return players[idx]
        except ValueError:
            pass
        print("Invalid choice.")
        return None

    def _item_name(self, item_id: str) -> str:
        item = self._item_repo.find_by_id(item_id)
        return item.name if item else item_id

    # ---------------------------------------------------------------- main menu
    def run(self):
        while True:
            clear()
            header("Game Inventory & Trading System")
            print("  1. Player Management")
            print("  2. Inventory Management")
            print("  3. Market")
            print("  4. Trade History")
            print("  5. System Info")
            print("  0. Exit")
            choice = input("\nChoice: ").strip()
            if choice == "1":
                self._player_menu()
            elif choice == "2":
                self._inventory_menu()
            elif choice == "3":
                self._market_menu()
            elif choice == "4":
                self._trade_history_menu()
            elif choice == "5":
                self._system_menu()
            elif choice == "0":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice.")
                pause()

    # -------------------------------------------------------------- player menu
    def _player_menu(self):
        while True:
            clear()
            header("Player Management")
            cur = f"[Current: {self._current_player.name}]" if self._current_player else ""
            print(f"  {cur}")
            print("  1. List All Players")
            print("  2. Switch Current Player")
            print("  3. Create New Player")
            print("  4. Delete Player")
            print("  0. Back")
            choice = input("\nChoice: ").strip()
            if choice == "1":
                self._list_players()
            elif choice == "2":
                p = self._select_player()
                if p:
                    self._current_player = p
                    print(f"Switched to player: {p.name}")
                pause()
            elif choice == "3":
                self._create_player()
            elif choice == "4":
                self._delete_player()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
                pause()

    def _list_players(self):
        clear()
        header("All Players")
        for p in self._player_svc.list_players():
            print(f"  [{p.player_id}] {p.name}  Gold={p.gold:.1f}  Level={p.level}  Items={p.backpack.total_slots()}")
        pause()

    def _create_player(self):
        name = input("Enter player name: ").strip()
        if not name:
            print("Name cannot be empty.")
            pause()
            return
        gold_str = input("Starting gold (default 1000): ").strip()
        gold = float(gold_str) if gold_str else 1000.0
        player = self._player_svc.create_player(name, gold)
        print(f"Created player: {player.name} (ID: {player.player_id})")
        pause()

    def _delete_player(self):
        p = self._select_player()
        if not p:
            pause()
            return
        confirm = input(f"Delete {p.name}? (yes/no): ").strip().lower()
        if confirm == "yes":
            self._player_svc.delete_player(p.player_id)
            if self._current_player and self._current_player.player_id == p.player_id:
                self._current_player = None
            print(f"Deleted {p.name}.")
        pause()

    # ----------------------------------------------------------- inventory menu
    def _inventory_menu(self):
        while True:
            clear()
            header("Inventory Management")
            if not self._current_player:
                print("  No player selected. Please select a player first.")
                pause()
                return
            p = self._current_player
            print(f"  Player: {p.name}  Gold: {p.gold:.1f}  Slots: {p.backpack.total_slots()}/{p.backpack.capacity}")
            print("  1. View Inventory")
            print("  2. Add Item")
            print("  3. Remove Item")
            print("  4. Sort by Price")
            print("  5. Search Item")
            print("  6. Undo Last Action")
            print("  0. Back")
            choice = input("\nChoice: ").strip()
            if choice == "1":
                self._view_inventory(p)
            elif choice == "2":
                self._add_item_to_inventory(p)
            elif choice == "3":
                self._remove_item_from_inventory(p)
            elif choice == "4":
                self._sorted_inventory(p)
            elif choice == "5":
                self._search_inventory(p)
            elif choice == "6":
                msg = self._inventory_svc.undo_last(p)
                print(msg if msg else "Nothing to undo.")
                pause()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
                pause()

    def _view_inventory(self, player: Player):
        clear()
        header(f"{player.name}'s Inventory")
        items = self._inventory_svc.get_inventory(player)
        if not items:
            print("  Inventory is empty.")
        for item, qty in items:
            print(f"  [{item.item_id}] {item.name:20s} {item.item_type:10s} {item.rarity:10s} x{qty}  ${item.base_price}")
        pause()

    def _add_item_to_inventory(self, player: Player):
        clear()
        header("Add Item")
        all_items = self._item_repo.all()
        for i, item in enumerate(all_items, 1):
            print(f"  {i}. [{item.item_id}] {item.name}  ({item.item_type}, {item.rarity})  ${item.base_price}")
        choice = input("Select item number: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_items):
                item = all_items[idx]
                qty_str = input("Quantity (default 1): ").strip()
                qty = int(qty_str) if qty_str else 1
                if self._inventory_svc.add_item(player, item.item_id, qty):
                    print(f"Added {item.name} x{qty} to inventory.")
                else:
                    print("Failed: inventory full or item not found.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
        pause()

    def _remove_item_from_inventory(self, player: Player):
        clear()
        header("Remove Item")
        items = self._inventory_svc.get_inventory(player)
        if not items:
            print("  Inventory is empty.")
            pause()
            return
        for i, (item, qty) in enumerate(items, 1):
            print(f"  {i}. {item.name} x{qty}")
        choice = input("Select item number: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                item, qty = items[idx]
                qty_str = input(f"Quantity to remove (max {qty}): ").strip()
                remove_qty = int(qty_str) if qty_str else 1
                if self._inventory_svc.remove_item(player, item.item_id, remove_qty):
                    print(f"Removed {item.name} x{remove_qty}.")
                else:
                    print("Failed: not enough quantity.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
        pause()

    def _sorted_inventory(self, player: Player):
        clear()
        header("Inventory Sorted by Price (High to Low)")
        items = self._inventory_svc.sort_inventory_by_price(player)
        for item, qty in items:
            print(f"  {item.name:20s} ${item.base_price:8.2f}  x{qty}")
        pause()

    def _search_inventory(self, player: Player):
        keyword = input("Search keyword: ").strip()
        results = self._inventory_svc.search_item_in_inventory(player, keyword)
        if results:
            for item, qty in results:
                print(f"  {item.name} x{qty}")
        else:
            print("No matching items.")
        pause()

    # -------------------------------------------------------------- market menu
    def _market_menu(self):
        while True:
            clear()
            header("Market")
            if not self._current_player:
                print("  No player selected.")
                pause()
                return
            print(f"  Current Player: {self._current_player.name}  Gold: {self._current_player.gold:.1f}")
            print("  1. Browse Active Listings")
            print("  2. Search by Item")
            print("  3. Search by Price Range")
            print("  4. Buy Item")
            print("  5. List Item for Sale")
            print("  6. Cancel My Listing")
            print("  7. Place Buy Order (Queue)")
            print("  8. Process Buy Orders")
            print("  0. Back")
            choice = input("\nChoice: ").strip()
            if choice == "1":
                self._browse_listings()
            elif choice == "2":
                self._search_by_item()
            elif choice == "3":
                self._search_by_price()
            elif choice == "4":
                self._buy_item()
            elif choice == "5":
                self._list_for_sale()
            elif choice == "6":
                self._cancel_listing()
            elif choice == "7":
                self._place_buy_order()
            elif choice == "8":
                trades = self._market_svc.process_order_queue()
                print(f"Processed {len(trades)} order(s).")
                pause()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
                pause()

    def _browse_listings(self):
        clear()
        header("Active Listings")
        listings = self._market_svc.get_active_listings()
        self._print_listings(listings)
        pause()

    def _print_listings(self, listings):
        if not listings:
            print("  No listings found.")
            return
        print(f"  {'ID':12s} {'Item':20s} {'Qty':5s} {'Price/unit':12s} {'Total':10s} Seller")
        print("  " + "-" * 70)
        for l in listings:
            item_name = self._item_name(l.item_id)
            seller = self._player_svc.get_player(l.seller_id)
            seller_name = seller.name if seller else l.seller_id
            print(f"  {l.listing_id:12s} {item_name:20s} {l.quantity:5d} ${l.price_per_unit:10.2f} ${l.total_price():8.2f}  {seller_name}")

    def _search_by_item(self):
        clear()
        header("Search Listings by Item")
        all_items = self._item_repo.all()
        for i, item in enumerate(all_items, 1):
            print(f"  {i}. {item.name}")
        choice = input("Select item number: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_items):
                listings = self._market_svc.search_by_item(all_items[idx].item_id)
                self._print_listings(listings)
        except ValueError:
            print("Invalid input.")
        pause()

    def _search_by_price(self):
        clear()
        header("Search by Price Range")
        try:
            low = float(input("Min price: ").strip())
            high = float(input("Max price: ").strip())
            listings = self._market_svc.search_by_price_range(low, high)
            self._print_listings(listings)
        except ValueError:
            print("Invalid price.")
        pause()

    def _buy_item(self):
        clear()
        header("Buy Item")
        listings = self._market_svc.get_active_listings()
        self._print_listings(listings)
        listing_id = input("\nEnter listing ID to buy: ").strip()
        trade = self._market_svc.buy_item(self._current_player, listing_id)
        if trade:
            print(f"Purchase successful! Trade ID: {trade.trade_id}")
            print(f"Spent: ${trade.total_price:.2f}  Remaining gold: {self._current_player.gold:.1f}")
        else:
            print("Purchase failed. Check listing ID, gold balance, or seller validity.")
        pause()

    def _list_for_sale(self):
        clear()
        header("List Item for Sale")
        p = self._current_player
        items = self._inventory_svc.get_inventory(p)
        if not items:
            print("Your inventory is empty.")
            pause()
            return
        for i, (item, qty) in enumerate(items, 1):
            print(f"  {i}. {item.name} x{qty}  (base: ${item.base_price})")
        try:
            idx = int(input("Select item number: ").strip()) - 1
            item, available_qty = items[idx]
            qty = int(input(f"Quantity (max {available_qty}): ").strip())
            price = float(input("Price per unit: ").strip())
            listing = self._market_svc.list_item(p, item.item_id, qty, price)
            if listing:
                print(f"Listed {item.name} x{qty} @ ${price} each. Listing ID: {listing.listing_id}")
            else:
                print("Failed to create listing.")
        except (ValueError, IndexError):
            print("Invalid input.")
        pause()

    def _cancel_listing(self):
        clear()
        header("Cancel My Listing")
        p = self._current_player
        from repository.listing_repository import ListingRepository
        my_listings = [l for l in self._market_svc.get_active_listings() if l.seller_id == p.player_id]
        if not my_listings:
            print("You have no active listings.")
            pause()
            return
        self._print_listings(my_listings)
        listing_id = input("Enter listing ID to cancel: ").strip()
        if self._market_svc.cancel_listing(p, listing_id):
            print("Listing cancelled. Item returned to inventory.")
        else:
            print("Failed to cancel listing.")
        pause()

    def _place_buy_order(self):
        clear()
        header("Place Buy Order")
        all_items = self._item_repo.all()
        for i, item in enumerate(all_items, 1):
            print(f"  {i}. {item.name}")
        try:
            idx = int(input("Select item: ").strip()) - 1
            item = all_items[idx]
            max_price = float(input("Maximum price you'll pay: ").strip())
            self._market_svc.enqueue_buy_order(self._current_player.player_id, item.item_id, max_price)
            print(f"Buy order queued for {item.name} @ max ${max_price}.")
        except (ValueError, IndexError):
            print("Invalid input.")
        pause()

    # --------------------------------------------------------- trade history
    def _trade_history_menu(self):
        while True:
            clear()
            header("Trade History")
            if not self._current_player:
                print("  No player selected.")
                pause()
                return
            print(f"  Player: {self._current_player.name}")
            print("  1. My Full Trade History")
            print("  2. My Purchases")
            print("  3. My Sales")
            print("  4. All System Trades")
            print("  0. Back")
            choice = input("\nChoice: ").strip()
            if choice == "1":
                trades = self._trade_svc.get_trades_for_player(self._current_player.player_id)
                self._print_trades(trades)
            elif choice == "2":
                trades = self._trade_svc.get_purchases(self._current_player.player_id)
                self._print_trades(trades)
            elif choice == "3":
                trades = self._trade_svc.get_sales(self._current_player.player_id)
                self._print_trades(trades)
            elif choice == "4":
                trades = self._trade_svc.get_all_trades()
                self._print_trades(trades)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
                pause()

    def _print_trades(self, trades):
        if not trades:
            print("  No trades found.")
            pause()
            return
        clear()
        header("Trade Records")
        for t in trades:
            buyer = self._player_svc.get_player(t.buyer_id)
            seller = self._player_svc.get_player(t.seller_id)
            bname = buyer.name if buyer else t.buyer_id
            sname = seller.name if seller else t.seller_id
            item_name = self._item_name(t.item_id)
            print(f"  [{t.trade_id}] {item_name} x{t.quantity} | ${t.total_price:.2f} | {bname} <- {sname} | {t.traded_at[:10]}")
        pause()

    # --------------------------------------------------------------- system
    def _system_menu(self):
        clear()
        header("System Info")
        stats = self._system_svc.get_system_stats()
        print(f"  Total Players:       {stats['total_players']}")
        print(f"  Active Listings:     {stats['active_listings']}")
        print(f"  Total Trades:        {stats['total_trades']}")
        print(f"  Total Trade Volume:  ${stats['total_trade_volume']:.2f}")
        print("\n  Item Category Tree:")
        for line in self._system_svc.print_category_tree().split("\n"):
            print("  " + line)
        pause()
