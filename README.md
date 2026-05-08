# Game Inventory & Trading System

A command-line game inventory and marketplace system implemented in Python. The project models players, backpacks, item catalogs, market listings, and trade history with a layered architecture and several custom data structures.

## Features

- Create a new player and continue from an existing save file.
- Manage a backpack grouped by item type.
- Sell items directly for gold within a validated price range.
- List backpack items on the market for other players to buy.
- Browse active market listings sorted by price.
- Search market listings by item name.
- Delist your own active market orders and return remaining items to your backpack.
- View player profile data, own listings, buy records, and sell records.
- Display an item catalog tree grouped by item type and rarity.
- Persist players, items, listings, trade records, item configuration, and saves as JSON files.

## Project Highlights

### Custom Data Structures

The project includes custom implementations under `src/data_structures/`:

- `Stack` for recent inventory actions.
- `Queue` for market restock and trade-record processing.
- `DoublyLinkedList` for backpack and trade-record traversal.
- `HashTable` for player, item, and listing lookup indexes.
- `BinarySearchTree` for price-ordered market listings.
- `Tree` for the item catalog hierarchy.

These structures are used by the service layer to support the main gameplay workflows. JSON repositories and some presentation-layer grouping still use standard Python containers where they are a practical fit for persistence and CLI rendering.

### Layered Architecture

```text
presentation/  ->  service/  ->  repository/  ->  domain/
CLI menus          business       JSON storage      models,
                   rules                            enums,
                                                    constants
```

### Consistent Service Responses

Service methods return a shared `Response` model with success/failure status, messages, optional data, and optional player state. Many service operations use the `@handle_exceptions` decorator to convert domain exceptions into failure responses.

### Centralized Game Configuration

Core rules such as initial gold, name length, price validation, rarity multipliers, and market restock ranges are defined in `src/domain/constants.py`.

## Project Structure

```text
game_inventory_trading_system/
|-- main.py
|-- pyproject.toml
|-- requirements.txt
|-- README.md
|-- ARCHITECTURE.md
|-- uml.md
|-- docs/
|   |-- *.docx
|-- src/
|   |-- data/
|   |   |-- buy_records.json
|   |   |-- item_config.json
|   |   |-- items.json
|   |   |-- listings.json
|   |   |-- players.json
|   |   |-- save.json
|   |   |-- sell_records.json
|   |-- data_structures/
|   |   |-- bst.py
|   |   |-- hash_table.py
|   |   |-- linked_list.py
|   |   |-- queue.py
|   |   |-- stack.py
|   |   |-- tree.py
|   |-- domain/
|   |   |-- constants.py
|   |   |-- enums.py
|   |   |-- exceptions.py
|   |   |-- messages.py
|   |   |-- models.py
|   |-- presentation/
|   |   |-- inventory_menu.py
|   |   |-- main_menu.py
|   |   |-- market_menu.py
|   |   |-- profile_menu.py
|   |   |-- utils.py
|   |-- repository/
|   |   |-- data_initializer.py
|   |   |-- repositories.py
|   |-- service/
|       |-- inventory_service.py
|       |-- market_service.py
|       |-- player_service.py
|       |-- system_service.py
|       |-- trade_service.py
|-- tests/
|   |-- integration/
|   |-- unit/
|       |-- data_structures/
|       |-- domain/
|       |-- repository/
|       |-- service/
```

## Requirements

- Python 3.10 or later.
- No runtime third-party dependencies.
- Development/test dependencies are optional: `pytest`, `pytest-xdist`, and `pytest-cov`.

## Run the Application

```bash
python main.py
```

On startup, the application initializes required JSON files under `src/data/` if they do not already exist.

## Gameplay Overview

1. Start a new game or continue from `src/data/save.json`.
2. Create a character with initial gold and starter items.
3. Use the backpack menu to view grouped items or sell items directly.
4. Use the market menu to browse, search, buy, list, or delist items.
5. Use the profile menu to review player information, listings, and trade history.
6. Save and exit from the main menu.

## Testing

Install test dependencies:

```bash
pip install pytest pytest-xdist pytest-cov
```

Run all tests:

```bash
python -m pytest
```

Run only data-structure tests:

```bash
python -m pytest tests/unit/data_structures/
```

Run a specific test file:

```bash
python -m pytest tests/unit/data_structures/test_stack.py -v
```

Run tests in parallel:

```bash
python -m pytest -n auto
```

## Test Layout

- `tests/unit/data_structures/` covers custom stack, queue, linked list, hash table, binary search tree, and general tree behavior.
- `tests/unit/domain/` covers enums and domain models.
- `tests/unit/repository/` covers JSON repository behavior.
- `tests/unit/service/` covers player, inventory, market, trade, and item catalog service logic.
- `tests/integration/` covers complete trading flows.

## Data Files

The game stores local state in `src/data/`:

- `item_config.json`: item definitions and base prices.
- `players.json`: player profiles and gold balances.
- `items.json`: player backpack contents.
- `listings.json`: market orders.
- `buy_records.json`: purchase history.
- `sell_records.json`: sale history.
- `save.json`: the currently saved player session.

## Example Service Patterns

Centralized constants:

```python
from src.domain import PlayerConfig, PriceConfig

PlayerConfig.INITIAL_GOLD
PriceConfig.calculate_range(base_price)
```

Unified response handling:

```python
from src.domain import Response, handle_exceptions

@handle_exceptions
def create_player(self, name: str) -> Response:
    ...
```

Centralized messages:

```python
from src.domain import ErrorMessages, SuccessMessages

ErrorMessages.ITEM_NOT_FOUND
SuccessMessages.ITEM_SOLD
```
