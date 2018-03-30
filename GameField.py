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
from Agent2 import Agent
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
        mode : GameMode
            The game mode that the game is to be played in.
        public_info : list
            The information that has been posted to the public channel
            The information will be in format (agent who sent, information)
        private_info : list
            The information that has been posted to the private channels
            The information will be in format (agent who sent, agent who is target, information)
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

        # Sets up the public and private information channels
        self.public_info = list()
        self.private_info = list()

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

    def post_to_channel(self, information, agent, target_agent=None):
        """ Adds information to a given channel.

        Parameters
        ----------
        information : list()
            The list of information to add to the given channel
        agent : Agent
            The agent that has sent the information
        target_agent : Agent
            The agent that the information is to be sent to in the case that the channel type is set to private.
            If the agent is set to None, then the information is posted to the public channel.
        """

        # Checks if an agent was given
        # No agent, public channel
        if target_agent is None:
            for info in information:
                self.public_info.append([agent, info])
        # Agent given, private channel
        else:
            for info in information:
                self.private_info.append([agent, target_agent, info])

    def get_from_channels(self, agent_requesting):
        """ Gets information pertaining to the agent from the public and private channels.

        Parameters
        ----------
        agent_requesting : Agent
            The agent that is requesting the information.  Used to determine which private channel information to send

        Returns
        -------
        info_to_send : list
            A list of information that is suppose to be sent to the agent

        """

        # Checks which information is important to the agent in the private_info list
        info_to_send = list()
        for info in self.private_info:
            if info[1] == agent_requesting:
                info_to_send.append(info)
                
        # Adds the public information to the info to send.
        info_to_send.extend(self.public_info)

        return info_to_send

    def clear_channels(self):
        """ Clears all of the information in the public and private channels.

        Returns
        -------
        info_deleted : list
            The list of information that was deleted from both of the channels
        """

        # Extend the public and private info channels into one temporary array to be returned
        deleted_info = self.public_info.extend(self.private_info)
        # Clear the channels
        self.public_info.clear()
        self.private_info.clear()

        return deleted_info
