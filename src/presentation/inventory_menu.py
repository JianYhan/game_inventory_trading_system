from .utils import clear_screen, print_header, prompt_choice, prompt_float, prompt_int, confirm
from ..domain import OrderStatus


def show_inventory_menu(player, inventory_service, market_service):
    while True:
        clear_screen()
        print_header(player)
        print("  [BACKPACK]")
        print("=" * 50)

        resp = inventory_service.get_backpack_grouped(player.player_id)
        groups: dict = resp.data or {}

        if not groups:
            print("  Your backpack is empty.")
            input("\nPress Enter to return...")
            return

        type_list = list(groups.keys())
        for i, t in enumerate(type_list, 1):
            count = sum(item.quantity for item in groups[t])
            print(f"  [{i}] {t} ({count} items)")
        print("  [0] Back")

        choice = prompt_choice("\nSelect type: ", set(range(len(type_list) + 1)))
        if choice is None:
            continue
        if choice == 0:
            return

        selected_type = type_list[choice - 1]
        items = groups[selected_type]
        _show_item_list(player, items, inventory_service)

        resp = inventory_service.get_backpack_grouped(player.player_id)
        groups = resp.data or {}


def _show_item_list(player, items, inventory_service):
    while True:
        clear_screen()
        print_header(player)
        print(f"  Items — {items[0].item_type.value if items else ''}")
        print("=" * 50)
        print(f"  {'#':<4} {'Name':<22} {'Rarity':<12} {'Qty':<5} {'Base Price':<12} {'Suggested'}")
        print("-" * 70)

        for i, item in enumerate(items, 1):
            lo = item.sell_price * 0.8
            hi = item.sell_price * 1.2
            print(f"  [{i}]  {item.name:<22} {item.rarity.label:<12} {item.quantity:<5} {item.sell_price:<12.0f} {lo:.0f}~{hi:.0f}")

        print("  [0] Back")
        choice = prompt_choice("\nSelect item to sell (0=back): ", set(range(len(items) + 1)))
        if choice is None:
            continue
        if choice == 0:
            return

        target = items[choice - 1]
        if not confirm(f"Sell {target.name}?"):
            continue

        lo = target.sell_price * 0.8
        hi = target.sell_price * 1.2
        price = prompt_float(f"Enter price ({lo:.0f}~{hi:.0f}): ")
        if price is None:
            continue
        qty = prompt_int(f"Enter quantity (1~{target.quantity}): ")
        if qty is None:
            continue

        resp = inventory_service.sell_item(player.player_id, target.item_id, qty, price)
        print(f"\n  {'[OK]' if resp.status.value == 'Success' else '[FAIL]'} {resp.message}")
        if resp.player:
            player.gold = resp.player.gold
        input("Press Enter to continue...")

        resp2 = inventory_service.get_backpack_grouped(player.player_id)
        groups = resp2.data or {}
        items = groups.get(target.item_type.value, [])
        if not items:
            return
