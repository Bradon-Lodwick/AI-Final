import random
import numpy as np
from collections import Counter

from PIL import Image, ImageSequence


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

    def move(self, direc, dist):
        if direc == "N" and self.location[0] - dist >= 0:
            self.location[0] -= dist
        elif direc == "E" and self.location[1] + dist < self.canvas_dim[0]:
            self.location[1] += dist
        elif direc == "S" and self.location[0] + dist < self.canvas_dim[1]:
            self.location[0] += dist
        elif direc == "W"and self.location[1] - dist >= 0:
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
            neighbor_north = 1

        if self.location[1] + 1 < self.canvas_dim[0]:
            neighbor_east = ar[self.location[0], self.location[1] + 1]
        else:
            neighbor_east = 1
            
        if self.location[0] + 1 < self.canvas_dim[1]:
            neighbor_south = ar[self.location[0] + 1, self.location[1]]
        else:
            neighbor_south = 1
            
        if self.location[1] - 1 >= 0:
            neighbor_west = ar[self.location[0], self.location[1] - 1]
        else:
            neighbor_west = 1

        total = neighbor_north + neighbor_east + neighbor_south + neighbor_west
        if total == 0:
            return 0.25, 0.25, 0.25, 0.25


        if neighbor_north/total > 1.0 or neighbor_east/total > 1.0 or neighbor_south/total > 1.0 or neighbor_west/total > 1.0:
            print("what")

        if neighbor_north/total + neighbor_east/total + neighbor_south/total + neighbor_west/total == 1:
            print("Good")
        else:
            print("Bad")

        return neighbor_north/total, neighbor_east/total, neighbor_south/total, neighbor_west/total



if __name__ == '__main__':

    im = Image.new("L", (100, 100), 0)
    ar = np.array(im)

    pen = Pencil([50, 50], ar)
    c = 1
    for i in range(50000):
        pen.move_random(1)
        ar[pen.get_loc()] = ar[pen.get_loc()]+10
        pen.neighbor_weights()
        c -= 0.01

    om = Image.fromarray(ar)

    om.save("Blank.png")
