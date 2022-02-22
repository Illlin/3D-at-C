from objects.base import *


class Compress(Base):
    # A spacial compression

    def __init__(self, shape, factor):
        super().__init__(shape.pos)
        self.shape = shape
        self.factor = factor
        self.pos = shape.pos

    def distance_to(self, other):
        # Outwards distance.

        d = np.array([abs(x) for x in self.pos - other]) - self.size
        return mag(max([*d, 0]) + min([max(d[0], max(d[1:])), 0]))
