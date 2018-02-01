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

    def move(self, direction, dist=settings.speed):
        """ Moves the bot in the given direction.

        Parameters
        ----------
        direction : settings.Direction
            The direction to move the agent in.
        dist : int
            The distance to move the agent. Defaults to the speed specified in the settings file.

        Raises
        ------
        ValueError
            Raised in the case the given direction was invalid.

        """

        # Move North
        if direction == settings.Direction.N:
            self.location[1] += dist
        # Move East
        elif direction == settings.Direction.E:
            self.location[0] += dist
        # Move South
        elif direction == settings.Direction.S:
            self.location[1] -= dist
        # Move West
        elif direction == settings.Direction.W:
            self.location[0] -= dist
        # Raise an error if the movement was invalid
        else:
            raise ValueError("Invalid direction. Use directions defined in the settings.Direction Enum.")

    def get_name(self):
        """ Gets the name of the object."""
        return self.name
    
    def set_field(self, field):
        self.field = field
