"""
Created GameObject class for Targets and Agents to inherit from
this is for easier interaction with the playing field and should keep them more consistent
"""
import settings

class GameObject:
    """
    Attributes
    ----------

    location : tuple
        current coordinates on the playing field
    name : str
        Name of the GameObject to be used in identification
    """

    location = []
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

    def move(self, direction, dist=settings.speed):
        if direction == settings.Direction.N:
            self.location[1] += dist
        if direction == settings.Direction.E:
            self.location[0] += dist
        if direction == settings.Direction.S:
            self.location[1] -= dist
        if direction == settings.Direction.W:
            self.location[0] -= dist

    def get_name(self):
        return self.name