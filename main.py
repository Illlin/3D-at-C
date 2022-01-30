# Imports
import numpy as np
import objects
import camera

sphere = objects.cube.Cube([2, 2, 0], [1, 1, 1])

print(sphere.distance_to([0, 0, 0]))

cam = camera.Camera([0, 0, 0], [0.73, 0])

cam.settings["fov"] = 2*np.pi
camera.save_frame(cam.render(sphere),"output.png")
