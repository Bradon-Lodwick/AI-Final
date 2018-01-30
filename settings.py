#!/usr/bin/env python
""" This file holds all settings variables that affect the simulation.

Important Notes
---------------
* All measurements of distance will be in metres
* All measurements of time will be in the arbitrary "steps" unit
* Speed, therefore, is in a measurement of metres/step

TODO
----
*

"""

# Authorship information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

from enum import Enum  # Used to create enumerations

# Playing field settings
width = 10.0  # The width of the playing field
length = 10.0  # The length of the playing field
no_agents = 5  # The number of agents to be used in the simulation
no_targets_per_agent = 5  # The number of targets for each agent to use


class Mode(Enum):
    """ Enumeration for the desired mode to be used when running the simulation.

    """

    COMPETITION = 1  # Value to be used for competition mode
    COLLABORATION = 2  # Value to be used for collaboration mode
    COMPASSIONATE = 3  # Value to be used for compassionate mode


# Agent settings
speed = 0.01  # The speed at which the agent moves, in metres/step
