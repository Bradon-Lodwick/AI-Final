#!/usr/bin/env python
"""
The game field class and all its methods.

TODO
----

"""

# Authorship Information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

from Settings import *
from Agent import Agent
from Target import Target
import random


class GameField:
    """ The game field class and all its methods. Extended by the agent and target class.

        Attributes
        ----------
        agents : list
            The list of agents that are on the game field.
        targets : list
            The list of targets that are on the game field.
        mode : str
            The game mode that the game is to be played in.
        """
    def __init__(self, no_agents, no_targets_per_agent, mode):
        """ TODO still have to finish up this as well
        """
        # Creates the needed number of agents, and their targets
        self.agents = list()
        self.targets = list()
        for a_id in range(0, no_agents):

            self.agents.append(Agent(self, a_id, ))

    def generate_unique_location(self):
        """ Returns a random location on the gamefield that is unoccupied by any other object on the game field.

        TODO - make it loop through all of the agent locations

        """
        # Generates the random x and y variables
        x = random.randint(0, size_x)
        y = random.randint(0, size_y)
        location = (x, y)

        # Loops through the agents to make sure the location is unique to the agent
        for agent in self.agents:
            # If the location is already taken by one of the agent's,
            if agent.get_location() == location:
                return -1

