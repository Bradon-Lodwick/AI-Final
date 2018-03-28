#!/usr/bin/env python
"""
The main method that runs the game event loop.

TODO
----

"""

# Authorship Information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

import GameField
from bearlibterminal import terminal
from Settings import *

def print_agent(terminal, agent):
    """

    :param terminal:
    :param agent:
    :return:
    """

    for i in range(21):
        for j in range(21):
            if agent.body[j + i * 21] != ' ':
                terminal.printf(agent.loc_x + j, agent.loc_y + i, agent.body[j + i * 21])

def play_game(game_mode):
    """ The main method of the game.  Creates the game field and all game objects, as defined in Settings.py, and
    runs the game until the win condition occurs.

    Parameters
    ----------
    game_mode : GameModes
        The game mode that the game is to be played in.
    """

    game_field = GameField(no_agents, no_targets_per_agent, game_mode.COMPETITIVE)
    terminal.open()
    terminal.set("window: size={}x{}, cellsize=8x8".format(size_x, size_y))

    # Runs the game in a never ending loop, breaks when win occurs
    while True:
        # Draws all of the targets
        for tar in game_field.targets:
            tar_location = tar.get_location()
            terminal.printf(tar_location[0], tar_location[1], tar.get_id())

        #-------AGENT STUFF----------
        for agent in game_field.agents:

            #------DRAW AGENT--------
            #------MOVE AGENT--------
                #---IS WINNER?-------

        #-----BREAK TO WIN SEQUENCE--

        #----REFRESH TERMINAL--------

    #-----WIN SEQUENCE
