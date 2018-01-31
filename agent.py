#!/usr/bin/env python
""" The file that holds the agent class and it's methods.
Setup of the agent uses the settings.py file to retrieve variables associated with the agent's speed, playing field
size, etc.

TODO
----
* Make agent's initial location unable to intersect with another agent's on class initialization
* Generate the needed number of targets for the agent
* Target list makes more sense to be outside of the agent class, as it shouldn't really be able to access the targets
outside of locating them

"""

# Authorship information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

import settings  # Stores global settings, such as speed of agents, number of targets, etc.
import random  # Used to place the agent on a random point on the playing field
from game_object import GameObject
from target import Target  # Used to generate the agent's target


class Agent(GameObject):
    """ The agent used in the simulation.

    Attributes
    ----------
    speed : float
        The distance the agent can go per step.
    no_targets_total : int
        The number of targets the agent needs to find.
    no_targets_found : int
        The number of targets the agent has found.
    mode : int
        The mode the agent should be started in. Uses the Mode Enum class from settings.py.
    public_channel : bool
        Whether or not the agent can use the public channel to communicate with other agents.
    private_channel : bool
        Whether or not the agent can use the private channel to communicate with other agents.
    x : float
        The x-coordinate of the agent on the playing field.
    y : float
        The y-coordinate of the agent on the playing field.

    Raises
    ------
    ValueError
        Raised in the case the given mode is not able to be handled by the agent.

    """
    # TODO implement Agent in a more GameObjectifying way
    def __init__(self, mode, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        """ Constructor for the Agent class.

        Parameters
        ----------
        mode : Mode
            The mode the agent is to be created in.

        """

        # Declares the required variables for the agent to interact with the environment
        self.speed = settings.speed  # The speed at which the agent can move in the environment
        self.no_targets_total = settings.no_targets_per_agent  # The number of targets the agent is required to find
        self.no_targets_found = 0  # The number of targets the agent has found

        # Determines mode-related variables
        self.mode = mode
        if mode == settings.Mode.COMPETITION:  # Sets the agent up for competition mode
            self.public_channel = True  # Allows public channel communication
            self.private_channel = False  # Disallows private channel communication
        elif mode == settings.Mode.COLLABORATION:  # Sets the agent up for collaboration mode
            self.public_channel = True  # Allows public channel communication
            self.private_channel = True  # Allows private channel communication
        elif mode == settings.Mode.COMPASSIONATE:  # Sets the agent up for compassionate mode
            self.public_channel = True  # Allows public channel communication
            self.private_channel = True  # Allows private channel communication
        else:  # If a non-existent mode is given, throws an error
            raise ValueError('The given mode was not valid.', 'given mode = {}'.format(mode))

        # Determines the location of the bot on the playing field using rng
        # TODO make the agent unable to intersect with other agents on initialization

        # The list of targets belonging to the agent
#        targets = list()
        # Creates the targets for the agent
#        for i in range(0, self.no_targets_total):
            # Create a target with the id number of i
#            targets.append(Target(self, i))
        # TODO send the targets somewhere else, doesn't make sense to have them in the thing looking for it. '''
