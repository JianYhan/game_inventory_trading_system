import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header(player=None):
    if player:
        print(f"  Player: {player.name} | Gold: {player.gold:.0f}")
    print("=" * 50)


def prompt_int(prompt_text: str) -> int | None:
    raw = input(prompt_text).strip()
    if not raw.isdigit():
        print("Please enter a valid number.")
        return None
    return int(raw)


def prompt_float(prompt_text: str) -> float | None:
    raw = input(prompt_text).strip()
    try:
        return float(raw)
    except ValueError:
        print("Please enter a valid number.")
        return None


def prompt_choice(prompt_text: str, valid: set[int]) -> int | None:
    value = prompt_int(prompt_text)
    if value is None:
        return None
    if value not in valid:
        print("Invalid option, please try again.")
        return None
    return value


def confirm(prompt_text: str) -> bool:
    raw = input(f"{prompt_text} (yes/no): ").strip().lower()
    return raw in ("yes", "y")
