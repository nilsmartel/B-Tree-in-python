from math import floor

def split_list(list):
    s = len(list)
    # index of mid element or left or mid element
    index = floor(s/2 - 0.5)

    first = list[:index]
    mid = list[index]
    second = list[index+1:]
    return [first, mid, second]

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


class BTreeNode:
    def __init__(self, keys = [], parent = None):
        self.parent = None
        self.keys = keys
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent == None

    def remove_child_unsafe(self, child):
        i=0
        for c in self.children:
            if c == child:
                self.children.pop(i)
                return
            i += 1

    def append_child_unsafe(self, child):
        child.parent = self
        self.children.append(child)
        self.children.sort()

    def split(self, tree):
        # first check if this node it the uppermost one. Create a new parent if needed
        if self.is_root():
            tree.root = BTreeNode()
            self.parent = tree.root
        else:
            self.parent.remove_child_unsafe(self)

        # now the parents are all set up!
        parent = self.parent


        # we have removed this node from it's parent.
        # Now we split up this node into 2 separate ones,
        # that we reinclude in the parent
        [lower, key, upper] = split_list(self.keys)
        parent.keys.append(key)
        parent.keys.sort()

        # lower and upper nodes
        l = BTreeNode(keys=lower, parent=parent)
        u = BTreeNode(keys=upper, parent=parent)

        # if this node has any children, we want to distribute them among these two new nodes
        if not self.is_leaf():
            # index where to split
            index = floor(len(self.children))
            for child in self.children[0:index]:
                l.append_child_unsafe(child)
            for child in self.children[index:]:
                u.append_child_unsafe(child)

            i = 0

        parent.children.append(l)
        parent.children.append(u)
        parent.children.sort()

        # now the parent has the right amount of children in ratio to it's keys

        # at last we need to check, if the parent has too many keys left and recurively fix that.
        if len(parent.keys) > 3:
            parent.split()



    def __lt__(self, other):
        self.keys[0] < other.keys[0]


    def add_key(self, tree, key):
        if key in self.keys:
            return

        if self.is_leaf():
            self.keys.append(key)
            self.keys.sort()
            if len(self.keys) > 3:
                self.split(tree)

            return

        for [elem, child] in zip(self.keys, self.children):
            if elem > key:
                child.add_key(tree, key)
                return

        self.children[-1].add_key(tree, key)


    def __eq__(self, other):
        return self.keys == other.keys


class BTree:
    def __init__(self):
        self.root = None

    def string(self):
        if not self.root:
            return "[]"

        s = ""
        q = [self.root, None]
        while len(q) != 0:
            node = q.pop(0)
            if not node:
                s += "\n"
                continue

            for child in node.children:
                q.append(child)

            s += str(node.keys) + " "

        return s

    def add_key(self, key):
        if not self.root:
            self.root = BTreeNode([key])
            return

        self.root.add_key(self, key)

def test_btree():
    t = BTree()
    t.add_key('b')
    for c in "ergha":
        t.add_key(c)
    t.add_key('a')
    for c in "in":
        t.add_key(c)
    print(t.string())

test_btree()
