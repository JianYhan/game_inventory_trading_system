import time
from .utils import clear_screen, print_header, prompt_choice, prompt_float, prompt_int, confirm
from ..domain import OrderStatus


def show_market_menu(player, inventory_service, market_service):
    while True:
        clear_screen()
        print_header(player)
        print("  [MARKET]")
        print("=" * 50)
        print("  [1] View Market Listings")
        print("  [2] List Item for Sale")
        print("  [3] Search Listings")
        print("  [0] Back")

        choice = prompt_choice("\nSelect: ", {0, 1, 2, 3})
        if choice is None:
            continue
        if choice == 0:
            return
        if choice == 1:
            _view_market(player, market_service)
        elif choice == 2:
            _list_item(player, inventory_service, market_service)
        elif choice == 3:
            _search_market(player, market_service)

        resp = market_service._player_repo.find_by_id(player.player_id)
        if resp:
            player.gold = resp.gold


def _view_market(player, market_service):
    while True:
        clear_screen()
        print_header(player)
        print("  [MARKET — All Listings]")
        print("=" * 50)

        resp = market_service.get_listings()
        listings = resp.data or []
        if not listings:
            print("  No active listings.")
            input("\nPress Enter to return...")
            return

        print(f"  {'#':<4} {'Item':<22} {'Seller':<14} {'Price':<10} {'Qty'}")
        print("-" * 60)
        for i, order in enumerate(listings, 1):
            seller = "SYSTEM" if order.seller_id == "SYSTEM" else order.seller_id[:8]
            print(f"  [{i}]  {order.item_name:<22} {seller:<14} {order.unit_price:<10.0f} {order.remaining_quantity}")

        print("  [0] Back")
        choice = prompt_choice("\nSelect listing to buy (0=back): ", set(range(len(listings) + 1)))
        if choice is None:
            continue
        if choice == 0:
            return

        order = listings[choice - 1]
        qty = prompt_int(f"Buy quantity (1~{order.remaining_quantity}): ")
        if qty is None:
            continue

        total = order.unit_price * qty
        if not confirm(f"Buy {qty}x {order.item_name} for {total:.0f} gold?"):
            continue

        resp = market_service.buy_item(player.player_id, order.order_id, qty)
        print(f"\n  {'[OK]' if resp.status.value == 'Success' else '[FAIL]'} {resp.message}")
        if resp.player:
            player.gold = resp.player.gold
        input("Press Enter to continue...")


def _list_item(player, inventory_service, market_service):
    clear_screen()
    print_header(player)
    print("  [LIST ITEM FOR SALE]")
    print("=" * 50)

    resp = inventory_service.get_backpack(player.player_id)
    items = resp.data or []
    if not items:
        print("  Your backpack is empty.")
        input("\nPress Enter to return...")
        return

    print(f"  {'#':<4} {'Item':<22} {'Rarity':<12} {'Qty':<5} {'Suggested'}")
    print("-" * 60)
    for i, item in enumerate(items, 1):
        lo = item.sell_price * 0.8
        hi = item.sell_price * 1.2
        print(f"  [{i}]  {item.name:<22} {item.rarity.label:<12} {item.quantity:<5} {lo:.0f}~{hi:.0f}")

    print("  [0] Back")
    choice = prompt_choice("\nSelect item: ", set(range(len(items) + 1)))
    if choice is None or choice == 0:
        return

    target = items[choice - 1]
    lo = target.sell_price * 0.8
    hi = target.sell_price * 1.2
    price = prompt_float(f"Enter unit price ({lo:.0f}~{hi:.0f}): ")
    if price is None:
        return
    qty = prompt_int(f"Enter quantity (1~{target.quantity}): ")
    if qty is None:
        return

    resp = market_service.list_item(player.player_id, target.item_id, qty, price)
    print(f"\n  {'[OK]' if resp.status.value == 'Success' else '[FAIL]'} {resp.message}")
    input("Press Enter to continue...")


def _search_market(player, market_service):
    clear_screen()
    print_header(player)
    print("  [SEARCH LISTINGS]")
    print("=" * 50)

    keyword = input("Enter item name to search: ").strip()
    resp = market_service.search_listings(keyword)
    if resp.status.value == "Failure":
        print(f"  [FAIL] {resp.message}")
        input("Press Enter to return...")
        return

    listings = resp.data
    print(f"\n  Found {len(listings)} result(s):")
    print(f"  {'#':<4} {'Item':<22} {'Seller':<14} {'Price':<10} {'Qty'}")
    print("-" * 60)
    for i, order in enumerate(listings, 1):
        seller = "SYSTEM" if order.seller_id == "SYSTEM" else order.seller_id[:8]
        print(f"  [{i}]  {order.item_name:<22} {seller:<14} {order.unit_price:<10.0f} {order.remaining_quantity}")
    input("\nPress Enter to return...")
