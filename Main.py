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
import threading
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

    terminal_read = []

    winner_list = list()

    # Runs the game in a never ending loop, breaks when win occurs
    while True:

        ag0 = game_field.agents[0]

       # for dest in ag0.destinations:
        #    terminal.printf(dest[0], dest[1], "{}".format(ag0.get_weight(dest, ag0.memory)))

        # Draws all of the targets
        for tar in game_field.targets:
            tar_location = tar.get_location()
            terminal.printf(tar_location[0], tar_location[1], "{}".format(tar.name))

        for i in range(size_x):
            for j in range(size_y):
                if ag0.memory[i][j] == 1:
                    terminal.printf(i,j,".")

        #-------AGENT STUFF----------
        # The agent threads list
        threads = []
        # Creates all of the agent threads
        for agent in game_field.agents:
            t = threading.Thread(target=agent_threading_function, args=(agent,))
            threads.append(t)
            #---IS WINNER?-------
            if agent.winner and agent not in winner_list:
                winner_list.append(agent)

        # Starts all of the threads
        for t in threads:
            t.start()
        # Waits for all the agent threads to finish
        for t in threads:
            t.join()

        for i in range(len(winner_list)):
            terminal.printf(0, i * 2, "Winner: {}".format(winner_list[i].g_id))

        #-----BREAK TO WIN SEQUENCE--

        #----REFRESH TERMINAL--------
        time.sleep(refresh)
        terminal.refresh()
        terminal.clear()

    #-----WIN SEQUENCE
    if terminal_read() != terminal.TK_CLOSE:
        terminal.close()


def agent_threading_function(agent):
    # Prints out the agents to the terminal
    for i in range(21):
        for j in range(21):
            if agent.body[j + i * 21] != ' ':
                if (agent.body[j + i * 21] != '.'):
                    terminal.printf(agent.drawing_location[0] + j, agent.drawing_location[1] + i, agent.body[j + i * 21])

    agent.memorize()
    try:
        terminal.printf(agent.goal[0]-1, agent.goal[1], "({})".format(agent.g_id))
    except:
        pass

    # Steps current agent
    agent.step()


play_game(GameModes.COOPERATIVE)
