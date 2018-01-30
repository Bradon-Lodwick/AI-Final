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


class Target:
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

    def __init__(self, agent, number):
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

        # Determines the location of the bot on the playing field using rng
        # TODO make the target unable to intersect with other targets on initialization
        self.x = random.uniform(0, settings.length)
        self.y = random.uniform(0, settings.width)

        # Initialize the found variable to False
        self.found = False
