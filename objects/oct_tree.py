from objects.base import *
import random

sqrt3 = np.sqrt(3)
sub_oct_pos = [
    0.5 * np.array([-1, -1, +1]),
    0.5 * np.array([-1, +1, +1]),
    0.5 * np.array([+1, -1, +1]),
    0.5 * np.array([+1, +1, +1]),
    0.5 * np.array([-1, -1, -1]),
    0.5 * np.array([-1, +1, -1]),
    0.5 * np.array([+1, -1, -1]),
    0.5 * np.array([+1, +1, -1]),
]
sub_oct_pos = sub_oct_pos[::-1]

class Tree:
    # An Oct Tree

    def __init__(self, depth=3):
        self.tree = self.fill_random(depth=depth)

    def fill_random(self, dencity=0.8, depth=0):
        tree = [
            0, 0,
            0, 0,

            0, 0,
            0, 0
        ]

        for i, c in enumerate(tree):
            if random.random() < dencity:
                if depth > 0:
                    tree[i] = self.fill_random(dencity=dencity, depth=depth-1)
                else:
                    tree[i] = 1
            else:
                tree[i] = 0

        return tree


def distance_to_tree(tree, center_pos, size, other, min_dist_out, fast=False):
    size_arr = 0.5 * np.array([size, size, size])

    min_dist = np.inf
    close = None
    min_pos = center_pos

    for i in range(8):
        if tree[i] != 0:
            pos = center_pos + size * sub_oct_pos[i]

            #dist = mag(pos - other)

            if tree[i] == 1 or fast:
                d = np.array([abs(x) for x in pos - other]) - size_arr
                dist = mag(max([*d, 0]) + min([max(d[0], max(d[1:])), 0]))

            else:
                dist = distance_to_tree(tree[i], pos, 0.5*size, other, min(min_dist, min_dist_out), fast=True)

            if dist < min_dist:
                min_dist = dist
                close = i
                min_pos = pos

    if close is None:
        return min_dist_out

    if tree[close] == 1:
        return min_dist

    return distance_to_tree(tree[close], min_pos, 0.5*size, other, min(min_dist, min_dist_out))


class OctTree(Base):
    # A 3d OctTree Approximation

    def __init__(self, pos, size: int, tree):
        super().__init__(pos)
        self.pos = np.array(pos)
        self.size = size
        self.tree = tree#.tree

    def distance_to(self, other):
        return distance_to_tree(self.tree, self.pos, self.size, other, np.inf)

