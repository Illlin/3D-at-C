# Handles the rendering of an image
from objects.base import *
from PIL import Image
import texture

x = 512
base_settings = {
    "fov":          0.5*np.pi,
    "res":          [x, x],#//2],
    "min_dist":     0.001,
    "max_dist":     100,
    "colour_drop":  1
}

cam_360 = {
    "fov":          2*np.pi,
    "res":          [x, x//2],
    "min_dist":     0.001,
    "max_dist":     100,
    "colour_drop":  1
}


class Ray:
    # Class to hold data a ray will gather
    # I will use external functions for ray traversal for speed reasons

    def __init__(self):
        self.surface_colour = (0, 0, 0)
        self.steps = 0
        self.hit_object = None
        self.distance_travelled = 0
        self.hit_pos = np.array([0, 0, 0])
        self.hit = False


def cast_ray(start, scene: Base, uv, max_d, min_d):
    ray = Ray()
    hit = False
    pos = start

    while not hit:
        distance_to = scene.distance_to(pos)

        if distance_to < min_d:
            # If at the target return the ray
            # TODO
            # Get hit object
            ray.surface_colour = texture.get_point(pos)  # [255,255,255]
            hit = True
            ray.hit_pos = pos
            ray.hit = True
            return ray

        elif ray.distance_travelled > max_d:
            # If the ray left the render area

            hit = True
            ray.hit_pos = pos
            return ray

        pos = pos + (distance_to*uv)
        ray.distance_travelled += distance_to
        ray.steps += 1


class Camera(Base):
    def __init__(self, pos, look_pos, settings=base_settings):
        super().__init__(pos)
        self.settings = settings
        self.look_pos = look_pos

    def render(self, scene):
        dropoff = self.settings["colour_drop"]
        res = self.settings["res"]
        min_d = self.settings["min_dist"]
        max_d = self.settings["max_dist"]

        frame = [[]] * (res[0]*res[1])  # Hold the frame

        horisontal_step = np.array([self.settings["fov"] / res[0], 0])
        vertical_step = horisontal_step[::-1]  # Flip array

        offset = np.array(horisontal_step*(res[0]//2) + vertical_step*(res[1]//2))

        for y in range(0, res[1]):  # Screen vertical pos
            for x in range(0, res[0]):  # Screen horisontal pos

                pixel_pos_spherical = self.look_pos - offset + horisontal_step*x + vertical_step*y
                pixel_pos_cartesian = spherical_to_cartesian(pixel_pos_spherical)

                ray = cast_ray(self.pos, scene, pixel_pos_cartesian, max_d, min_d)

                frame[x+(y*res[0])] = (
                    ray.surface_colour[0],
                    ray.surface_colour[1],
                    int(((dropoff/(ray.distance_travelled*ray.distance_travelled))*ray.surface_colour[2]))
                )

            print((y*100)/res[1]//1, "%")
        return res, frame


def save_frame(frame, file_location):
    image = Image.new("HSV", frame[0])
    image.putdata(frame[1])
    image = image.convert("RGB")
    image.save(file_location)
