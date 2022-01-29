# Handles the rendering of an image

from objects.base import *

base_settings = {
    "fov":          1/2*np.pi,
    "res":          [1024, 1024],
    "min_dist":     0.001,
    "max_dist":     100
}


class Camera(Base):
    def __init__(self, pos, look_pos, settings=base_settings):
        super().__init__(pos)
        self.settings = settings
        self.look_pos = look_pos

    def render(self, scene):

        res = self.settings["res"]
        horisontal_step = np.array([self.settings["fov"] / res[0], 0])
        vertical_step = horisontal_step[::-1]  # Flip array

        offset = np.array(horisontal_step*(res[0]//2) + vertical_step*(res[1]//2))

        a = {}

        for y in range(0, res[1]):  # Screen vertical pos
            for x in range(0, res[0]):  # Screen horisontal pos
                pixel_pos_spherical = self.look_pos - offset + horisontal_step*x + vertical_step*y
                pixel_pos_cartesian = spherical_to_cartesian(pixel_pos_spherical)

                x = str(mag(pixel_pos_cartesian))
                if x in a:
                    a[x] += 1
                else:
                    a[x] = 1

        print(a)
