"""
Created GameObject class for Targets and Agents to inherit from
this is for easier interaction with the playing field and should keep them more consistent
"""
import settings


class GameObject:
    """
    Attributes
    ----------

    location : list
        current coordinates on the playing field
    name : str
        Name of the GameObject to be used in identification
    """

    location = []
    name = str
    field = None

    def __init__(self, origin, name=None):
        # TODO Choose name format
        """ Constructor for the GameObject class.

        Parameters
        ----------
        origin : list
            The starting location of the object.
        name : str
            The name to be giving to the object.

        """
        self.location = origin
        self.name = name

    def get_location(self):
        """ Gets the location of the object."""
        return self.location

    def get_name(self):
        """ Gets the name of the object."""
        return self.name
    
    def set_field(self, field):
        self.field = field
