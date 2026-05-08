from .utils import clear_screen, print_header, prompt_choice, prompt_int, confirm
from .inventory_menu import show_inventory_menu
from .market_menu import show_market_menu
from .profile_menu import show_profile_menu


def show_main_menu(player, inventory_service, market_service, trade_service, system_service):
    while True:
        clear_screen()
        print_header(player)
        print("  [MAIN MENU]")
        print("=" * 50)
        print("  [1] Backpack")
        print("  [2] Market")
        print("  [3] My Profile")
        print("  [4] Item Catalog")
        print("  [0] Save & Exit")

        choice = prompt_choice("\nSelect: ", {0, 1, 2, 3, 4})
        if choice is None:
            continue
        if choice == 0:
            system_service.save_game(player.player_id)
            print("\n  Game saved. Thank you for playing!")
            return
        if choice == 1:
            show_inventory_menu(player, inventory_service, market_service)
        elif choice == 2:
            show_market_menu(player, inventory_service, market_service)
        elif choice == 3:
            show_profile_menu(player, trade_service, market_service)
        elif choice == 4:
            clear_screen()
            print(system_service.print_category_tree())
            input("\nPress Enter...")


def show_entry_menu(player_service, system_service):
    while True:
        clear_screen()
        print("=" * 50)
        print("   GAME INVENTORY & TRADING SYSTEM")
        print("=" * 50)

        has_save = system_service.has_save()
        if has_save:
            print("  [1] Continue")
            print("  [2] New Game")
            print("  [3] Exit")
            valid = {1, 2, 3}
        else:
            print("  [1] New Game")
            print("  [2] Exit")
            valid = {1, 2}

        choice = prompt_int("\nSelect: ")
        if choice is None:
            continue
        if choice not in valid:
            print("Invalid option, please try again.")
            input("Press Enter...")
            continue

        if has_save:
            if choice == 3:
                print("\nThank you for playing!")
                return None
            if choice == 1:
                resp = system_service.load_save()
                if resp.status.value == "Failure":
                    print(f"  [FAIL] {resp.message}")
                    input("Press Enter...")
                    continue
                return resp.player
            if choice == 2:
                player = _create_player(player_service)
                if player:
                    return player
        else:
            if choice == 2:
                print("\nThank you for playing!")
                return None
            if choice == 1:
                player = _create_player(player_service)
                if player:
                    return player


def _create_player(player_service):
    clear_screen()
    print("=" * 50)
    print("  [NEW GAME — Create Your Character]")
    print("=" * 50)
    while True:
        name = input("Enter your character name: ").strip()
        resp = player_service.create_player(name)
        if resp.status.value == "Success":
            print(f"\n  [OK] {resp.message}")
            input("Press Enter to start...")
            return resp.player
        print(f"  [FAIL] {resp.message}")
