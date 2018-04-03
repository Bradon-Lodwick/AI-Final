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
from Util import *
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
    data = list()
    for mode in modes:
        for i in range(0, no_games_per_mode):
            data.extend(play_game(mode, i+1))
    return data


def play_game(mode, run_no=1):
    """ The main method of the game.  Creates the game field and all game objects, as defined in Settings.py, and
    runs the game until the win condition occurs.

    Parameters
    ----------
    mode : GameModes
        The game mode that the game is to be played in.
    run_no : int
        The run number of the game.
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

        time_s = time.time()

        ag0 = game_field.agents[0]

        # Draws all of the targets on the terminal
        for tar in game_field.targets:

            if tar.collected:
                colour = "#a0a0a0"
            elif tar.owner.movement_mode == MoveModes.PATHFIND:
                colour = "#00ff00"
            else:
                colour = "#ffffff"
            tar_location = tar.get_location()
            terminal.printf(tar_location[0], tar_location[1], "[color={}]{}[/color]".format(colour, tar.name))

        for i in range(size_x):
            for j in range(size_y):
                if ag0.memory[i][j] == 1:
                    terminal.printf(i, j, "[color=white].[/color]")

        # un-comment for destination weights to be printed
        '''
        for dest in ag0.destinations:
            mem = ag0.get_weight(dest, ag0.memory)
            terminal.printf(dest[0], dest[1], "{}".format(mem))
        '''

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

        # Clear the game_field's channels
        game_field.clear_channels()

        # Prints to the terminal which agents finished collecting their targets
        for i in range(len(finished_agents)):
            terminal.printf(0, i * 2, "Agent {} done".format(finished_agents[i].g_id))

        # Refresh the terminal
        while(time.time() - time_s < refresh):
            pass
        terminal.refresh()
        terminal.clear()

        # Check for the win condition
        game_complete = game_field.check_win_condition()
        if game_complete:
            print ("\n \n \n \n")

    # Get happiness
    return game_field.get_agent_happinesses(run_no)


def print_agent(agent):
    """ Prints the given agent on the terminal window.

    Parameters
    ----------
    agent : Agent
        The agent to print to the terminal.
    """

    # Chooses colour based on agent state, e.g. running away

    if agent.run_away:
        colour = "#ff0000"
    elif agent.movement_mode == MoveModes.PATHFIND:
        colour = "#00ff00"
    else:
        colour = "#ffffff"

    for i in range(21):
        for j in range(21):
            if agent.body[j + i * 21] != ' ':
                if agent.body[j + i * 21] != '.':
                    terminal.printf(
                        agent.drawing_location[0] + j, agent.drawing_location[1] + i, "[color={}]{}[/color]".format(colour, agent.body[j + i * 21]))
    try:
        terminal.printf(agent.goal[0]-1, agent.goal[1], "[color={}]({})[color]".format(colour, agent.g_id))
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
csvData = play_games(no_iterations, [GameModes.COMPASSIONATE, GameModes.COMPETITIVE, GameModes.COOPERATIVE])

add_to_csv(csvData)
add_to_csv2(csvData)

#adds to the second csv file, once for each game mode
#add_to_csv2(1,,)
#add_to_csv2(2,,)
#add_to_csv2(2,,)
