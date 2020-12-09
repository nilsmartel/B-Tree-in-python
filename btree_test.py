from btree import split_list, BTree

def test(a, b):
    if a != b:
        print(f"[failure] {a} != {b}")
    else:
        print("[success]")

def test_split_list():
    print("test: test_split_list")
    test([[1], 2, [3]], split_list([1, 2, 3]))
    test([[1], 2, [3, 4]], split_list([1, 2, 3, 4]))
    test([[1,2], 3, [4, 5]], split_list([1, 2, 3, 4, 5]))

test_split_list()

def test_btree():
    print("test_btree")
    t = BTree()
    for c in "berghain":
        t.add_key(c)
        print(f"\n{c}")
        print(t.string())

test_btree()
