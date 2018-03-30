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
        self_targets_found : list
            The list of targets that the agent has found for itself.
        other_targets_found : list
            The list of targets that the agent has found for other agents.
        movement_mode : char
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
        in_area = self.scanArea()

        if len(in_area) > 0:
            self.run_away = True
            self.goal = self.escape_zone(in_area)

        elif not self.run_away and len(self.destinations) != 0:
            for dest in self.destinations:
                if self.get_weight(dest, self.memory) == 0:
                    self.destinations.remove(dest)
            if len(self.destinations) != 0:
                self.destinations.sort(key=lambda x: (self.distance_from_self(x), -self.get_weight(x, self.memory)))
                self.goal = self.destinations[0]

        if self.location[0] < self.goal[0]:
            self.direct = 1
        elif self.location[0] > self.goal[0]:
            self.direct = 3
        elif self.location[1] < self.goal[1]:
            self.direct = 2
        elif self.location[1] > self.goal[1]:
            self.direct = 0

        if self.location[0] == self.goal[0] and self.location[1] == self.goal[1] and not self.run_away:
            if len(self.destinations) != 0:
                self.goal = self.destinations.pop(0)

        if self.location[0] == self.goal[0] and self.location[1] == self.goal[1] and self.run_away:
            self.run_away = False

        if self.checkMove(self.direct) and (len(self.destinations) != 0 or self.run_away):
            self.move(self.direct)

        elif len(self.destinations) != 0:
            self.goal = self.destinations[0]

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

    def checkMove(self, direction):
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

    def get_weight(self, coord, map):
        weight = 0
        for i in range(coord[0]-5, coord[0]+5):
            for j in range(coord[1]-5, coord[1]+5):
                if (0 <= j and j < 100 and 0 <= i and i < 100):
                    weight += map[i][j]
        return weight

    def scanArea(self):
        """ Scans the area for game objects, updating its memory as it finds targets. Returns whether an agent is within
        its radar
        """
        nearby = self.game_field.scan_radius(self)
        foundAgent = []
        for obj in nearby:
            if(isinstance(obj,Agent)):
                #is another agent
                foundAgent.append(obj)
            if(isinstance(obj, Target) and obj.owner == self and not obj.collected):
                #is a target that belongs to the agent and belongs to the agent
                self.self_targets_found.append(obj)
                obj.collect()
                #print("HAHA got {}".format(len(self.self_targets_found)))
                if len(self.self_targets_found) == no_targets_per_agent:
                    print("WIN!")
                    self.winner = True
            elif (isinstance(obj,Target) and obj.owner != self and (obj not in self.other_targets_found)):
                #is a target that belongs to another agent
                self.other_targets_found.append(obj)

        return foundAgent

