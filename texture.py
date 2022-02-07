import numpy as np
from PIL import Image

filename = "brick.png"
size = 512

img = Image.open(filename)
img = img.convert("HSV")
data = np.array(img, dtype="uint8")


def get_point(vect):
    vect *= size
    vect %= size
    return data[int((vect[0]+vect[1]))%size][int(vect[2])]

