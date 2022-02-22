from objects.base import *


class Sphere(Base):
    # A 3d Sphere

    def __init__(self, pos, radius):
        super().__init__(pos)
        self.pos = np.array(pos)
        self.radius = radius

    def distance_to(self, other):
        assert isinstance(self.radius, object)
        dist_to_center = self.pos - other
        return dist_to_center - self.radius*dist_to_center
