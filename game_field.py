""" The file that holds the gameField and it's functions

TODO
----
* replace get_location with proper coordinate function

"""

__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

import numpy as np
import settings


class GameField:
    """ The field that the game will be played on. Simulates the sensors that the agents would use, by doing things
    like sensing the objects around it.

    Attributes
    ----------
    length : int
        The length of the game field.
    width : int
        The width of the game field.
    game_objects : list
        The list of game objects on the game field.

    """

    # length and width of field
    length = None
    width = None
    game_objects = []   # list of all objects on the field

    def __init__(self, game_objects, length=settings.length, width=settings.width):
        """ Initializes the game field

        Parameters
        ----------
        game_objects : list
            The initial list of game objects.
        length : int
            The length of the game field.
        width : int
            The width of the game field.
           
        """
        self.length = length
        self.width = width
        self.game_objects = game_objects

        # Loops through the game objects and assigns their field value to the current field
        for obj in game_objects:
            obj.set_field(self)

    # adds a new object to the field
    def add_object(self, new_object):
        self.game_objects.append(new_object)
        new_object.set_field(self)

    def remove_object(self, object):
        self.game_objects.remove(object)

    # function that will return all other objects within radius of an agent
    # TODO get_location should be consistent with game_objects location function
    def scan_radius(self, agent, radius):
        origin = agent.get_location()
        surroundings = []

        # loops through all objects on the field
        for x in self.game_objects:
            if x != agent:
                loc = x.get_location()
                # Calculates distance between objects
                distance = abs((loc[0]-origin[0])**2 + (loc[1]-origin[1])**2)**0.5

                # If the distance is less than the search radius the object is added to surroundings
                if distance < radius:
                    # A list of all nearby objects is returned to the agent
                    surroundings.append(x)

        return surroundings
