"""
Created GameObject class for Targets and Agents to inherit from
this is for easier interaction with the playing field and should keep them more consistent
"""

from settings import Direction

class GameObject:
    """
    Attributes
    ----------

    location : tuple
        current coordinates on the playing field
    name : str
        Name of the GameObject to be used in identification
    """

    location = tuple
    name = str

    def __init__(self, origin, name=None):
        # TODO Choose name format
        """ Constructor for the GameObject class.

                Parameters
                ----------
                Origin: The starting location of the object
                name : the name to be giving to the object
        """
        self.location = origin
        self.name = name

    def get_location(self):
        return self.location

    def move(self, direction):
        if direction == Direction.N:
            self.location[1] += 1
        if direction == Direction.E:
            self.location[0] += 1
        if direction == Direction.S:
            self.location[1] -= 1
        if direction == Direction.W:
            self.location[0] -= 1

    def get_name(self):
        return self.name
