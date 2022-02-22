import numpy as np
from PIL import Image

filename = "square_floor.png"
size = 1024

img = Image.open(filename)
img = img.convert("RGB")
data = np.array(img, dtype="uint8")


def get_point(vect):
    vect *= size
    vect %= size
    return data[int((vect[1]+vect[2]))%size][int(vect[0])]

