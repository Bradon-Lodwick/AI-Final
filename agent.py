#!/usr/bin/env python
""" The file that holds the agent class and it's methods.
Setup of the agent uses the settings.py file to retrieve variables associated with the agent's speed, playing field
size, etc.

TODO
----
* Make agent's initial location unable to intersect with another agent's on class initialization
*

"""

# Authorship information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

import settings  # Stores global settings, such as speed of agents, number of targets, etc.
from game_object import GameObject
from target import Target  # Used to generate the agent's target
from game_field import GameField  # Used to simulate the sensors that the bot uses to interact with the environment


class Agent(GameObject):
    """ The agent used in the simulation.

    Attributes
    ----------
    speed : float
        The distance the agent can go per step.
    no_targets_total : int
        The number of targets the agent needs to find.
    targets_found : list
        The list of targets the agent has found that belong to it.
    targets_seen : list
        The list of targets the agent has found that belong to other agents.
    mode : int
        The mode the agent should be started in. Uses the Mode Enum class from settings.py.
    public_channel : bool
        Whether or not the agent can use the public channel to communicate with other agents.
    private_channel : bool
        Whether or not the agent can use the private channel to communicate with other agents.
    x : float
        The x-coordinate of the agent on the playing field.
    y : float
        The y-coordinate of the agent on the playing field.

    Raises
    ------
    ValueError
        Raised in the case the given mode is not able to be handled by the agent.

    """
    def __init__(self, mode, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        """ Constructor for the Agent class.

        Parameters
        ----------
        mode : Mode
            The mode the agent is to be created in.

        """

        # Declares the required variables for the agent to interact with the environment
        self.speed = settings.speed  # The speed at which the agent can move in the environment
        self.no_targets_total = settings.no_targets_per_agent  # The number of targets the agent is required to find
        self.targets_found = list()  # The list of targets the agent has found that belong to it
        self.targets_seen = list()  # The list of targets the agent has found that don't belong to it

        # Determines mode-related variables
        self.mode = mode
        if mode == settings.Mode.COMPETITION:  # Sets the agent up for competition mode
            self.public_channel = True  # Allows public channel communication
            self.private_channel = False  # Disallows private channel communication
        elif mode == settings.Mode.COLLABORATION:  # Sets the agent up for collaboration mode
            self.public_channel = True  # Allows public channel communication
            self.private_channel = True  # Allows private channel communication
        elif mode == settings.Mode.COMPASSIONATE:  # Sets the agent up for compassionate mode
            self.public_channel = True  # Allows public channel communication
            self.private_channel = True  # Allows private channel communication
        else:  # If a non-existent mode is given, throws an error
            raise ValueError('The given mode was not valid.', 'given mode = {}'.format(mode))

    def move_agent_random(self, dist):
        # print("\n{} location: {}".format(self.name, self.get_location()))
        # print("My field size is: {}x{}".format(self.field.width, self.field.length))
        for go in self.field.scan_radius(self, 10):
            # print("{0:<3}\t{1:<10}\t{2}".format(go.__class__.__name__, go.get_name(), go.get_location()))
            if go.__class__.__name__ == "Target" and go.agent == self:
                go.is_found()
        
        possible_directions = [settings.Direction.N, settings.Direction.E, settings.Direction.S, settings.Direction.W]

        if self.location[0] - dist < 0:
            possible_directions.remove(settings.Direction.W)

        if self.location[0] + dist > self.field.width:
            possible_directions.remove(settings.Direction.E)

        if self.location[1] - dist < 0:
            possible_directions.remove(settings.Direction.S)

        if self.location[1] + dist > self.field.length:
            possible_directions.remove(settings.Direction.N)

        self.move(random.choice(possible_directions), dist)

    def after_movement(self, game_field):
        """ Ran after the agent has moved. Updates the list of objects in it's radar, determines valid movement
        directions based on nearby agents/game field bounds, and deals with targets in it's radius.

        Parameters
        ----------
        game_field : GameField
            The game field that the agent is on.

        """

        # Scan the area to see what the agent can see
        vis_obj = game_field.scan_radius(self, settings.radius)

        # Loops through all of the objects to see if there are any agents
        for obj in vis_obj:
            # If the object is an agent
            if isinstance(obj, Agent):
                # Checks to see which direction the bot should be allowed to move in
                if self.get_location()[0] < obj.get_location()[0]:  # If self is further to the West
                    if self.get_location()[1] < obj.get_location()[1]:  # If self is further to the South
                        # TODO give self priority
                        pass
                    else:
                        # TODO give obj priority
                        pass
                else:  # If self is further to the East
                    if self.get_location()[1] < obj.get_location()[1]:  # If self is further to the South
                        # TODO give obj priority
                        pass
                    else:
                        # TODO give self priority
                        pass

            # If the object is a target
            elif isinstance(obj, Target):
                # Collects target if it is it's own target
                if obj.agent == self:
                    # Tells the target it is found so it can be removed from the game field
                    obj.is_found()
                    # Adds the target to the agent's target_found list
                    self.targets_found.append(obj)
                else:
                    # Store target in memory
                    self.targets_seen.append(obj)
