# Architecture Overview

This document describes the architecture of the Game Inventory & Trading System as implemented in the current codebase. The system is a command-line Python application that supports player creation, backpack management, item selling, marketplace trading, trade history, save/load behavior, and an item catalog tree.

## Design Goals

- Keep business logic separate from command-line input/output.
- Store persistent game state in simple JSON files.
- Use custom data structures in the service layer for lookup, ordering, traversal, and queue/stack workflows.
- Return consistent service results through the shared `Response` model.
- Centralize validation rules, messages, enums, and game configuration.
- Provide a testable layered design with unit and integration test coverage.

## High-Level Architecture

```text
User
 |
 v
presentation/
CLI menus, prompts, display formatting
 |
 v
service/
Business rules, validation, workflows, custom structure indexes
 |
 v
repository/
JSON persistence and object serialization/deserialization
 |
 v
domain/
Dataclasses, enums, constants, messages, exceptions
```

The `data_structures/` package is used mainly by the service layer. It is kept separate from the domain models so that the structures can be tested independently and reused across workflows.

## Module Responsibilities

| Layer | Main Files | Responsibility |
|---|---|---|
| Entry point | `main.py` | Initializes JSON data files, creates services, and starts the CLI flow. |
| Presentation | `src/presentation/*.py` | Shows menus, collects user input, formats output, and calls services. |
| Service | `src/service/*.py` | Enforces game rules, coordinates repositories, manages custom data structures, and returns `Response` objects. |
| Repository | `src/repository/*.py` | Reads/writes JSON files and converts stored dictionaries into domain objects. |
| Domain | `src/domain/*.py` | Defines dataclasses, enums, constants, messages, and domain exceptions. |
| Data structures | `src/data_structures/*.py` | Implements stack, queue, linked list, hash table, binary search tree, and general tree. |
| Data | `src/data/*.json` | Stores players, items, listings, trade records, item configuration, and save data. |
| Tests | `tests/` | Covers unit behavior for layers and integration behavior for trading flows. |

## Dependency Direction

```text
main.py
  -> presentation
      -> service
          -> repository
              -> domain
          -> data_structures
```

Presentation code does not access JSON files directly. Repository code does not contain business rules. Domain models do not depend on the service or presentation layer.

## Runtime Flow

1. `main.py` calls `initialize()` to create required JSON files if missing.
2. Service objects are created: `PlayerService`, `InventoryService`, `MarketService`, `TradeService`, and `SystemService`.
3. `show_entry_menu()` loads an existing save or creates a new player.
4. `show_main_menu()` routes the user to backpack, market, profile, or item catalog views.
5. Services execute business operations and return `Response` objects.
6. Repositories persist state changes to JSON files.

## Domain Model

The current domain layer uses dataclasses rather than an inheritance hierarchy for item types.

| Model | Purpose |
|---|---|
| `Player` | Stores player id, name, gold, and creation time. |
| `ItemConfig` | Stores static item configuration such as id, name, type, rarity, and base price. |
| `BackpackItem` | Stores an item owned by a player, including quantity and calculated sell price. |
| `MarketOrder` | Represents a marketplace listing with seller, item, price, quantity, status, and listing time. |
| `BuyRecord` | Records a completed purchase from the buyer perspective. |
| `SellRecord` | Records a completed sale from the seller perspective. |
| `GameSave` | Represents saved session data. |
| `Response` | Standard service return object containing status, message, optional data, and optional player. |

Important enums:

- `Rarity`: `COMMON`, `RARE`, `EPIC`, `LEGENDARY`, each with a label and price multiplier.
- `ItemType`: `WEAPON`, `POTION`, `ARMOR`, `MATERIAL`.
- `OrderStatus`: `ON_SALE`, `PARTIAL`, `SOLD_OUT`, `DELISTED`.
- `ResultStatus`: `SUCCESS`, `FAILURE`.

## Custom Data Structures

| Structure | Implementation | Main Usage | Typical Complexity |
|---|---|---|---|
| `Stack` | Linked-node stack | Recent inventory action messages | `push`, `pop`, `peek`: O(1) |
| `Queue` | Linked-node queue with front/rear pointers | Market restock and trade-record processing | `enqueue`, `dequeue`: O(1) |
| `DoublyLinkedList` | Linked nodes with previous/next pointers | Backpack traversal and trade-record lists | append O(1), traversal O(n), remove O(n) |
| `HashTable` | Separate chaining hash table | Player, item, and listing lookup indexes | average O(1), worst O(n) |
| `BinarySearchTree` | Node-based BST | Price-sorted market listings | average O(log n), worst O(n) |
| `Tree` | General tree with parent/children links | Item catalog grouped by type and rarity | traversal O(n), find O(n) |

The project also uses standard Python containers where they are appropriate for JSON serialization, configuration loading, and CLI grouping. The custom structures are used to demonstrate and support core data-management workflows.

## Service Layer Design

### PlayerService

Responsibilities:

- Validate player names.
- Create new players with initial gold.
- Give starter backpack items.
- Cache players with `HashTable`.
- Update player gold.

Key repositories:

- `PlayerRepository`
- `ItemRepository`
- `ConfigRepository`

### InventoryService

Responsibilities:

- Load a player's backpack.
- Group backpack items by type.
- Add items and merge quantities.
- Deduct items when listing or buying.
- Sell items directly for gold.
- Validate quantity and price range.

Key structures:

- `DoublyLinkedList` for backpack traversal.
- `HashTable` for item lookup by item id.
- `Stack` for recent action messages.

### MarketService

Responsibilities:

- List items for sale.
- Browse active listings sorted by price.
- Search listings by item name.
- Buy from active listings.
- Delist active own listings.
- Generate system restock orders.

Key structures:

- `HashTable` for order lookup by order id.
- `BinarySearchTree` for price-ordered active listings.
- `Queue` for restock processing.

### TradeService

Responsibilities:

- Load purchase records.
- Load sale records.
- Load a player's market listings.
- Convert trade records through a FIFO queue into linked-list-backed lists.

Key structures:

- `Queue` for record processing.
- `DoublyLinkedList` for record traversal.

### SystemService

Responsibilities:

- Save and load the current player session.
- Build and print the item catalog.
- Group catalog entries by item type and rarity.

Key structure:

- `Tree` for the catalog hierarchy.

## Key Workflows

### Create Player

```text
Presentation
  -> PlayerService.create_player(name)
      -> validate name
      -> check PlayerRepository.name_exists(name)
      -> create Player with initial gold
      -> PlayerRepository.save(player)
      -> give starter BackpackItem entries
      -> ItemRepository.save_item(...)
      -> cache player in HashTable
      -> Response.ok(...)
```

### Sell Item Directly

```text
Presentation
  -> InventoryService.sell_item(player_id, item_id, quantity, price)
      -> load backpack into DoublyLinkedList and HashTable
      -> find target item by item_id
      -> validate quantity
      -> validate price with PriceConfig
      -> add gold to player
      -> reduce or remove backpack item
      -> persist player and item changes
      -> push action message to Stack
      -> Response.ok(...)
```

### List Item on Market

```text
Presentation
  -> MarketService.list_item(player_id, item_id, quantity, unit_price)
      -> find item in backpack
      -> validate quantity and price
      -> InventoryService.deduct_item(...)
      -> create MarketOrder
      -> ListingRepository.save(order)
      -> index order in HashTable
      -> insert order into BinarySearchTree by price/list time/order id
      -> Response.ok(...)
```

### Buy Market Item

```text
Presentation
  -> MarketService.buy_item(buyer_id, order_id, quantity)
      -> load active listings into HashTable and BinarySearchTree
      -> find order by order_id
      -> validate order status, quantity, and buyer != seller
      -> deduct buyer gold
      -> add seller gold unless seller is SYSTEM
      -> add item to buyer backpack
      -> update order status and remaining quantity
      -> save buy and sell records
      -> Response.ok(...)
```

### Item Catalog Tree

```text
SystemService.get_category_tree()
  -> root: "Item Catalog"
      -> item type node, e.g. "weapon"
          -> rarity node, e.g. "weapon / Rare"
              -> item node, e.g. "Iron Sword (1002)"
```

This tree is displayed through the main menu's item catalog option.

## Persistence Design

All persistent data is stored in `src/data/` as JSON.

| File | Content | Repository/Service |
|---|---|---|
| `item_config.json` | Static item definitions and base prices | `ConfigRepository`, `data_initializer.py` |
| `players.json` | Player profiles and gold balances | `PlayerRepository` |
| `items.json` | Player backpack contents | `ItemRepository` |
| `listings.json` | Market orders | `ListingRepository` |
| `buy_records.json` | Purchase history | `TradeRepository` |
| `sell_records.json` | Sale history | `TradeRepository` |
| `save.json` | Current saved player session | `SystemService` |

Repositories isolate file format details from business logic. Services work with domain objects rather than raw JSON dictionaries.

## Validation and Error Handling

Validation rules are centralized in service methods and configuration classes:

- Player names must be non-empty and within `PlayerConfig.MIN_NAME_LENGTH` and `PlayerConfig.MAX_NAME_LENGTH`.
- Item quantities must be positive and cannot exceed available inventory/listing quantity.
- Sell/list prices must be within `PriceConfig.MIN_PRICE_FACTOR` and `PriceConfig.MAX_PRICE_FACTOR` of the item's sell price.
- Buyers cannot buy their own market listings.
- Gold cannot be deducted if the player has insufficient funds.

Domain exceptions include:

- `ValidationException`
- `InsufficientGoldException`
- `ItemNotFoundException`
- `PlayerNotFoundException`

The `@handle_exceptions` decorator converts service-layer exceptions into `Response.fail(...)` and logs errors.

## Testing Strategy

The test suite is organized by layer:

```text
tests/
|-- unit/
|   |-- data_structures/
|   |-- domain/
|   |-- repository/
|   |-- service/
|-- integration/
```

Testing goals:

- Verify each custom data structure independently.
- Verify domain model properties and enum behavior.
- Verify repository serialization/deserialization and persistence behavior.
- Verify service-level business rules, validation, and failure responses.
- Verify full trading flows across multiple layers.

Suggested commands:

```bash
python -m pytest
python -m pytest tests/unit/data_structures/
python -m pytest tests/unit/service/
python -m pytest tests/integration/
```

## Design Trade-Offs

- JSON storage keeps the project simple and easy to inspect, but it is not optimized for concurrent writes or large datasets.
- Services rebuild some in-memory indexes, such as market listing hash tables and price BSTs, to keep persisted JSON as the source of truth.
- The `BinarySearchTree` gives sorted listing output, but it can degrade to O(n) if keys are inserted in an already sorted pattern.
- The general `Tree` is simple and readable for catalog display, but `find` is O(n) because it traverses the tree.
- The project uses custom structures for learning and demonstration, while still using Python containers for JSON-compatible persistence and presentation formatting.
