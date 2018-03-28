#!/usr/bin/env python
"""
The target class and all its methods.

TODO
----

"""

# Authorship Information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

from GameObject import GameObject


class Target(GameObject):
    """ The target class and all its methods. Extended by the agent and target class.

        Attributes
        ----------
        game_field : GameField
            The game field that the object is on.
        g_id : int
            The id of the game object.
        location : list
            The location of the object on the game field.
        owner : Agent
            The agent that owns the target
        """

    def __init__(self, game_field, g_id, location, owner):
        GameObject.__init__(self, game_field, g_id, location)
        self.owner = owner
        self.name = "{} - {}".format(owner.g_id, g_id)
        self.collected = False

    def collect(self):
        self.collected = True

    def get_owner(self):
        """ Gets the owner of the agent.

        Returns
        -------
        Returns the owner of the agent.
        """

        return self.owner

    def set_owner(self, owner):
        """ Sets the owner of the agent.

        Parameters
        ----------
        owner : Agent
            The agent to have the owner set to.

        Returns
        -------
        Returns the owner after reassignment
        """

        self.owner = owner
        return owner
