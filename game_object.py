"""
Created GameObject class for Targets and Agents to inherit from
this is for easier interaction with the playing field and should keep them more consistent
"""
class GameObject:
    """
    Attributes
    ----------

    location: current coordinates on the playing field
    name: Name of the GameObject to be used in identification
    """

    location = tuple
    name = str

    def __init__(self, origin, name="unspecified"):
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

    def move(self, x, y):
        self.location[0] += x
        self.location[1] += y

    def get_name(self):
        return self.name