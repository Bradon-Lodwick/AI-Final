#!/usr/bin/env python
"""
The agent class and all its methods.

TODO
----

"""

# Authorship Information
__author__ = "Bradon Lodwick, Reid Butson, Thomas Reis"
__version__ = "0.1"
__status__ = "Prototype"

from GameObject import GameObject
from Target import Target
from Settings import *
from math import inf
import numpy as np
import random


class Agent(GameObject):
    """ The agent class and all its methods. Extended by the agent and target class.

        Attributes
        ----------
        game_field : GameField
            The game field that the object is on.
        g_id : int
            The id of the game object.
        location : list
            The location of the object on the game field.
        targets_collected : list
            The list of targets that the agent has found for itself.
        other_targets_found : list
            The list of targets that the agent has found for other agents.
        movement_mode : MoveMode
            The movement mode that the object is in
        memory : np.Array
        """

    def __init__(self, game_field, g_id, location):
        """ TODO add a list for targets known but not collected
            TODO add a value to store previous movement direction to allow collision avoidance to force right turns
        """
        GameObject.__init__(self, game_field, g_id, location)
        print("yes hello I am agent {}".format(self.g_id))
        # Creates the empty lists for the targets the agent has found
        self.targets_collected = list()
        self.self_targets_found = list()
        self.other_targets_found = list()
        self.destinations = []
        # Initializes the agent's movement to the exploration mode
        self.movement_mode = MoveModes.EXPLORE
        # Initializes the memory of the map that the agent has seen
        self.direct = None
        self.memory = np.ones(shape=(size_x, size_y))
        self.drawing_location = [self.location[0] - 10, self.location[1] - 10]
        self.winner = False
        self.run_away = False
        self.last_collision = 1
        self.goal = []
        self.body = \
            "      +++++++++      " \
            "    ++.........++    " \
            "   +.............+   " \
            "  +...............+  " \
            " +.................+ " \
            " +.................+ " \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            "+.........{}.........+" \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            "+...................+" \
            " +.................+ " \
            " +.................+ " \
            "  +...............+  " \
            "   +.............+   " \
            "    ++.........++    " \
            "      +++++++++      ".format(self.g_id)

        self.add_sub_locations()

    def add_sub_locations(self):
        for i in range(int(size_x/10)):
            for j in range(int(size_y/10)):
                self.destinations.append([i*10+5, j*10+5])

    def distance_from_self(self, coord):
        distance = abs(coord[0] - self.location[0]) + abs(coord[1] - self.location[1])
        return distance

    def step(self):
        # TODO Collect steps when running away
        self.get_info()
        in_area = self.scan_area()

        if len(in_area) > 0 and not self.run_away:
            self.run_away = True
            self.goal = self.escape_zone(in_area)

        elif not self.run_away and len(self.destinations) != 0:
            for dest in self.destinations:
                if self.get_weight(dest, self.memory) == 0:
                    self.destinations.remove(dest)
            if len(self.destinations) != 0:
                self.destinations.sort(key=lambda x: (self.distance_from_self(x), -self.get_weight(x, self.memory)))
                # Only set the goal if the agent is in exploration mode
                if self.movement_mode == MoveModes.EXPLORE:
                    self.goal = self.destinations[0]

        if self.location[0] < self.goal[0]:
            self.direct = 1
        elif self.location[0] > self.goal[0]:
            self.direct = 3
        elif self.location[1] < self.goal[1]:
            self.direct = 2
        elif self.location[1] > self.goal[1]:
            self.direct = 0

        # If goal is reached and agent is not running away from other agents
        if self.location[0] == self.goal[0] and self.location[1] == self.goal[1] and not self.run_away:
            # Checks to see which movement mode it is in
            # Exploration mode
            if self.movement_mode == MoveModes.EXPLORE:
                if len(self.destinations) != 0:
                    self.goal = self.destinations.pop(0)
            # Pathfinding mode
            if self.movement_mode == MoveModes.PATHFIND:
                # Set the new closest target to be the goal
                self.goal = self.find_closest_target(self.self_targets_found, self.location)

        if self.location[0] == self.goal[0] and self.location[1] == self.goal[1] and self.run_away:
            self.run_away = False

        if self.check_move(self.direct) and (len(self.destinations) != 0 or self.run_away):
            self.move(self.direct)

        elif len(self.destinations) != 0:
            self.goal = self.destinations[0]

        # Checks which game mode it is in to determine how it should communicate
        if self.game_field.mode == GameModes.COMPETITIVE:
            # Currently no communication is done in competitive, but eventually trading targets based on happiness
            # could be added
            pass
        elif self.game_field.mode == GameModes.COMPASSIONATE:
            # Shares memory to public channel
            self.post_info(self.memory)
            # Share target information to the other agent
            for target in self.other_targets_found:
                self.post_info(target, target=target.owner)
                self.other_targets_found.remove(target)
        elif self.game_field.mode == GameModes.COOPERATIVE:
            # Shares memory to public channel
            self.post_info(self.memory)
            # Share target information to the other agent
            for target in self.other_targets_found:
                self.post_info(target, target=target.owner)
                self.other_targets_found.remove(target)

    def escape_zone(self, enemies, factor=1):
        # TODO add jitter
        num_e = len(enemies)
        avg_x, avg_y = 0, 0
        for e in enemies:
            avg_x += int(e.location[0]/num_e)
            avg_y += int(e.location[1]/num_e)

        escape_destination = [factor*(2*self.location[0] - avg_x), factor*(2*self.location[1] - avg_y)]
        return escape_destination

    def move(self, direction):
        if direction == 0:
            self.location[1] -= speed
        elif direction == 2:
            self.location[1] += speed
        elif direction == 1:
            self.location[0] += speed
        elif direction == 3:
            self.location[0] -= speed
        self.drawing_location = [self.location[0]-10, self.location[1]-10]

    def check_move(self, direction):
        # TODO return approved coordinates
        if direction == 1 and self.location[0] + speed < 100:
            return True
        elif direction == 2 and self.location[1] + speed < 100:
            return True
        elif direction == 3 and self.location[0] - speed > 0:
            return True
        elif direction == 0 and self.location[1] - speed > 0:
            return True
        else:
            return False

    @staticmethod
    def get_weight(coord, mat):
        weight = 0
        for i in range(coord[0]-5, coord[0]+5):
            for j in range(coord[1]-5, coord[1]+5):
                if 0 <= j < 100 and 0 <= i < 100:
                    weight += mat[i][j]
        return weight

    def scan_area(self):
        """ Scans the area for game objects, updating its memory as it finds targets. Returns whether an agent is within
        its radar
        """
        nearby = self.game_field.scan_radius(self)
        found_agent = []
        for obj in nearby:
            if isinstance(obj, Agent):
                # is another agent
                found_agent.append(obj)
            # is a target that belongs to the agent and belongs to the agent
            if isinstance(obj, Target) and obj.owner == self and not obj.collected:
                # Checks if target was in the self_targets_found list to remove if nescessary
                if obj in self.self_targets_found:
                    self.self_targets_found.remove(obj)

                # Collects the target
                self.targets_collected.append(obj)
                obj.collect()

                if len(self.targets_collected) == no_targets_per_agent:
                    print("Agent {} collected all of its targets".format(self.g_id))
                    self.winner = True

            elif isinstance(obj, Target) and obj.owner != self and (obj not in self.other_targets_found):
                # is a target that belongs to another agent
                self.other_targets_found.append(obj)

        return found_agent

    def memorize(self):
        for i in range(21):
            for j in range(21):
                try:
                    if 0 <= self.drawing_location[0] + j < 100 and 0 <= self.drawing_location[1] + i < 100:
                        if self.body[j + i * 21] != ' ':
                            self.memory[self.drawing_location[0] + j, self.drawing_location[1] + i] = 0
                except IndexError:
                    pass

    def post_info(self, information, target=None):
        """ Post information to the public channel. Will be stored in the game field.

        Parameters
        ----------
        information : list()
            The list of information to be sent to the public channel.
        target : Agent
            The agent to send to in case private communication is desired. None if public desired.

        """

        # Posts the information to game_field
        self.game_field.post_to_channel(information, self, target)

    def get_info(self):
        """ Retrieves information from the game field, from both private and public channels, and processes it.
        """

        # Gets the info from the game field
        information_list = self.game_field.get_from_channels(self)

        # Loops through all of the information that was sent by the game field
        for single_info_list in information_list:
            # If the info was from a private channel, set all variables
            if len(single_info_list) == 3:
                agent_sent = single_info_list[0]
                info = single_info_list[2]
            # If the info was sent on public channel, set all variables
            else:
                agent_sent = single_info_list[0]
                info = single_info_list[1]

            # Deal with each type of information differently
            # Memory information
            if isinstance(info, np.ndarray):
                # Multiplies the new memory with its own, so it doesn't go and check areas that the given information
                # already said was covered
                self.memory *= info

            # Target information
            elif isinstance(info, Target):
                # Adds the target to the necessary target memory based on its owner
                # If target belongs to this agent
                if info.owner == self and info not in self.targets_collected and info not in self.self_targets_found:
                    # TODO After merging, this needs to be changed so that it appends to the proper target list
                    self.self_targets_found.append(info)
                # If target belongs to another agent
                elif info.owner != self and info not in self.other_targets_found:
                    self.other_targets_found.append(info)
            # Agent information
            elif isinstance(info, Agent):
                # Currently only a pass, as it doesn't do anything with information about where an agent is, but is
                # here in case it is needed in the future
                pass

    def evaluate_move_mode(self):
        """ Evaluates which movement mode the agent should be in by checking how many targets the agent has locations
        for and how many it has collected.

        Returns
        -------
        self.movement_mode : MoveModes
            The movement mode the agent has been set to.
        """

        # If the agent doesn't know all target locations, continue exploration mode
        if len(self.targets_collected) + len(self.self_targets_found) < no_targets_per_agent:
            self.movement_mode = MoveModes.EXPLORE
        # If the agent knows where all the remaining targets to be collected are
        elif len(self.targets_collected) + len(self.self_targets_found) == no_targets_per_agent:
            self.movement_mode = MoveModes.PATHFIND
        # If it reaches this state, then an error has occurred when assigning the agent's target memory
        else:
            raise RuntimeError("The number of targets in agent {0}'s targets found and collected memory acceeds "
                               "total targets\ntargets_collected={1}\ntargets_found={2}".
                               format(self.g_id, len(self.targets_collected), len(self.self_targets_found)))

    def find_closest_target(self, targets, start):
        """ Finds the closest node to a given starting location in a given list of targets.

        Parameters
        ----------
        targets : list
            The list of targets to calculate the shortest path between.
        start : list
            The x, y coordinates of the start position.

        Returns
        -------
        best_target: Target
            The target that is closest to the given location.
        """

        # The best target so far
        best_target = None
        best_distance = inf
        # Iterate through all targets to determine closest one
        for target in targets:
            current_distance = self.calculate_manhattan_distance(self.location, target.location)
            # If current_distance is smaller than the best_distance, set the current target to be best
            if current_distance < best_distance:
                best_distance = current_distance
                best_target = target

        return best_target

    def move_to_target(self, target):
        """ Moves the agent towards the given target.

        Parameters
        ----------
        target : Target
            The target the agent is to move towards.
        """

    @staticmethod
    def calculate_manhattan_distance(location1, location2):
        """ Calculates the manhattan distance between the 2 given locations.

        Parameters
        ----------
        location1 : list
            The first location in x, y format.
        location2 : list
            The second location in x, y format.

        Returns
        -------
        Returns the manhattan distance between the targets.
        """

        return abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])
