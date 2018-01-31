#!/usr/bin/env python
""" The file that holds the target class and it's methods.
Setup of the target uses the settings.py file to retrieve variables associated with the playing field size,
number of targets, etc.

TODO
----
* Make target's initial location unable to intersect with another target's on class initialization

"""

# Authorship information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

import settings  # Stores global settings, such as speed of agents, number of targets, etc.
import random  # Used to place the agent on a random point on the playing field
from game_object import GameObject


class Target(GameObject):
    """ A target that the agent is tasked with finding.

    Attributes
    ----------
    agent : Agent
        The agent that the target belongs to.
    number : int
        The target id number. For example, if an agent needs to find 5 targets, this value will be between 1-5.
    found : bool
        Whether the target has been found by it's agent.

    """
    # Initialize the found variable to False
    found = False

    # TODO fix duplicates between GameObject and Target, make more compatible
    def __init__(self, agent, number, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        """ Constructor for the Target class.

        Parameters
        ----------
        agent : Agent
            The agent that the target belongs to.
        number : int
            The target id number. For example, if an agent needs to find 5 targets, this value will be between 1-5.

        """

        # Set the required parameters for the class
        self.agent = agent  # The agent the target belongs to
        self.number = number  # The id number of the target

    def is_found(self):
        self.found = True
        print("Agent {} has found {}!".format(self.agent.name, self.name))
        self.field.remove_object(self)
