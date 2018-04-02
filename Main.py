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


def play_games(no_games_per_mode, modes):
    """ Runs the given number of games for each mode.

    Parameters
    ----------
    no_games_per_mode : int
        The number of games to be played for each given mode.
    modes : list
        The list of GameModes to run.
    """
    for mode in modes:
        for i in range(0, no_games_per_mode):
            play_game(mode)


def play_game(mode):
    """ The main method of the game.  Creates the game field and all game objects, as defined in Settings.py, and
    runs the game until the win condition occurs.

    Parameters
    ----------
    mode : GameModes
        The game mode that the game is to be played in.
    """

    # Set up the game_field object, as well as the agents when the game field is created.
    game_field = GameField(no_agents, no_targets_per_agent, mode)

    # Set up the terminal to be used for output
    terminal.open()
    terminal.set("window: size={}x{}, cellsize=8x8".format(size_x, size_y))

    # The list of agents that have found all of their targets
    finished_agents = list()

    # Boolean that controls whether the game has been completed or not
    game_complete = False

    # Runs the game until game_complete is set to True
    while not game_complete:
        # The first agent in the game_field's list, to be used when showing memory values on the terminal

        ag0 = game_field.agents[0]

        # Draws all of the targets on the terminal
        for tar in game_field.targets:
            tar_location = tar.get_location()
            terminal.printf(tar_location[0], tar_location[1], "{}".format(tar.name))
        for i in range(size_x):
            for j in range(size_y):
                if ag0.memory[i][j] == 1:
                    terminal.printf(i, j, ".")

        # Starts the threading for the agents
        # The agent threads list
        threads = []
        # Creates all of the agent threads
        for agent in game_field.agents:
            t = threading.Thread(target=agent_threading_function, args=(agent,))
            threads.append(t)
            # Adds the agent to the finished_agents list if all of its targets were found
            if agent.all_targets_collected and agent not in finished_agents:
                finished_agents.append(agent)
        # Starts all of the threads
        for t in threads:
            t.start()
        # Waits for all the agent threads to finish
        for t in threads:
            t.join()

        # Prints to the terminal which agents finished collecting their targets
        for i in range(len(finished_agents)):
            terminal.printf(0, i * 2, "Agent {} done".format(finished_agents[i].g_id))

        # Refresh the terminal
        time.sleep(refresh)
        terminal.refresh()
        terminal.clear()

        # Check for the win condition
        game_complete = game_field.check_win_condition()

    # TODO still errors in the way this prints to the console
    # Output game winner information to the terminal based on game mode
    if game_field.mode == GameModes.COMPETITIVE or game_field.mode == GameModes.COMPASSIONATE:
        agent_string = ''
        for agent in finished_agents:
            if agent_string == '':
                agent_string += '{}'.format(agent.g_id)
            else:
                agent_string += ', {}'.format(agent.g_id)
        if game_field.mode == GameModes.COMPETITIVE:
            terminal.printf(0, 0, "Agent(s) {} won!".format(agent_string))
        elif game_field.mode == GameModes.COMPASSIONATE:
            terminal.printf(0, 0, "Agent(s) {} found all their targets!".format(finished_agents))
    elif game_field.mode == GameModes.COOPERATIVE:
        terminal.printf(0, 0, "All agents found their targets!")

    # Refresh the terminal
    terminal.refresh()

    # Stops terminal from closing when game is complete
    if terminal.read() != terminal.TK_CLOSE:
        terminal.close()


def print_agent(agent):
    """ Prints the given agent on the terminal window.

    Parameters
    ----------
    agent : Agent
        The agent to print to the terminal.
    """
    for i in range(21):
        for j in range(21):
            if agent.body[j + i * 21] != ' ':
                if agent.body[j + i * 21] != '.':
                    terminal.printf(
                        agent.drawing_location[0] + j, agent.drawing_location[1] + i, agent.body[j + i * 21])
    try:
        terminal.printf(agent.goal[0]-1, agent.goal[1], "({})".format(agent.g_id))
    # TODO this should be changed to a less broad exception class, what exception are we expecting this to cause?
    except Exception:
        pass


def agent_threading_function(agent):
    """ The function used to run the agent steps in threads, to allow the agents to run asynchronously.

    Parameters
    ----------
    agent : Agent
        The agent to have move a step.
    """

    # Step the agent
    agent.step()

    # Print the agent
    print_agent(agent)


# play_game(GameModes.COMPASSIONATE)
play_games(1, [GameModes.COMPASSIONATE, GameModes.COMPETITIVE, GameModes.COOPERATIVE])
