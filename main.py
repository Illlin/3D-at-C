# Imports
import numpy as np
import objects
import camera
import time
import scene
from multiprocessing import Pool
import os

if os.getlogin() == "solst":
    print("Wrong OS dummy")
    start = time.time()
    world = scene.Scene([0.0, 0.0, 0.0], "Ship2.json")

    world.advance_frame(0)

    setting = camera.cam_360
    #setting = camera.base_settings
    x = 1440

    setting["res"] = [x, int(x/2)]

    cam = camera.Camera([0.0, 0.0, 0.0], [0.0, 0.0], settings=setting)
    camera.save_frame(cam.render(world), "render/graph.png")
    print("took", int(time.time()-start))
    exit()

ffmpeg = 'ffmpeg -r 15 -i "render/frame%04d.png" -c:v libx264 -vf "fps=24,format=yuv420p" render/out.mp4 -y'

os.system("rm render/frame*.png")

a = time.time()

def render(frame):
    #print("Thread", frame)
    filename = "render/frame{frame:04d}.png".format(frame=frame)
    world = scene.Scene([0, 0, 0], "TestScene.json")

    world.advance_frame(frame)

    #setting = camera.cam_360
    setting = camera.base_settings
    x = 256

    setting["res"] = [x, int(x/1)]


    cam = camera.Camera([0, 0, 0], [0, 0], settings=setting)
    camera.save_frame(cam.render(world), filename)

    return filename


if __name__ == "__main__":
    with Pool(50) as p:
        print(p.map(render, range(0, 24)))

os.system(ffmpeg)

print("\n\n---------------\nIt took", int(time.time()-a), "Seconds to render")


