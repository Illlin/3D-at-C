from objects.base import *
import objects
import json

supported = {
    "Cube": objects.cube.Cube,
    "Sphere": objects.sphere.Sphere
}


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
        for shape in self.objects:
            dist = min(shape.distance_to(other), dist)

        return dist

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

        flags = 0
        for i, c in enumerate(flags_arr):
            flags += c*(2**(len(flags_arr)-(i+1)))

        for shape in scene["Shapes"]:
            shape_type = shape[0]
            creator = shape[1]
            phys = shape[2]
            shape_object = supported[shape_type](*creator)
            shape_object.phys_init(*phys)
            self.objects.append(shape_object)
