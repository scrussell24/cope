from copy import deepcopy


class TreeNode:

    def __init__(self, data, children):
        self.data = data
        self.children = children

    def reduce(self, fn, initial):
        reduced = initial
        for child in self.children:
            reduced = child.reduce(fn, reduced)
        return fn(self, reduced)

    def walk(self, fn):
        self.data = fn(self)
        for child in self.children:
            child.walk(fn)

    def depth(self, depth=0):
        gd = depth  # greatest depth
        for child in self.children:
            cd = child.depth(depth=depth+1)
            gd = cd if cd > gd else gd
        return gd

    def get(self, index):
        if index == 0:
            return self
        for child in self.children:
            size = len(child)
            if index <= size:
                return child.get(index-1)
            index -= size

    def set(self, index, node):
        new_node = self.get(index)
        new_node.data, new_node.children = node.data, node.children
        return self

    def __str__(self, level=0):
        indent = '  |' * level
        string = f'{indent} > {self.data}\n'
        for child in self.children:
            string += child.__str__(level=level+1)
        return string

    def __len__(self):
        return self.reduce(lambda x, y: y + 1, 0)
