""" The file that holds the gameField and it's functions

TODO
----
*replace get_location with proper coordinate function

"""
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

import numpy as np
import settings


class GameField:

    # length and width of field
    length = None
    width = None
    game_objects = []   # list of all objects on the field

    # initialized based on settings file
    def __init__(self):
        self.length = settings.length
        self.width = settings.width

    # adds a new object to the field
    def add_objects(self, new_object):
        self.game_objects.append(new_object)

    # function that will return all other objects within radius of an agent
    # TODO get_location should be consistent with game_objects location function
    def scan_radius(self, agent, radius):
        origin = agent.get_location()
        surroundings = []

        # loops through all objects on the field
        for x in self.game_objects:
            if x != agent:
                loc = x.get_location()
                distance = abs((loc[0]-origin[0])**2 + (loc[1]-origin[1])**2)**0.5 # calculates distance between objects

                if distance < radius: # if the distance is less than the search radius the object is added to surroundings
                    surroundings.append((x.__class__.__name__, x.get_name(), x.get_location()))  # a list of all nearby objects is returned to the agent

        return surroundings
