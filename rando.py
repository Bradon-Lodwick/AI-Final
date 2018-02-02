"""
Tester Pencil class, Pencil acts as a pseudo agent that will move
partially randomly based on where it has been previously
"""

import random
import numpy as np
from PIL import Image


class Pencil:
    """
    Attributes
    ----------

    location : list
        Current location of pencil on the canvas
    canvas : matrix
        The drawing surface from the pencil
    canvas_dim : tuple
        The dimensions of the canvas
    """

    location = []
    canvas = None
    canvas_dim = tuple
    directions = ["N", "E", "S", "W"]

    def __init__(self, origin, canvas):
        """Constructor for the Pencil class

        :param origin:
            The initial start point for the pencil
        :param canvas:
            The image matrix to be drawn on

        """
        self.location = origin
        self.canvas = canvas
        self.canvas_dim = np.shape(canvas)[:2]

    def move(self, direction, dist):
        """Moves the pencil to a new location

        :param direction:
            The direction for the pencil to travel
        :param dist:
            How far the Pencil will move
        :return:
        """

        #   Adjusts the position based off the given Direction and Distance
        if direction == "N" and self.location[0] - dist >= 0:
            self.location[0] -= dist
        elif direction == "E" and self.location[1] + dist < self.canvas_dim[0]:
            self.location[1] += dist
        elif direction == "S" and self.location[0] + dist < self.canvas_dim[1]:
            self.location[0] += dist
        elif direction == "W" and self.location[1] - dist >= 0:
            self.location[1] -= dist
        else:
            return 1  # If the pencil is unable to be moved it returns 1

        return 0  # If the pencil moved it returns 0

    def move_random(self, dist):
        """ Moves in a random direction a specified distance

        :param dist:
            How far to move
        """

        # Chooses a random direction from directions
        d = random.choice(self.directions)

        self.move(d, dist)

    def get_loc(self):
        """ Get's Pencil location as a tuple

        :return:
            Pencil location
        """
        return self.location[0], self.location[1]

    def neighbor_weights(self):
        """ Weighs the nearby neighbours based off colour
         to decide a preferred direction **discontinued**

        :return:
            returns a probability list that corresponds to directions
        """

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

    def move_random_weighted(self):
        # TODO add parameters for radar distance, and move distance
        """ Moves the pencil in a random direction based off
        the nearest ten neighbors in all four directions

        """

        # Creates a sub array from the canvas matrix,
        # sub arrays are the ten closest cells to the pencils current location
        # The average of the ten cells are found and assigned to North, East, South, and West
        neighbor_north = int(self.canvas[self.location[0] - 10: self.location[0], self.location[1]].sum() / 10)

        neighbor_east = int(self.canvas[self.location[0], self.location[1] + 1: self.location[1] + 11].sum() / 10)

        neighbor_south = int(self.canvas[self.location[0] + 1: self.location[0] + 11, self.location[1]].sum() / 10)

        neighbor_west = int(self.canvas[self.location[0], self.location[1] - 10: self.location[1]].sum() / 10)

        # The total of all directional values is calculated
        total = int(neighbor_north) + int(neighbor_east) + int(neighbor_south) + int(neighbor_west)

        # If the total is 0 the pencil will move randomly with even weights,
        # this avoids divide by zero error
        if total == 0:
            self.move_random(1)
            return

        # Probability of each direction is calculated based on their percentage
        neighbor_north = neighbor_north / total

        neighbor_east = neighbor_east / total

        neighbor_south = neighbor_south / total

        neighbor_west = neighbor_west / total

        # fix is a check to make sure the probabilities are equal to 1
        fix = neighbor_north + neighbor_east + neighbor_south + neighbor_west

        # if any probabilities are greater than 1 raises ValueError
        if neighbor_north > 1.0 or neighbor_east > 1.0 or neighbor_south > 1.0 \
                or neighbor_west > 1.0:

            raise ValueError("Probability cannot be higher than 1 N:{} E:{} S:{} W:{}".format
                             (neighbor_north, neighbor_east, neighbor_south, neighbor_west))

        # if probabilities do not sum to 1 the difference is added to North's probability
        # This does makes north more likely but since fix comes from rounding errors the difference is negligible
        # could be solved by dividing fix by four and adding evenly but this could result in more error
        # d is the chosen direction
        elif fix != 1:
            fix = 1 - fix
            d = np.random.choice(self.directions,
                                 p=[neighbor_north + fix, neighbor_east, neighbor_south, neighbor_west])
        else:
            d = np.random.choice(self.directions, p=[neighbor_north, neighbor_east, neighbor_south, neighbor_west])

        # the canvas at the current location is darkened
        self.canvas[self.get_loc()] = self.canvas[self.get_loc()] - 25
        # prevents colour value from being negative
        if self.canvas[pen.get_loc()] < 0:
            self.canvas[pen.get_loc()] = 0
        # pencil is moved in direction d
        self.move(d, 1)


if __name__ == '__main__':
    # Creates blank white canvas
    im = Image.new("L", (100, 100), 255)
    ar = np.array(im)  # [:, :, 0] < needed if using an image for canvas sometimes TODO try catch maybe?
    # creates new pencil at 50, 50
    pen = Pencil([50, 50], ar)

    # moves i steps
    for i in range(10000):
        pen.move_random_weighted()
        # Every 100 steps the canvas is saved for external gif reasons
        if i % 100 == 0:
            om = Image.fromarray(255 - pen.canvas)  # canvas colours inverted for easier viewing
            om.save("MainFrames/test/test{}.png".format(i))
