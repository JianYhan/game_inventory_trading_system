import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import shutil
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

PASS = "PASS"
FAIL = "FAIL"
results = []

def check(name, condition):
    status = PASS if condition else FAIL
    results.append((name, status))
    print(f"  [{status}] {name}")

def setup():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    for f in ["players.json", "items.json", "listings.json", "trades.json"]:
        p = os.path.join(data_dir, f)
        if os.path.exists(p):
            os.remove(p)
    DataInitializer().initialize()
    player_repo = PlayerRepository()
    item_repo = ItemRepository()
    listing_repo = ListingRepository()
    trade_repo = TradeRepository()
    player_svc = PlayerService(player_repo)
    inventory_svc = InventoryService(player_repo, item_repo)
    market_svc = MarketService(player_repo, item_repo, listing_repo, trade_repo)
    trade_svc = TradeService(trade_repo)
    system_svc = SystemService(player_repo, listing_repo, trade_repo)
    return player_svc, inventory_svc, market_svc, trade_svc, system_svc, item_repo


print("=" * 55)
print("  Game Inventory Trading System - Test Suite")
print("=" * 55)

player_svc, inventory_svc, market_svc, trade_svc, system_svc, item_repo = setup()
arthur = player_svc.get_by_name("Arthur")
luna = player_svc.get_by_name("Luna")
zephyr = player_svc.get_by_name("Zephyr")

# ----------------------------------------------------------------
print("\n[1] Player Service")
check("list_players returns 3", len(player_svc.list_players()) == 3)
check("get_by_name Arthur", arthur is not None)
check("get_player by id", player_svc.get_player("p001") is not None)
check("get_by_name nonexistent returns None", player_svc.get_by_name("Ghost") is None)
new_p = player_svc.create_player("Tester", 500.0)
check("create_player", new_p is not None and new_p.name == "Tester")
check("create_player gold", new_p.gold == 500.0)
player_svc.delete_player(new_p.player_id)
check("delete_player", player_svc.get_player(new_p.player_id) is None)

# ----------------------------------------------------------------
print("\n[2] Inventory - Basic")
inv = inventory_svc.get_inventory(arthur)
check("get_inventory not empty", len(inv) > 0)
check("add_item success", inventory_svc.add_item(arthur, "wpn_002", 1))
check("item in backpack after add", arthur.backpack.has_item("wpn_002", 1))
check("remove_item success", inventory_svc.remove_item(arthur, "wpn_002", 1))
check("item gone after remove", not arthur.backpack.has_item("wpn_002", 1))

# ----------------------------------------------------------------
print("\n[3] Inventory - Edge Cases")
check("remove nonexistent item", not inventory_svc.remove_item(arthur, "fake_id", 1))
check("remove more than owned", not inventory_svc.remove_item(arthur, "pot_001", 999))
check("add nonexistent item_id", not inventory_svc.add_item(arthur, "fake_id", 1))

# backpack full with different items
p_full = player_svc.create_player("FullBag", 1000.0)
p_full.backpack.capacity = 2
inventory_svc.add_item(p_full, "wpn_001", 1)
inventory_svc.add_item(p_full, "wpn_002", 1)
check("backpack full blocks new slot", not inventory_svc.add_item(p_full, "wpn_003", 1))
check("backpack full allows stacking", inventory_svc.add_item(p_full, "wpn_001", 1))

# ----------------------------------------------------------------
print("\n[4] Inventory - Undo")
inventory_svc.add_item(arthur, "mat_001", 5)
msg = inventory_svc.undo_last(arthur)
check("undo add", msg is not None)
check("item removed after undo", arthur.backpack.get_quantity("mat_001") == 20)
msg2 = inventory_svc.undo_last(arthur)
check("second undo works", msg2 is not None)

# ----------------------------------------------------------------
print("\n[5] Inventory - Sort & Search")
sorted_inv = inventory_svc.sort_inventory_by_price(arthur)
check("sort by price descending", sorted_inv[0][0].base_price >= sorted_inv[-1][0].base_price)
results_sword = inventory_svc.search_item_in_inventory(arthur, "sword")
check("search case insensitive lower", len(results_sword) > 0)
results_upper = inventory_svc.search_item_in_inventory(arthur, "SWORD")
check("search case insensitive upper", len(results_sword) == len(results_upper))
check("search no match returns empty", len(inventory_svc.search_item_in_inventory(arthur, "zzznomatch")) == 0)

# ----------------------------------------------------------------
print("\n[6] Market - List Item")
listing = market_svc.list_item(luna, "pot_002", 1, 90.0)
check("list_item success", listing is not None)
check("item removed from backpack after listing", luna.backpack.get_quantity("pot_002") == 2)
check("listing is active", listing.status == "active")
check("listing in active listings", listing in market_svc.get_active_listings())

check("list item not in backpack fails", market_svc.list_item(luna, "wpn_002", 1, 100.0) is None)
check("list more than owned fails", market_svc.list_item(luna, "pot_002", 999, 10.0) is None)

# ----------------------------------------------------------------
print("\n[7] Market - Buy Item")
before_gold = arthur.gold
trade = market_svc.buy_item(arthur, listing.listing_id)
check("buy_item success", trade is not None)
check("gold deducted from buyer", arthur.gold == before_gold - listing.total_price())
check("item added to buyer backpack", arthur.backpack.has_item("pot_002", 1))
check("listing status sold", market_svc._listing_cache.get(listing.listing_id) is None)

check("buy already sold listing fails", market_svc.buy_item(arthur, listing.listing_id) is None)

# ----------------------------------------------------------------
print("\n[8] Market - Buy Edge Cases")
listing2 = market_svc.list_item(luna, "pot_002", 1, 50.0)
check("buy own listing fails", market_svc.buy_item(luna, listing2.listing_id) is None)

poor = player_svc.create_player("Poor", 1.0)
check("buy with insufficient gold fails", market_svc.buy_item(poor, listing2.listing_id) is None)

check("buy nonexistent listing fails", market_svc.buy_item(arthur, "fake_listing") is None)

# ----------------------------------------------------------------
print("\n[9] Market - Cancel Listing")
listing3 = market_svc.list_item(luna, "pot_002", 1, 80.0)
qty_before = luna.backpack.get_quantity("pot_002")
result = market_svc.cancel_listing(luna, listing3.listing_id)
check("cancel listing success", result)
check("item returned to backpack", luna.backpack.get_quantity("pot_002") == qty_before + 1)
check("cancel nonexistent listing fails", not market_svc.cancel_listing(luna, "fake_id"))
listing4 = market_svc.list_item(luna, "pot_002", 1, 70.0)
check("cancel other player listing fails", not market_svc.cancel_listing(arthur, listing4.listing_id))

# ----------------------------------------------------------------
print("\n[10] Market - Search")
market_svc.list_item(zephyr, "mat_001", 10, 6.0)
market_svc.list_item(zephyr, "mat_001", 5, 8.0)
by_item = market_svc.search_by_item("mat_001")
check("search_by_item finds listings", len(by_item) >= 2)
by_price = market_svc.search_by_price_range(5.0, 10.0)
check("search_by_price_range finds results", len(by_price) >= 2)
check("search_by_price_range empty range", len(market_svc.search_by_price_range(99999, 99999)) == 0)

# ----------------------------------------------------------------
print("\n[11] Market - Buy Order Queue")
market_svc.enqueue_buy_order(arthur.player_id, "mat_001", 7.0)
trades = market_svc.process_order_queue()
check("buy order queue processed", len(trades) >= 1)
check("queue empty after process", market_svc._order_queue.is_empty())

market_svc.enqueue_buy_order(arthur.player_id, "mat_001", 0.01)
trades = market_svc.process_order_queue()
check("buy order with too low price yields no trade", len(trades) == 0)

# ----------------------------------------------------------------
print("\n[12] Trade Service")
all_trades = trade_svc.get_all_trades()
check("get_all_trades not empty", len(all_trades) > 0)
arthur_trades = trade_svc.get_trades_for_player(arthur.player_id)
check("get_trades_for_player", len(arthur_trades) > 0)
purchases = trade_svc.get_purchases(arthur.player_id)
check("get_purchases", len(purchases) > 0)
volume = trade_svc.get_trade_volume(arthur.player_id)
check("get_trade_volume > 0", volume > 0)
empty_trades = trade_svc.get_trades_for_player("nonexistent_player")
check("trades for nonexistent player empty", len(empty_trades) == 0)

# ----------------------------------------------------------------
print("\n[13] System Service")
stats = system_svc.get_system_stats()
check("stats has total_players", stats["total_players"] > 0)
check("stats has active_listings", "active_listings" in stats)
check("stats has total_trades", stats["total_trades"] > 0)
check("stats has total_trade_volume", stats["total_trade_volume"] > 0)
tree_str = system_svc.print_category_tree()
check("category tree contains weapon", "weapon" in tree_str)
check("category tree contains armor", "armor" in tree_str)

# ----------------------------------------------------------------
print("\n[14] Data Structures")
from data_structures.doubly_linked_list import DoublyLinkedList
dll = DoublyLinkedList()
dll.append(1); dll.append(2); dll.append(3)
check("DLL size", dll.size() == 3)
node = dll.find(lambda x: x == 2)
dll.remove(node)
check("DLL remove", dll.size() == 2)
check("DLL iter", list(dll.iter()) == [1, 3])

from data_structures.stack import Stack
s = Stack()
s.push(10); s.push(20)
check("Stack peek", s.peek() == 20)
check("Stack pop", s.pop() == 20)
check("Stack size", s.size() == 1)
try:
    s.pop()  # empties stack
    s.pop()  # should raise
    check("Stack empty pop raises", False)
except IndexError:
    check("Stack empty pop raises", True)

from data_structures.queue import Queue
q = Queue()
q.enqueue("a"); q.enqueue("b")
check("Queue dequeue FIFO", q.dequeue() == "a")
check("Queue size", q.size() == 1)

from data_structures.bst import BinarySearchTree
bst = BinarySearchTree()
for v in [5, 3, 7, 1, 4]:
    bst.insert(v, f"val{v}")
check("BST inorder sorted", [k for k, _ in bst.inorder()] == [1, 3, 4, 5, 7])
check("BST search", bst.search(3) == "val3")
check("BST range_query", list(bst.range_query(3, 5)) == [(3,"val3"),(4,"val4"),(5,"val5")])
bst.delete(3)
check("BST delete", bst.search(3) is None)

from data_structures.hash_table import HashTable
ht = HashTable()
ht.put("k1", "v1"); ht.put("k2", "v2")
check("HashTable get", ht.get("k1") == "v1")
check("HashTable contains", ht.contains("k2"))
ht.delete("k1")
check("HashTable delete", not ht.contains("k1"))
check("HashTable size", ht.size() == 1)

from data_structures.tree import Tree
t = Tree("root")
t.insert("root", "child1")
t.insert("root", "child2")
t.insert("child1", "grandchild")
check("Tree find", t.find("child1") is not None)
check("Tree find deep", t.find("grandchild") is not None)
check("Tree find missing", t.find("missing") is None)
nodes = list(t.traverse())
check("Tree traverse all nodes", len(nodes) == 4)

# ----------------------------------------------------------------
print("\n" + "=" * 55)
passed = sum(1 for _, s in results if s == PASS)
failed = sum(1 for _, s in results if s == FAIL)
print(f"  Results: {passed} passed, {failed} failed out of {len(results)} tests")
if failed > 0:
    print("\n  Failed tests:")
    for name, status in results:
        if status == FAIL:
            print(f"    - {name}")
print("=" * 55)
