# Imports
import numpy as np
import objects
import camera

sphere = objects.sphere.Sphere([2, 0, 0], 1)

print(sphere.distance_to([0, 0, 0]))

cam = camera.Camera([0, 0, 0], [0, 0])

cam.render(sphere)
