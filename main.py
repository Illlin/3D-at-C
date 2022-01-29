# Imports
import numpy as np
import objects
import camera

sphere = objects.cube.Cube([2.6, 0, 0], [1, 1, 1])

print(sphere.distance_to([0, 0, 0]))

cam = camera.Camera([0, 0, 0], [0, 0])

cam.settings["fov"] = np.pi
cam.render(sphere)
