import numpy as np

# Useful functions

mag = np.linalg.norm


def spherical_to_cartesian(spherical):
    # Convert Spherical coordinates to Cartesian

    az = spherical[0]
    el = spherical[1]

    x = np.cos(el) * np.cos(az)
    y = np.cos(el) * np.sin(az)
    z = np.sin(el)

    return np.array([x, y, z])

# Base 3d Object


class Base:
    # Basic 3d object. Includes all required 3d object functions

    def __init__(self, pos):
        self.pos = np.array(pos)
        self.vel = np.array(0, 0, 0)

    def distance_to(self, other):
        # Get the minimum distance from a point to the object

        return mag(self.pos - other)




class Scene(Base):
    # A set of objects

    def __init__(self, objects):
        super().__init__([0, 0, 0])
        self.objects = objects

    def distance_to(self, other):
        return min([x.distance_to(other) for x in self.objects])

