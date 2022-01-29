import numpy as np

# Useful functions
mag = np.linalg.norm


class Base:
    # Basic 3d object. Includes all required 3d object functions

    def __init__(self, pos):
        self.pos = np.array(pos)

    def distance_to(self, other):
        # Get the minimum distance from a point to the object

        return mag(self.pos - other)
