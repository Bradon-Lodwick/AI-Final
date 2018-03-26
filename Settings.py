from enum import Enum


# The size of the gamefield
size_x = 100
size_y = 100


class MoveModes(Enum):
    """ Modes that the agent can be in for movement.
    """
    EXPLORE = 'explore'
    PATHFIND = 'pathfind'

class GameModes(Enum):
    """ Modes that the simulation can be in for game play.
    """
    COMPETITIVE = 'competitive'
    COMPASSIONATE = 'compassionate'
    COOPERATIVE = 'cooperative'

