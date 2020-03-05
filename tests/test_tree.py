from cope.tree import TreeNode


def test_constructor():
    data = 4
    children = []
    tree = TreeNode(data, children)
    assert tree.data == 4

def test_reduce():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    tree = TreeNode(3, [child1, child2])
    reduced = tree.reduce(lambda n, r: n.data + r, 0)
    assert reduced == 6

def test_walk():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    tree = TreeNode(3, [child1, child2])
    tree.walk(lambda n: n.data*2)
    assert tree.reduce(lambda n, r: n.data + r, 0) == 12

def test_depth():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    parent = TreeNode(3, [child1, child2])
    root = TreeNode(None, [parent])
    assert root.depth() == 2

def test_get():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    parent = TreeNode(3, [child1, child2])
    root = TreeNode(None, [parent])
    assert root.get(0).data == None
    assert root.get(1).data == 3
    assert root.get(2).data == 1
    assert root.get(3).data == 2

def test_set():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    parent = TreeNode(3, [child1, child2])
    root = TreeNode(None, [parent])
    change = TreeNode("test", [TreeNode("end", [])])
    root.set(1, change)
    assert root.get(1).data == "test"
    assert root.get(2).data == "end"

def test_str():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    parent = TreeNode(3, [child1, child2])
    root = TreeNode(None, [parent])
    assert str(root)

def test_len():
    child1 = TreeNode(1, [])
    child2 = TreeNode(2, [])
    parent = TreeNode(3, [child1, child2])
    root = TreeNode(None, [parent])
    assert len(root) == 4
