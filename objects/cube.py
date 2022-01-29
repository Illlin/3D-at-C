from objects.base import *


class Cube(Base):
    # A 3d Cube

    def __init__(self, pos, size):
        super().__init__(pos)
        self.pos = np.array(pos)
        self.size = np.array(size)

    def distance_to(self, other):
        # Outwards distance.

        d = np.array([abs(x) for x in self.pos - other]) - self.size
        return mag(max([*d, 0]) + min([max(d[0], max(d[1:])), 0]))
