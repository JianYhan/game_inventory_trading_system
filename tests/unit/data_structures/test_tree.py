from src.data_structures.tree import Tree, TreeNode


def test_tree_node_creation():
    node = TreeNode("root", {"kind": "catalog"})

    assert node.value == "root"
    assert node.data == {"kind": "catalog"}
    assert node.parent is None
    assert node.children == []


def test_insert_and_find_nested_nodes():
    tree = Tree("root")

    child = tree.insert("root", "child")
    grandchild = tree.insert("child", "grandchild")

    assert tree.find("child") is child
    assert tree.find("grandchild") is grandchild
    assert tree.find("missing") is None
    assert grandchild.parent is child


def test_traverse_uses_preorder():
    tree = Tree("root")
    tree.insert("root", "child1")
    tree.insert("root", "child2")
    tree.insert("child1", "grandchild")

    assert [node.value for node in tree.traverse()] == [
        "root",
        "child1",
        "grandchild",
        "child2",
    ]


def test_to_lines_indents_tree_levels():
    tree = Tree("root")
    tree.insert("root", "child")
    tree.insert("child", "grandchild")

    assert tree.to_lines() == [
        "- root",
        "  - child",
        "    - grandchild",
    ]


def test_insert_requires_existing_parent():
    tree = Tree("root")

    try:
        tree.insert("missing", "child")
    except ValueError as exc:
        assert "Parent node" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
