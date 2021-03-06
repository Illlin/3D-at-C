# Handles the rendering of an image
from objects.base import *
from PIL import Image
import texture

mag = np.linalg.norm

x = 1024
base_settings = {
    "fov":          0.5*np.pi,
    "res":          [x, x],#//2],
    "min_dist":     0.001,
    "max_dist":     10,
    "gamma":  3
}

cam_360 = {
    "fov":          2*np.pi,
    "res":          [x, x//2],
    "min_dist":     0.001,
    "max_dist":     100,
    "gamma":  5
}

cam_180 = {
    "fov":          1*np.pi,
    "res":          [x, x],
    "min_dist":     0.001,
    "max_dist":     100,
    "gamma":  3
}

base_texture = texture.Texture("UV_Grid_Sm.jpg", 1024)
background = texture.Texture("stars.png", 1440*4)


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
    min_factor = 0
    fact = 1 - min_factor
    if 380 <= wl < 420:
        factor = min_factor + fact * ((wl - 380) / (420 - 380))
    elif 420 <= wl < 701:
        factor = 1
    elif 701 <= wl < 780:
        factor = min_factor + fact * ((780 - wl) / (780 - 700))
    else:
        factor = 0

    colour = [max_intencity * pow(val * factor, gamma) for val in colour]

    if round:
        colour = [int(x) for x in colour]

    return np.array(colour)


def red_shift_wl(dv, wl, c, doppler=True, lorenz=True):
    # If this is not the case, physics handler is broken and this function will divide by zero
    assert -c < dv < c

    # First we will account for time dilation of the frequency of light emitted using the Lorentz factor of the objects
    if lorenz:
        colour_freq = c / wl

        # https://www.bbc.co.uk/bitesize/guides/zwdwwmn/revision/2
        lorentz_inv = np.sqrt(1 - ((dv * dv) / (c * c)))  # 1 / Relative time

        new_freq = lorentz_inv * colour_freq

        new_wl = c / new_freq
    else:
        new_wl = wl
    # Now we account for redshift caused by relative motion of the objects
    # http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/redshf.html

    # Work out the Doppler factor ( Does not account for time dilation)
    if doppler:
        b = dv / c
        z = np.sqrt((1+b)/(1-b))-1

        final_wl = (z+1) * new_wl
    else:
        final_wl = new_wl

    final_colour = wl_to_rgb(final_wl)

    return final_colour


def red_shift_rgb(dv, base_colour, c, base_wl = np.array([650, 510, 440]), doppler=True, lorenz=True):
    # If this is not the case, physics handler is broken and this function will divide by zero
    assert -c < dv < c

    # First we will account for time dilation of the frequency of light emitted using the Lorentz factor of the objects
    if lorenz:
        colour_freq = c / base_wl

        # https://www.bbc.co.uk/bitesize/guides/zwdwwmn/revision/2
        lorentz_inv = np.sqrt(1 - ((dv * dv) / (c * c)))  # 1 / Relative time

        new_freq = lorentz_inv * colour_freq

        new_wl = c / new_freq
    else:
        new_wl = base_wl

    # Now we account for redshift caused by relative motion of the objects
    # http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/redshf.html

    # Work out the Doppler factor ( Does not account for time dilation)
    if doppler:
        b = dv / c
        z = np.sqrt((1+b)/(1-b))-1

        final_wl = (z+1) * new_wl
    else:
        final_wl = new_wl

    colour_mix = np.array([wl_to_rgb(wl, max_intencity=1, round=False) for wl in final_wl])

    final_r = base_colour[0] * colour_mix[0]
    final_g = base_colour[1] * colour_mix[1]
    final_b = base_colour[2] * colour_mix[2]
    final_colour = [final_r, final_g, final_b]

    return np.array([int(x) for x in sum(final_colour)])


def cast_ray(start, scene: Base, uv, max_d, min_d, flags, screen_pos):
    # Flags:
    #  1    Render Texture
    #  2    Render Redshift (Doppler)
    #  4    Render Redshift (Lorenz)
    #  8    Render Length Contraction
    # 16    Render Background
    # 32
    # 64

    ray = Ray()
    hit = False
    pos = start
    one_arr = np.array([1,1,1])
    white = np.array([255,255,255])

    while not hit:
        if flags & 8 == 8:
            # Get speed of object:
            speed = scene.get_speed_at(pos)

            if mag(speed) > 5:  # FIXING SHIT
                print("Something bad")

            speed_uv = (speed/mag(speed))
            lorenz = 1/np.sqrt(1-(speed*speed)/(scene.c*scene.c))

            scale = np.array([1, 1, 1])/lorenz

            distance_to = scene.distance_to(pos/scale) * min(scale)

        else:
            distance_to = scene.distance_to(pos)

        pos = pos + (distance_to * uv)
        ray.distance_travelled += distance_to
        ray.steps += 1

        if distance_to < min_d:
            # If at the target return the ray
            # TODO
            # Get hit object

            v1 = scene.get_speed_at(pos) # Velocity of hit object
            direction = pos-start
            uv_direction = direction/mag(direction)
            dv = v1*uv_direction
            mag_dv = mag(dv) * np.sign(np.dot(dv, one_arr))

            if flags & 1 == 1:
                if flags & 8 == 8:
                    text_pos = pos / scale
                    #colour = base_texture.get_point(text_pos - scene.object_at_point(pos).pos)
                else:
                    pass
                    #colour = base_texture.get_point(pos - scene.object_at_point(pos).pos)
            else:
                pass
                #colour = white

            colour = white

            ray.surface_colour = red_shift_wl(
                mag_dv,
                550,
                scene.c,
                doppler=(flags & 2 == 2),
                lorenz=(flags & 4 == 4)

            )

            hit = True
            ray.hit_pos = pos
            ray.hit = True
            return ray

        elif ray.distance_travelled > max_d:
            # If the ray left the render area
            if flags & 16 == 16:
                colour = background.get_point2d(screen_pos)

                #colour = white
                ray.surface_colour = colour[:]
            else:
                ray.surface_colour = (255, 255, 255)
            hit = True
            ray.hit_pos = pos
            return ray


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
            for x in range(0, res[0]):  # Screen horizontal pos
                pixel_pos_spherical = self.look_pos - offset + horisontal_step*x + vertical_step*y
                pixel_pos_cartesian = spherical_to_cartesian(pixel_pos_spherical)

                ray = cast_ray(
                    self.pos,
                    scene,
                    pixel_pos_cartesian,
                    max_d,
                    min_d,
                    scene.flags,
                    np.array([x/res[0], y/res[0]])/2
                )

                if ray.distance_travelled > max_d:
                    factor = 1
                else:
                    factor = float(dropoff/(ray.distance_travelled*ray.distance_travelled))
                col = factor*ray.surface_colour
                rgb = tuple([int(x) for x in col])

                frame[x+(y*res[0])] = rgb

            print((y*100)/res[1]//1, "%")
        return res, frame


def save_frame(frame, file_location):
    image = Image.new("RGB", frame[0])
    image.putdata(frame[1])
    #image = image.convert("RGB")
    image.save(file_location)