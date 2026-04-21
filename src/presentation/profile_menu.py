import time
from .utils import clear_screen, print_header, prompt_choice, confirm
from ..domain import OrderStatus


def show_profile_menu(player, trade_service, market_service):
    while True:
        clear_screen()
        print_header(player)
        print("  [MY PROFILE]")
        print("=" * 50)
        print("  [1] My Listings")
        print("  [2] My Purchase Records")
        print("  [3] My Sale Records")
        print("  [0] Back")

        choice = prompt_choice("\nSelect: ", {0, 1, 2, 3})
        if choice is None:
            continue
        if choice == 0:
            return
        if choice == 1:
            _show_my_listings(player, trade_service, market_service)
        elif choice == 2:
            _show_buy_records(player, trade_service)
        elif choice == 3:
            _show_sell_records(player, trade_service)


def _show_my_listings(player, trade_service, market_service):
    while True:
        clear_screen()
        print_header(player)
        print("  [MY LISTINGS]")
        print("=" * 50)

        resp = trade_service.get_my_listings(player.player_id)
        orders = resp.data or []
        if not orders:
            print("  No listings found.")
            input("\nPress Enter to return...")
            return

        active = [o for o in orders if o.status in (OrderStatus.ON_SALE, OrderStatus.PARTIAL)]
        inactive = [o for o in orders if o.status not in (OrderStatus.ON_SALE, OrderStatus.PARTIAL)]
        combined = active + inactive

        print(f"  {'#':<4} {'Item':<22} {'Price':<10} {'Rem':<5} {'Status'}")
        print("-" * 60)
        for i, order in enumerate(combined, 1):
            print(f"  [{i}]  {order.item_name:<22} {order.unit_price:<10.0f} {order.remaining_quantity:<5} {order.status.value}")

        print("  [0] Back  |  Enter # to delist an active listing")
        choice = prompt_choice("\nSelect: ", set(range(len(combined) + 1)))
        if choice is None:
            continue
        if choice == 0:
            return

        order = combined[choice - 1]
        if order.status not in (OrderStatus.ON_SALE, OrderStatus.PARTIAL):
            print("  This listing is no longer active.")
            input("Press Enter to continue...")
            continue

        if confirm(f"Delist '{order.item_name}'?"):
            resp = market_service.delist(player.player_id, order.order_id)
            print(f"\n  {'[OK]' if resp.status.value == 'Success' else '[FAIL]'} {resp.message}")
            input("Press Enter to continue...")


def _show_buy_records(player, trade_service):
    clear_screen()
    print_header(player)
    print("  [MY PURCHASE RECORDS]")
    print("=" * 50)

    resp = trade_service.get_my_buy_records(player.player_id)
    records = resp.data or []
    if not records:
        print("  No purchase records.")
    else:
        print(f"  {'Item':<22} {'Qty':<5} {'Price':<10} {'Total':<10} {'Time'}")
        print("-" * 70)
        for r in records:
            t = time.strftime("%m-%d %H:%M", time.localtime(r.trade_time))
            print(f"  {r.item_name:<22} {r.quantity:<5} {r.unit_price:<10.0f} {r.total_price:<10.0f} {t}")
    input("\nPress Enter to return...")


def _show_sell_records(player, trade_service):
    clear_screen()
    print_header(player)
    print("  [MY SALE RECORDS]")
    print("=" * 50)

    resp = trade_service.get_my_sell_records(player.player_id)
    records = resp.data or []
    if not records:
        print("  No sale records.")
    else:
        print(f"  {'Item':<22} {'Qty':<5} {'Price':<10} {'Total':<10} {'Time'}")
        print("-" * 70)
        for r in records:
            t = time.strftime("%m-%d %H:%M", time.localtime(r.trade_time))
            print(f"  {r.item_name:<22} {r.quantity:<5} {r.unit_price:<10.0f} {r.total_price:<10.0f} {t}")
    input("\nPress Enter to return...")
