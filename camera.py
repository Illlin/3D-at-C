# Handles the rendering of an image
from objects.base import *
from PIL import Image
import texture
import math

x = 512
base_settings = {
    "fov":          0.5*np.pi,
    "res":          [x, x],#//2],
    "min_dist":     0.001,
    "max_dist":     100,
    "gamma":  1
}

cam_360 = {
    "fov":          2*np.pi,
    "res":          [x, x//2],
    "min_dist":     0.001,
    "max_dist":     100,
    "gamma":  1
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


def wl_to_rgb(wl, gamma = 0.8, max_intencity = 255, round=True):
    # http://www.physics.sfasu.edu/astro/color/spectra.html
    # Colour space mapping used from source

    # Get base colour
    if 380 <= wl < 440:
        colour = [
            -(wl - 440) / (440 - 380),
            0,
            1
        ]
    elif 440 <= wl < 490:
        colour = [
            0,
            (wl - 440) / (490 - 440),
            1
        ]
    elif 490 <= wl < 510:
        colour = [
            0,
            1,
            -(wl - 510) / (510 - 490)
        ]
    elif 510 <= wl < 580:
        colour = [
            (wl - 510) / (580 - 510),
            1,
            0
        ]
    elif 580 <= wl < 645:
        colour = [
            1,
            -(wl - 645) / (645 - 580),
            0
        ]
    elif 645 <= wl < 781:
        colour = [
            1,
            0,
            0
        ]
    else:
        colour = [0, 0, 0]

    # Drop off intencity at vision limits
    min = 0
    fact = 1-min
    if 380 <= wl < 420:
        factor = min + fact * ((wl - 380) / (420 - 380))
    elif 420 <= wl < 701:
        factor = 1
    elif 701 <= wl < 781:
        factor = min + fact * ((780 - wl) / (780 - 700))
    else:
        factor = 0

    colour = [max_intencity * (val * factor) for val in colour]
    #colour = [max_intencity * pow(val * factor, gamma) for val in colour]
    if round:
        colour = [int(x) for x in colour]

    return colour

def red_shift_wl(dv, wl, c):
    # If this is not the case, physics handler is broken and this function will divide by zero
    assert -c < dv < c

    # First we will account for time dilation of the frequency of light emitted using the Lorentz factor of the objects

    colour_freq = c / wl

    # https://www.bbc.co.uk/bitesize/guides/zwdwwmn/revision/2
    lorentz_inv = math.sqrt(1 - ((dv * dv) / (c * c)))  # 1 / Relative time

    new_freq = lorentz_inv * colour_freq

    new_wl = c / new_freq
    # Now we account for redshift caused by relative motion of the objects
    # http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/redshf.html

    # Work out the Doppler factor ( Does not account for time dilation)
    b = dv / c
    z = math.sqrt((1+b)/(1-b))-1

    final_wl = (z+1) * new_wl

    #colour_mix = np.array([wl_to_rgb(wl, max_intencity=1, round=False) for wl in final_wl])

    final_colour = wl_to_rgb(final_wl)
    return final_colour

def red_shift_rgb(dv, base_colour, c, base_wl = np.array([650, 510, 440])):
    # If this is not the case, physics handler is broken and this function will divide by zero
    assert -c < dv < c

    # First we will account for time dilation of the frequency of light emitted using the Lorentz factor of the objects

    colour_freq = c / base_wl

    # https://www.bbc.co.uk/bitesize/guides/zwdwwmn/revision/2
    lorentz_inv = math.sqrt(1 - ((dv * dv) / (c * c)))  # 1 / Relative time

    new_freq = lorentz_inv * colour_freq

    new_wl = c / new_freq
    # Now we account for redshift caused by relative motion of the objects
    # http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/redshf.html

    # Work out the Doppler factor ( Does not account for time dilation)
    b = dv / c
    z = math.sqrt((1+b)/(1-b))-1

    final_wl = (z+1) * new_wl

    colour_mix = np.array([wl_to_rgb(wl, max_intencity=1, round=False) for wl in final_wl])

    final_r = base_colour[0] * colour_mix[0]
    final_g = base_colour[1] * colour_mix[1]
    final_b = base_colour[2] * colour_mix[2]
    final_colour = [final_r, final_g, final_b]

    return [int(x) for x in sum(final_colour)]


#print("----result----\n", red_shift(0.8, np.array([0, 255, 0]), 5))





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
        dropoff = self.settings["gamma"]
        res = self.settings["res"]
        min_d = self.settings["min_dist"]
        max_d = self.settings["max_dist"]

        frame = [[]] * (res[0]*res[1])  # Hold the frame

        horisontal_step = np.array([self.settings["fov"] / res[0], 0])
        vertical_step = horisontal_step[::-1]  # Flip array

        offset = np.array(horisontal_step*(res[0]//2) + vertical_step*(res[1]//2))

        for y in range(0, res[1]):  # Screen vertical pos
            for x in range(0, res[0]):  # Screen horisontal pos
                #print(wl_to_rgb(y+400))
                #col = red_shift_wl((x-res[0]/2), y+1, res[0]/2+10)

                col = red_shift_rgb((x - res[0] / 2), texture.get_point(np.array([x/1024,0,y/1024])), res[0] / 2 + 10)
                #col = red_shift_rgb((x - res[0] / 2), (255,0,255), res[0] / 2 + 10)
                #col = wl_to_rgb(y)
                frame[x+(y*res[0])] = tuple(col)

                """
                pixel_pos_spherical = self.look_pos - offset + horisontal_step*x + vertical_step*y
                pixel_pos_cartesian = spherical_to_cartesian(pixel_pos_spherical)

                ray = cast_ray(self.pos, scene, pixel_pos_cartesian, max_d, min_d)

                frame[x+(y*res[0])] = (
                    ray.surface_colour[0],
                    ray.surface_colour[1],
                    int(((dropoff/(ray.distance_travelled*ray.distance_travelled))*ray.surface_colour[2]))
                )
                """

            print((y*100)/res[1]//1, "%")
        return res, frame


def save_frame(frame, file_location):
    image = Image.new("RGB", frame[0])
    image.putdata(frame[1])
    #image = image.convert("RGB")
    image.save(file_location)
