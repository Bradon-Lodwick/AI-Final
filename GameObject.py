#!/usr/bin/env python
"""
The game object class and all its methods. Extended by the agent and target class.

TODO
----

"""

# Authorship Information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"


class GameObject:
    """ The game object class and all its methods. Extended by the agent and target class.

    Attributes
    ----------
    game_field : GameField
        The game field that the object is on.
    g_id : int
        The id of the game object.
    location : list
        The location of the object on the game field.
    """

    def __init__(self, game_field, g_id, location):
        """ Initializes the game object.

        Parameters
        ----------
        game_field : GameField
            The game field that the object is on.
        g_id : int
            The id of the game object.
        location : list
            The location of the object on the game field.
        """

        self.game_field = game_field
        self.g_id = g_id
        self.location = location

    def get_game_field(self):
        """ Gets the game field that the object is on.

        Returns
        -------
        GameField : Returns the game field of the object.
        """

        return self.game_field

    def set_game_field(self, game_field):
        """ Sets the game field that the object is on.

        Parameters
        ----------
        game_field : GameField
            The game field that the object is to be put on

        Returns
        -------
        GameField : Returns the game field of the object after reassignment.
        """

        self.game_field = game_field
        return self.game_field

    def get_id(self):
        """ Gets the id of the object.

        Returns
        -------
        int : Returns the id of the object.
        """

        return self.g_id

    def set_id(self, g_id):
        """ Sets the id of the object.

        Parameters
        ----------
        g_id : int
            The new id of the object.

        Returns
        -------
        int : Returns the id of the object after reassignment.
        """

        self.g_id = g_id
        return self.g_id

    def get_location(self):
        """ Gets the id of the object.

        Returns
        -------
        int : Returns the id of the object.
        """

        return self.location

    def set_location(self, location):
        """ Sets the id of the object.

        Parameters
        ----------
        location : list
            The new location to have the object set to.

        Returns
        -------
        int : Returns the id of the object after reassignment.
        """

        self.location = location
        return self.location
