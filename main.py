# Imports
import numpy as np
import objects
import camera
import time
import scene
a = time.time()

print(time.time()-a)

#sphere = objects.oct_tree.OctTree([2, 2, 0], 1, tree)
sphere = objects.sphere.Sphere([2, 2, 0], np.sqrt(3))
sphere = objects.cube.Cube([2, 2, 0], np.array([1, 1, 1]))
sphere = scene.Scene([0, 0, 0], "TestScene.json")

print(sphere.pos)
setting = camera.cam_360
setting = camera.base_settings
x = 1024
setting["res"] = [x, 100]


camL = camera.Camera([-0.05, 0.05, 0], [0.73, 0], settings=setting)
camR = camera.Camera([0.05, -0.05, 0], [0.73, 0], settings=setting)
camera.save_frame(camL.render(sphere), "data3.png")
#camera.save_frame(camR.render(sphere), "outputR.png")

"""
sphere = objects.cube.Cube([2, 2, 0], [1, 1, 1])

print(sphere.distance_to([0, 0, 0]))

cam = camera.Camera([0, 0, 0], [0.73, 0])

cam.settings["fov"] = 2*np.pi
camera.save_frame(cam.render(sphere),"output.png")
"""
