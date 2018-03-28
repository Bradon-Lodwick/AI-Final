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
        # Creates the empty lists for the targets the agent has found
        self.self_targets_found = list()
        self.other_targets_found = list()
        # Initializes the agent's movement to the exploration mode
        self.movement_mode = MoveModes.EXPLORE
        # Initializes the memory of the map that the agent has seen
        self.memory = np.ones(shape=(size_x, size_y))
        self.prevstep = None
        self.drawing_location = [self.location[0] - 11, self.location[1] - 11]
        self.winner = False
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

    def step(self):
        """

        TODO
        ----
        * Add ability for agents to pathfind towards their targets while exploring if they are nearby
        * Add a weight to the target depending on how many targets it knows the location
        """

        # The location that the agent is aiming to go to
        desired_location = None
        # Check movement mode
        if self.movement_mode == MoveModes.PATHFIND:
            # Get closest target location
            desired_location = self.get_closest_target_location()

        # Determine movement direction based on weight function
        weighted_direction = self.get_weighted_direction(desired_location)

        # Re-evaluate number of targets known
        if not len(self.self_targets_found) < no_targets_per_agent:
            self.movement_mode = MoveModes.PATHFIND

        # Change target direction if agent in radar
        # TODO needs to change direction based on previous direction, not desired, to avoid collision
        if self.ScanArea() and (not(self.prevstep == None)):
            if self.prevstep == Direction.N and self.location[0] + 1 < 100:
                weighted_direction = Direction.E
            elif self.prevstep == Direction.E and self.location[1] + 1 < 100:
                weighted_direction = Direction.S
            elif self.prevstep == Direction.S and self.location[0] - 1 > 0:
                weighted_direction = Direction.W
            elif self.prevstep == Direction.W and self.location[0] - 1 > 0:
                weighted_direction = Direction.N

        self.prevstep = weighted_direction

        # Move in given direction
        self.move(weighted_direction)

    def move(self, direction):
        if direction == Direction.N:
            self.location[1] -= speed
        elif direction == Direction.S:
            self.location[1] += speed
        elif direction == Direction.E:
            self.location[0] += speed
        elif direction == Direction.W:
            self.location[0] -= speed
        if (self.location[0] > 100 or self.location[0] < 0) or (self.location[1] > 100 or self.location[1] < 0):
            print("O No")
        self.drawing_location = [self.location[0]-11, self.location[1]-11]

    def ScanArea(self):
        """ Scans the area for game objects, updating its memory as it finds targets. Returns whether an agent is within
        its radar
        """
        nearby = self.game_field.scan_radius(self)
        foundAgent = False
        for obj in nearby:
            if isinstance(obj,Agent):
                #is another agent
                foundAgent = True
            if(isinstance(obj, Target) and obj.owner == self and not obj.collected):
                #is a target that belongs to the agent and belongs to the agent
                self.self_targets_found.append(obj)
                obj.collect()
                if len(self.other_targets_found) == no_targets_per_agent:
                    self.winner = True
            elif (isinstance(obj,Target) and (obj not in self.other_targets_found)):
                #is a target that belongs to another agent
                self.other_targets_found.append(obj)
        return foundAgent



    def get_closest_target_location(self):
        """ Returns the closest found target's location.

        Returns
        -------
        best : list
            The coordinate of the closest target to the agent in (x, y) format.
        """
        best_dist = inf
        best = None
        # finds the closest target in the targets found
        for target in self.self_targets_found:
            target_loc = target.get_location()
            dist_to_target = abs(target_loc[0] - self.location[0]) + abs(target_loc[1] - self.location[1])
            if dist_to_target < best_dist:
                best = target_loc
                best_dist = dist_to_target
        return best

    def get_weighted_direction(self, target):
        """ Returns a direction for the agent to move in based on weighted values generated by its memory and given
        target information.

        Parameters
        ----------
        target : list
            The x, y coordinates of the target

        Returns
        -------
        current_best : Direction
            The movement direction to go in.
        """

        # Weighted direction from given target
        target_x_weight = 0
        target_y_weight = 0
        # Checks if target was given
        if target is not None:
            desired_x = target[0]
            desired_y = target[1]

            # Locks off directions that do not lead to the target
            if self.location[1] > desired_y:
                    target_y_weight = Direction.N
            else:
                    target_y_weight = Direction.S

            if self.location[0] > desired_x:
                target_x_weight = Direction.W
            else:
                target_x_weight = Direction.E

        # Initializes the weight of all the directions
        weightN, weightE, weightS, weightW = 0, 0, 0, 0

        # Each if statement checks which directions can be moved in based on if there is a wall or if it is locked from
        # path finding in that direction
        # Checks for North
        if self.location[1] - speed > 0 and target_y_weight != Direction.S:
            # Looks double the radar range in the given direction, and increases weight based on how many cells not
            # visited
            for j in range(0, radar_radius * 2):
                # Tries until it hits a wall in the memory
                try:
                    if (self.memory[self.location[0], self.location[1] - j] == 1) and not (self.location[1] - j < 0):
                        weightN = weightN + 1
                except IndexError:
                    break
        # Check for South
        if self.location[1] + speed < 100 and target_y_weight != Direction.N:
            # Looks double the radar range in the given direction, and increases weight based on how many cells not
            # visited
            for j in range(0, radar_radius * 2):
                # Tries until it hits a wall in the memory
                try:
                    if (self.memory[self.location[0], self.location[1] + j] == 1) and not (self.location[1] + j > 100):
                        weightS = weightS + 1
                except IndexError:
                    break
        # Checks for West
        if self.location[0] - speed > 0 and target_x_weight != Direction.E:
            # Looks double the radar range in the given direction, and increases weight based on how many cells not
            # visited
            for j in range(0, radar_radius * 2):
                # Tries until it hits a wall in the memory
                try:
                    if (self.memory[self.location[0] - j,self.location[1]] == 1) and not (self.location[0] - j < 0):
                        weightW = weightW + 1
                except IndexError:
                    break
        # Checks for East
        if self.location[0] + speed < 100 and target_x_weight != Direction.W:
            # Looks double the radar range in the given direction, and increases weight based on how many cells not
            # visited
            for j in range(0, radar_radius * 2):
                # Tries until it hits a wall in the memory
                try:
                    if (self.memory[self.location[0] + j,self.location[1]] == 1) and not (self.location[0] + j > 100):
                        weightE = weightE + 1
                except IndexError:
                    break

        # Checks which weight is higher, in case of tie picks one at random
        current_best_weight = 0
        current_best_direction = 0
        current_best_val = 0
        # Checks all weights, and in case of ties picks one at random
        Nval,Sval,Eval,Wval = random.randint(0,100), random.randint(0,100), random.randint(0,100), random.randint(0,100)
        # Checks North weight
        if current_best_weight <  weightN:
            current_best_direction = Direction.N
            current_best_weight = weightN
            current_best_val = Nval
        # Checks East weight
        if current_best_weight <  weightE or (current_best_weight == weightE and Eval > current_best_val):
            current_best_direction = Direction.E
            current_best_weight = weightE
            current_best_val = Eval
        # Checks South weight
        if current_best_weight <  weightS or (current_best_weight == weightS and Sval > current_best_val):
            current_best_direction = Direction.S
            current_best_weight = weightS
            current_best_val = Sval
        # Checks West weight
        if current_best_weight <  weightW or (current_best_weight == weightW and Wval > current_best_val):
            current_best_direction = Direction.W
            current_best_weight = weightW
            current_best_val = Wval

        # Return the current best weighted direction
        return current_best_direction

