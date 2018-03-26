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
from Settings import *
import numpy as np


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
        GameObject.__init__(self, game_field, g_id, location)
        # Creates the empty lists for the targets the agent has found
        self.self_targets_found = list()
        self.other_targets_found = list()
        # Initializes the agent's movement to the exploration mode
        self.movement_mode = MoveModes.EXPLORE
        # Initializes the memory of the map that the agent has seen
        self.memory = np.ones(shape=(size_x, size_y))
