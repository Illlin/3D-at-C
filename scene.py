from objects.base import *
import objects
import json

supported = {
    "Cube": objects.cube.Cube,
    "Sphere": objects.sphere.Sphere
}


def load_object(input_arr):
    if input_arr[0] in supported:
        shape_type = supported[input_arr[0]]
        constructor = []
        for part in input_arr[1]:
            if type(part) == list:
                if part[0] in supported:
                    constructor.append(load_object(part))
                else:
                    constructor.append(part)
        shape_object = shape_type(*constructor)
        if len(input_arr) == 3:
            shape_object.phys_init(*input_arr[2])

        return shape_object


class Scene(Base):
    # A 3d Scene to handle complex building of enviromnments from a file

    def __init__(self, pos, file):
        super().__init__(pos)
        self.pos = np.array(pos)

        self.objects = []
        self.c = None
        self.fps = None
        self.frames = None
        self.flags = None
        self.frame = None

        self.load_file(file)

    def distance_to(self, other):
        # Multi Object Distance Function

        dist = np.inf
        closest = None
        for shape in self.objects:
            dist_new = shape.distance_to(other)
            if dist_new < dist:
                dist = dist_new
                closest = object

        return dist

    def object_at_point(self, point):
        # Get the closest object at a point

        dist = np.inf
        closest = None
        for shape in self.objects:
            dist_new = shape.distance_to(point)
            if dist_new < dist:
                dist = dist_new
                closest = shape

        return closest

    def move(self, delta):
        for shape in self.objects:
            shape.move(delta)

    def get_speed_at(self, pos):
        return self.object_at_point(pos).get_speed_at(pos)

    def advance_frame(self, no):
        self.move(no/self.fps)
        self.frame += no

    def load_file(self, file):
        content = ""

        with open(file, "r") as scene_file:
            for line in scene_file:
                content += line
        scene = json.loads(content)

        self.c = scene["C"]
        self.fps = scene["FPS"]
        self.frames = scene["Frames"]
        flags_arr = scene["Flags"]
        self.frame = scene["Frame"]

        self.flags = 0
        for i, c in enumerate(flags_arr):
            self.flags += c*(2**(len(flags_arr)-(i+1)))

        for shape in scene["Shapes"]:
            self.objects.append(load_object(shape))

        if self.frame != 0:
            self.move(self.frame/self.fps)

