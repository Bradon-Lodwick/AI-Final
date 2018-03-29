#!/usr/bin/env python
"""
The agent class and all its methods.

TODO
----

"""

# Authorship Information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

from GameObject import GameObject
from Target import Target
from Settings import *
from math import inf
import numpy as np
import random


class Agent(GameObject):
    """ The agent class and all its methods. Extended by the agent and target class.

        Attributes
        ----------
        game_field : GameField
            The game field that the object is on.
        g_id : int
            The id of the game object.
        location : list
            The location of the object on the game field.
        self_targets_found : list
            The list of targets that the agent has found for itself.
        other_targets_found : list
            The list of targets that the agent has found for other agents.
        movement_mode : char
            The movement mode that the object is in
        memory : np.Array
        """

    def __init__(self, game_field, g_id, location):
        """ TODO add a list for targets known but not collected
            TODO add a value to store previous movement direction to allow collision avoidance to force right turns
        """
        print("yes hello I am agent 2")
        GameObject.__init__(self, game_field, g_id, location)
        # Creates the empty lists for the targets the agent has found
        self.self_targets_found = list()
        self.other_targets_found = list()
        self.destinations = []
        # Initializes the agent's movement to the exploration mode
        self.movement_mode = MoveModes.EXPLORE
        # Initializes the memory of the map that the agent has seen
        self.memory = np.ones(shape=(size_x, size_y))
        self.drawing_location = [self.location[0] - 10, self.location[1] - 10]
        self.winner = False
        self.body = \
            "      +++++++++      " \
            "    ++.........++    " \
            "   +.............+   " \
            "  +...............+  " \
            " +.................+ " \
            " +.................+ " \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            "+.........{}.........+" \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            " +.................+ " \
            " +.................+ " \
            "  +...............+  " \
            "   +.............+   " \
            "    ++.........++    " \
            "      +++++++++      ".format(self.g_id)

        self.add_sub_locations()


    def add_sub_locations(self):
        for i in range(int(size_x/10)):
            for j in range(int(size_y/10)):
                self.destinations.append((i*10+5, j*10+5))



    def distance_from_self(self, coord):
        distance = abs(coord[0] - self.location[0]) + abs(coord[1] - self.location[1])
        return distance

    def step(self):
        if len(self.destinations) != 0:
            self.destinations.sort(key=lambda x: self.distance_from_self(x))
            if self.location[0] < self.destinations[0][0]:
                self.location[0] += 1
                self.drawing_location = [self.location[0] - 10, self.location[1] - 10]
            elif self.location[0] > self.destinations[0][0]:
                self.location[0] -= 1
                self.drawing_location = [self.location[0] - 10, self.location[1] - 10]
            elif self.location[1] < self.destinations[0][1]:
                self.location[1] += 1
                self.drawing_location = [self.location[0] - 10, self.location[1] - 10]
            elif self.location[1] > self.destinations[0][1]:
                self.location[1] -= 1
                self.drawing_location = [self.location[0] - 10, self.location[1] - 10]

            if self.location[0] == self.destinations[0][0] and self.location[1] == self.destinations[0][1]:
                self.destinations.pop(0)

