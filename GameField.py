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