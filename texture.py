import numpy as np
from PIL import Image


class Texture:
    def __init__(self, filename, size):
        self.filename = filename
        self.size = size

        img = Image.open(filename)
        img = img.convert("RGB")
        self.data = np.array(img, dtype="uint8")

    def get_point(self, pos):
        pos *= self.size
        pos %= self.size
        return self.data[int((pos[0] + pos[1])) % self.size][int(pos[2])]

    def get_point2d(self, pos):
        pos *= self.size
        pos %= self.size
        return self.data[int(pos[1])][int(pos[0])]

