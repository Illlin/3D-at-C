import numpy as np
from functools import lru_cache

# Useful functions

mag = np.linalg.norm


def spherical_to_cartesian(spherical):
    # Convert Spherical coordinates to Cartesian

    az = spherical[0]
    el = spherical[1]

    x = np.cos(el) * np.cos(az)
    y = np.cos(el) * np.sin(az)
    z = np.sin(el)

    return np.array([x, y, z])


@lru_cache(maxsize=32)
def rotate(theta):
    c = np.cos(theta)
    s = np.sin(theta)

    return np.mat([[1, 0, 0],
                   [0, c, -s],
                   [0, s, c]])

    return np.mat([[c,  0,  s],
                   [0,  1,  0],
                   [-s, 0,  c]])


# Base 3d Object
def default_move_func(vel, delta):
    return delta*vel


def angular_velocity(pos, rot):
    # around X axis
    x = np.zeros(3)
    w = rot[0]
    x_v = np.array([-pos[2], pos[1]])
    x_v = w * (x_v / mag(x_v))

    if np.isnan(x_v).any():
        x_v = np.zeros(2)

    x[2] = -x_v[0]
    x[1] = x_v[1]

    # around Y axis
    y = np.zeros(3)
    w = rot[1]
    y_v = np.array([-pos[2], -pos[0]])
    y_v = w * (y_v / mag(y_v))

    if np.isnan(y_v).any():
        y_v = np.zeros(2)

    y[0] = y_v[0]
    y[1] = y_v[1]

    # around Z axis
    z = np.zeros(3)
    w = rot[2]
    z_v = np.array([pos[1], pos[0]])
    z_v = w*(z_v/mag(z_v))

    if np.isnan(z_v).any():
        z_v = np.zeros(2)

    z[0] = z_v[0]
    z[1] = z_v[1]

    return np.sqrt(x*x + y*y + z*z)





class Base:
    # Basic 3d object. Includes all required 3d object functions

    def __init__(self, pos):
        self.pos = np.array(pos)
        self.vel = np.array([0, 0, 0])
        self.rot = np.array([0., 0., 0.])
        self.rot_vel = np.array([0, 0, 0])
        self.move_func = default_move_func
        self.c = 0

    def phys_init(self, vel, rot_vel):
        self.vel = np.array(vel)
        self.rot_vel = np.array(rot_vel)

    def distance_to(self, other):
        # Get the minimum distance from a point to the object

        return self.pos - other

    def get_speed_at(self, pos):
        # Hacky fix TODO remove hacky fix
        safe_speed = 4.95
        #return self.vel
        #return min(ma, safe_speed)

        speed = self.vel.copy()

        speed += angular_velocity(self.pos - pos, self.rot_vel)

        ma = mag(speed)
        if ma > safe_speed:
            return safe_speed*(speed/ma)

        return speed

    def move(self, delta):
        self.rot += self.move_func(self.rot_vel, delta)
        self.pos += self.move_func(self.vel, delta)
        print(delta, self.vel, self.pos)
        # Delta represents the time between frames
        if False:
            if delta > 2:
                t = 2.0
                a = np.array([0.0,-2.45,0.0])
                self.pos += self.vel*t+0.5*a*t*t
                self.vel = self.vel+a*t

                t = delta - 2
                a = np.array([0.0, 2.45, 0.0])
                self.pos += self.vel * t + 0.5 * a * t * t
                self.vel = self.vel + a * t

            else:
                a = np.array([0.0, -2.45, 0.0])
                self.pos += self.vel * delta + 0.5 * a * delta * delta
                self.vel = self.vel + a * delta

            print(delta, self.vel, self.pos)
            # Split into two functions
            self.rot += self.move_func(self.rot_vel, delta)
            self.vel += self.move_func(self.vel, delta)






class Scene(Base):
    # A set of objects

    def __init__(self, objects):
        super().__init__([0, 0, 0])
        self.objects = objects

    def distance_to(self, other):
        return min([x.distance_to(other) for x in self.objects])

