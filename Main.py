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

import time
from GameField import GameField
from bearlibterminal import terminal
from Settings import *


def play_game(mode):
    """ The main method of the game.  Creates the game field and all game objects, as defined in Settings.py, and
    runs the game until the win condition occurs.

    Parameters
    ----------
    game_mode : GameModes
        The game mode that the game is to be played in.
    """

    game_field = GameField(no_agents, no_targets_per_agent, mode)
    terminal.open()
    terminal.set("window: size={}x{}, cellsize=8x8".format(size_x, size_y))

    winner_list = list()

    # Runs the game in a never ending loop, breaks when win occurs
    while True:
        # Draws all of the targets
        for tar in game_field.targets:
            tar_location = tar.get_location()
            terminal.printf(tar_location[0], tar_location[1], "{}".format(tar.name))

        #-------AGENT STUFF----------
        for agent in game_field.agents:
            # Prints out the agents to the terminal
            for i in range(21):
                for j in range(21):
                    if agent.body[j + i * 21] != ' ':
                        if (agent.body[j + i * 21] != '.'):
                            terminal.printf(agent.drawing_location[0] + j, agent.drawing_location[1] + i, agent.body[j + i * 21])
                        try:
                            agent.memory[agent.drawing_location[0] + j, agent.drawing_location[1] + i] = 0
                        except IndexError:
                            pass

            # Steps current agent
            agent.step()
            #---IS WINNER?-------
            if agent.winner:
                winner_list.append(agent)

        for i in range(len(winner_list)):
            terminal.printf(0, i * 2, "Winner: {}".format(winner_list[i].name))

        #-----BREAK TO WIN SEQUENCE--

        #----REFRESH TERMINAL--------
        time.sleep(refresh)
        terminal.refresh()
        terminal.clear()

    #-----WIN SEQUENCE


play_game(GameModes.COMPETITIVE)
