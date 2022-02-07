# Imports
import numpy as np
import objects
import camera
import time
a = time.time()

print(time.time()-a)

sphere = objects.oct_tree.OctTree([2, 2, 0], 1, tree)
sphere = objects.sphere.Sphere([2, 2, 0], np.sqrt(3))
cam = camera.Camera([0, 0, 0], [0.73, 0])
camera.save_frame(cam.render(sphere), "output.png")

"""
sphere = objects.cube.Cube([2, 2, 0], [1, 1, 1])

print(sphere.distance_to([0, 0, 0]))

cam = camera.Camera([0, 0, 0], [0.73, 0])

cam.settings["fov"] = 2*np.pi
camera.save_frame(cam.render(sphere),"output.png")
"""
