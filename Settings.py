from enum import Enum


# GAME FIELD SETTINGS
# The size of the game field
size_x = 100
size_y = 100
# The number of agents on the game field
no_agents = 5
# The number of targets for each agent
no_targets_per_agent = 5

# TERMINAL SETTINGS
# The refresh rate of the terminal
refresh = 0.05

# AGENT SETTINGS
# Speed of the agents
speed = 1
# Radar range of the agents
radar_radius = 10


class MoveModes(Enum):
    """ Modes that the agent can be in for movement.
    """
    EXPLORE = 1
    PATHFIND = 2
    STOP = 3


class GameModes(Enum):
    """ Modes that the simulation can be in for game play.
    """
    COMPETITIVE = 1
    COMPASSIONATE = 2
    COOPERATIVE = 3


class Direction(Enum):
    """ The valid directions that an agent can move in.
    """
    N = 1
    E = 2
    S = 3
    W = 4
