from objects.base import *


class Unison(Base):
    # A 3d Sphere

    def __init__(self, pos, *objects):
        super().__init__(pos)
        self.pos = np.array(pos)
        self.objects = objects

    def distance_to(self, other):
        coord = other - self.pos
        dist = np.inf
        for object in self.objects:
            d = object.distance_to(coord)
            dist = min(dist, d)
        return dist
