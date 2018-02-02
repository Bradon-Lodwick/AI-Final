import random
import numpy as np
from PIL import Image
import imageio
import glob


def save_gif(images):
    sequence = []
    for ima in images:
        sequence.append(imageio.imread(ima))

    imageio.mimsave("gif/Weight_Map2.gif", sequence)


class Pencil:
    location = []
    canvas = None
    canvas_dim = tuple

    probability = [0.25, 0.25, 0.25, 0.25]
    directions = ["N", "E", "S", "W"]

    def __init__(self, origin, canvas):
        self.location = origin
        self.canvas = canvas
        self.canvas_dim = np.shape(canvas)[:2]

    def move(self, direction, dist):
        if direction == "N" and self.location[0] - dist >= 0:
            self.location[0] -= dist
        elif direction == "E" and self.location[1] + dist < self.canvas_dim[0]:
            self.location[1] += dist
        elif direction == "S" and self.location[0] + dist < self.canvas_dim[1]:
            self.location[0] += dist
        elif direction == "W" and self.location[1] - dist >= 0:
            self.location[1] -= dist
        else:
            return 1

        return 0

    def move_random(self, dist):

        d = random.choice(self.directions)

        self.move(d, dist)

    def get_loc(self):
        return self.location[0], self.location[1]

    def neighbor_weights(self):

        if self.location[0] - 1 >= 0:
            neighbor_north = ar[self.location[0] - 1, self.location[1]]
        else:
            neighbor_north = 255

        if self.location[1] + 1 < self.canvas_dim[0]:
            neighbor_east = ar[self.location[0], self.location[1] + 1]
        else:
            neighbor_east = 255

        if self.location[0] + 1 < self.canvas_dim[1]:
            neighbor_south = ar[self.location[0] + 1, self.location[1]]
        else:
            neighbor_south = 255

        if self.location[1] - 1 >= 0:
            neighbor_west = ar[self.location[0], self.location[1] - 1]
        else:
            neighbor_west = 255

        total = int(neighbor_north) + int(neighbor_east) + int(neighbor_south) + int(neighbor_west)
        if total == 0:
            return [0.25, 0.25, 0.25, 0.25]

        neighbor_north = neighbor_north / total

        neighbor_east = neighbor_east / total

        neighbor_south = neighbor_south / total

        neighbor_west = neighbor_west / total

        # fix is a check to make sure the probabilities are equal to 1
        fix = neighbor_north + neighbor_east + neighbor_south + neighbor_west

        if neighbor_north > 1.0 or neighbor_east > 1.0 or neighbor_south > 1.0 \
                or neighbor_west > 1.0:

            raise ValueError("Probability cannot be higher than 1 N:{} E:{} S:{} W:{}".format
                             (neighbor_north, neighbor_east, neighbor_south, neighbor_west))

        elif fix != 1:
            fix = 1 - fix
            return [neighbor_north + fix, neighbor_east, neighbor_south, neighbor_west]

        return [neighbor_north, neighbor_east, neighbor_south, neighbor_west]


if __name__ == '__main__':

    im = Image.new("L", (100, 100), 255)
    ar = np.array(im)
    pen = Pencil([50, 50], ar)

    for i in range(20000):
        ar[pen.get_loc()] = ar[pen.get_loc()] - 100
        if ar[pen.get_loc()] < 0:
            ar[pen.get_loc()] = 0
        choice = np.random.choice(["N", "E", "S", "W"], p=pen.neighbor_weights())  # 0.25, 0.25, 0.25, 0.25])
        pen.move(choice, 1)

        ar[:, :] = 255 - ar[:, :]
        if i % 100 == 0:
            om = Image.fromarray(ar)
            om.save("frames5/Blank{}.png".format(i))
        ar[:, :] = 255 - ar[:, :]

    """
    frames = []

    for file in glob.glob("frames4/*.png"):
        frames.append(file)

    save_gif(frames)
    """