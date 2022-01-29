# Handles the rendering of an image

from objects.base import *

base_settings = {
    "fov":          0.5*np.pi,
    "res":          [100, 100],
    "min_dist":     0.001,
    "max_dist":     100
}


def cast_ray(start, scene: Base, uv, max_d, min_d):
    ray = Ray()
    hit = False
    pos = start

    while not hit:
        distance_to = scene.distance_to(pos)

        if distance_to < min_d:
            # If at the target return the ray
            # TODO
            # Get colour
            # Get hit object

            ray.surface_colour = np.array([1, 1, 1])
            hit = True
            ray.hit_pos = pos
            ray.hit = True
            return ray

        if ray.distance_travelled > max_d:
            # If the ray left the render area

            hit = True
            ray.hit_pos = pos
            return ray

        pos = pos + (distance_to*uv)
        ray.distance_travelled += distance_to
        ray.steps += 1


class Ray:
    # Class to hold data a ray will gather
    # I will use external functions for ray traversal for speed reasons

    def __init__(self):
        self.surface_colour = np.array([0, 0, 0])
        self.steps = 0
        self.hit_object = None
        self.distance_travelled = 0
        self.hit_pos = np.array([0, 0, 0])
        self.hit = False


class Camera(Base):
    def __init__(self, pos, look_pos, settings=base_settings):
        super().__init__(pos)
        self.settings = settings
        self.look_pos = look_pos

    def render(self, scene):
        res = self.settings["res"]
        min_d = self.settings["min_dist"]
        max_d = self.settings["max_dist"]

        frame = [[]] * (res[0]*res[1])  # Hold the frame

        horisontal_step = np.array([self.settings["fov"] / res[0], 0])
        vertical_step = horisontal_step[::-1]  # Flip array

        offset = np.array(horisontal_step*(res[0]//2) + vertical_step*(res[1]//2))

        prt = ""

        for y in range(0, res[1]):  # Screen vertical pos
            for x in range(0, res[0]):  # Screen horisontal pos
                pixel_pos_spherical = self.look_pos - offset + horisontal_step*x + vertical_step*y
                pixel_pos_cartesian = spherical_to_cartesian(pixel_pos_spherical)

                ray = cast_ray(self.pos, scene, pixel_pos_cartesian, max_d, min_d)

                if ray.hit:
                    prt += "██"
                else:
                    prt += "  "

                frame[x+(y*res[0])] = ray.surface_colour

            prt += "\n"

        print(prt)
