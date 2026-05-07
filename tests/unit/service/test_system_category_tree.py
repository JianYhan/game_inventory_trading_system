from src.service.system_service import SystemService


def test_system_service_builds_item_category_tree():
    service = SystemService()

    tree = service.get_category_tree()

    assert tree.find("weapon") is not None
    assert tree.find("armor") is not None
    assert tree.find("Wooden Sword (1001)") is not None


def test_print_category_tree_returns_catalog_text():
    service = SystemService()

    tree_text = service.print_category_tree()

    assert "Item Catalog" in tree_text
    assert "weapon" in tree_text
    assert "armor" in tree_text
