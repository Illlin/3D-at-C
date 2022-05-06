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
    world = scene.Scene([0.0, 0.0, 0.0], "TestScene.json")

    world.advance_frame(0)

    setting = camera.cam_360
    #setting = camera.base_settings
    x = 1440

    setting["res"] = [x, int(x/2)]

    cam = camera.Camera([0.0, 0.0, 0.0], [0.0, 0.0], settings=setting)
    camera.save_frame(cam.render(world), "render/graph.png")
    print("took", int(time.time()-start))
    exit()

ffmpeg = 'ffmpeg -r 24 -i "render/frame%04d.png" -c:v libx264 -vf "fps=24,format=yuv420p" render/out.mp4 -y'
os.system("rm render/frame*.png")
a = time.time()


def render(frame):
    # Render the required frame in a thread safe manner

    # Output file name with 4 digits.
    filename = "render/frame{frame:04d}.png".format(frame=frame)

    # Create scene object
    world = scene.Scene([0, 0, 0], "TestScene.json")
    world.advance_frame(frame)  # Advance time to current frame

    # Load camera settings
    setting = camera.base_settings

    x = 64
    setting["res"] = [x, int(x/1)]

    # Initiate camera
    cam = camera.Camera([0, 0, 0], [0, 0], settings=setting)
    frame = cam.render(world)  # Render frame
    camera.save_frame(frame, filename)  # Output frame

    return filename  # Return from thread


if __name__ == "__main__":
    with Pool(50) as p:
        print(p.map(render, range(0, 24)))

os.system(ffmpeg)

print("\n\n---------------\nIt took", int(time.time()-a), "Seconds to render")


