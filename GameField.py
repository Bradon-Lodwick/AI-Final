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
import numpy as np
import random


class GameField:
    """ The game field class and all its methods. Extended by the agent and target class.

        Attributes
        ----------
        agents : list
            The list of agents that are on the game field.
        targets : list
            The list of targets that are on the game field.
        object_list : list
            The list of all targets and agents on the game field.
        mode : str
            The game mode that the game is to be played in.
        """
    def __init__(self, no_agents, no_targets_per_agent, mode):
        """ TODO still have to finish up this as well
        """
        # Creates the agent and target lists
        self.agents = list()
        self.targets = list()

        # Loops to create the necessary number of agents
        for a_id in range(0, no_agents):
            location = self.generate_unique_location()
            new_agent = Agent(self, a_id, location)
            self.agents.append(new_agent)

            # Adds all the targets for the newly generated agent
            for t_id in range(0, no_targets_per_agent):
                location = self.generate_location()
                new_target = Target(self, t_id, location, new_agent)
                self.targets.append(new_target)

        # Sets the game mode of the game field
        self.object_list = self.agents + self.targets
        self.mode = mode

    def scan_radius(self, agent):
        origin = (agent.location[0], agent.location[1])
        surroundings = []

        for obj in self.object_list:
            if obj != agent:
                loc = (obj.location[0], obj.location[1])
                distance = np.sqrt((loc[0] - origin[0]) ** 2 + (loc[1] - origin[1]) ** 2)

                if distance <= radar_radius:
                    surroundings.append(obj)

        return surroundings

    # Debug Function to return all targets belonging to the given agent
    def ReturnAllTargets(self, agent):
        targets=[]
        for obj in self.object_list:
            if obj != agent:
                if (isinstance(obj,Target) and obj.owner == agent):
                    targets.append(obj)
        return targets

    def generate_unique_location(self):
        """ Returns a random location on the game field that is unoccupied by any other object on the game field.

        Returns
        -------
        location : list
            The unique location that was found in (x, y) format
        """

        # Value used to exit the loop
        loc_found = False
        location = list()
        while not loc_found:
            # Generates the random x and y variables
            x = random.randint(1, size_x)
            y = random.randint(1, size_y)
            location = [x, y]

            # Loops through the agents to make sure the location is unique to the agent
            loc_found_temp = True
            for agent in self.agents:
                # If the location is already taken by one of the agent's
                if agent.get_location() == location:
                    loc_found_temp = False
                    break
            # Set the location found value to the temporary value
            loc_found = loc_found_temp

        # Return the unique location that was found
        return location

    @staticmethod
    def generate_location():
        """ Returns a random location on the field.

        Returns
        -------
        location : list
            The random location in (x, y) format.
        """
        # Generates the random x and y variables
        x = random.randint(1, size_x)
        y = random.randint(1, size_y)
        location = [x, y]
        return location
