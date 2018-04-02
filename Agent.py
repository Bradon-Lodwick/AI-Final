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
        all_targets_collected : bool
            Holds whether all of the agent's targets have been collected by itself. Collected targets are stored in
            self.targets_collected.
        body : str
            The shape of the agent to be drawn in the terminal.
        destinations : list
            The list of destinations for the agent to go to for exploration mode.
        direct : Direction
            The direction that the agent would like to move in.
        drawing_location : list
            The location to draw the agent on the terminal window at.
        g_id : int
            The id of the game object.
        game_field : GameField
            The game field that the object is on.
        goal : list
            The location the agent would like to move into
        happiness_list : double
            The happiness of the agent.
        location : list
            The location of the object on the game field.
        memory : np.Array
            The memory of the locations that the agent has visited on the game field. 0's in the list mean the agent has
            gone to the location, 1 means it has not.
        movement_mode : MoveMode
            The movement mode that the object is in.
        no_steps_taken : int
            The number of steps the agent has moved.
        other_targets_found : list
            The list of targets that the agent does not own and knows the location of.
        self_targets_found : list
            The list of targets that the agent owns and knows the location of.
        std_deviation : double
            The standard deviation of the agent's happiness.
        targets_collected : list
            The list of targets that the agent has collected.
        """

    def __init__(self, game_field, g_id, location):
        """ Initializes the agent object.

        Parameters
        ----------
        game_field : GameField
            The game field that the agent is to be created on.
        g_id : int
            The id of the agent.
        location : list
            The location the agent will start on, passed in (x, y) format.
        """
        GameObject.__init__(self, game_field, g_id, location)
        # Creates the empty lists for the targets the agent has found
        self.targets_collected = list()
        self.self_targets_found = list()
        self.other_targets_found = list()

        # Sets up the destinations sub matrices
        self.destinations = []
        self.add_sub_locations()
        self.add_sub_locations()

        # Initializes the agent's movement to the exploration mode
        self.movement_mode = MoveModes.EXPLORE

        # Happiness setup
        # Sets the number of steps the agent has taken to 0
        self.no_steps_taken = 0
        # Set initial happiness of list to an empty list
        self.happiness_list = list()

        # Set the minimum
        self.std_deviation = None

        # Sets the direction the agent is to go in to None, as at initialization it doesn't have a goal set
        self.direct = None

        # Initializes the memory of the map that the agent has seen
        self.memory = np.ones(shape=(size_x, size_y))

        # Sets to False as not all targets should be collected on initialization
        self.all_targets_collected = False

        # Boolean value for whether the agent is running away from another agent
        self.run_away = False

        # (x, y) list of the goal location for the agent to go to.
        self.goal = []

        # The location to use for drawing on the terminal
        self.drawing_location = [self.location[0] - 10, self.location[1] - 10]
        # The shape of the agent's body to draw onto the terminal window
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

        # Output to console that the agent was created successfully
        print("Agent {} created at location {}".format(self.g_id, self.location))

    def add_sub_locations(self):
        """ Determines the location of sub matrices to be used when the agent is in exploration mode. Adds the locations
        into the destinations list.
        """
        for i in range(int(size_x/10)):
            for j in range(int(size_y/10)):
                self.destinations.append([i*10+5, j*10+5])

    def distance_from_self(self, coord):
        """ Calculates the manhattan distance between the agent and the given co-ordinate.

        Parameters
        ----------
        coord : list
            The co-ordinate of the other location in (x, y) format.

        Returns
        -------
        distance : int
            The distance from the agent to the given target
        """
        distance = abs(coord[0] - self.location[0]) + abs(coord[1] - self.location[1])
        return distance

    def check_needed_movement_mode(self):
        """ Re-evaluates which movement mode the agent should be in based on how many targets it has collected and
        knows the location of.
        """

        # Gets the current movement mode so that it can be output if the movement mode changed
        previous_mode = self.movement_mode

        # If the agent has found all of its targets
        if self.all_targets_collected:
            self.movement_mode == MoveModes.STOP
        # If all targets that are left to be collected are known
        elif len(self.self_targets_found) + len(self.targets_collected) == no_targets_per_agent:
            # Changes based on which mode the game is in
            # If in competitive or compassionate, automatically goes to path finding mode
            if self.game_field.mode == GameModes.COMPETITIVE or self.game_field.mode == GameModes.COMPASSIONATE:
                self.movement_mode = MoveModes.PATHFIND
            # If in cooperative, only goes to path finding when all of the agents have their target locations
            # TODO change true to function checking all agent info
            elif self.game_field.mode == GameModes.COOPERATIVE and self.game_field.check_all_agents_ready():
                self.movement_mode = MoveModes.PATHFIND
            else:
                self.movement_mode = MoveModes.EXPLORE
        # If all targets that are left are not known, change to exploration mode
        elif len(self.self_targets_found) + len(self.targets_collected) < no_targets_per_agent:
            self.movement_mode = MoveModes.EXPLORE
        # If all targets known + all targets collected > no_targets_per_agent, and error has occurred somewhere
        else:
            raise RuntimeWarning('Agent {} currently thinks it has collected/found locations for more targets than '
                                 'possible\nfound={}, collected={}, no_targets_per_agent={}'
                                 .format(self.g_id, len(self.self_targets_found), len(self.targets_collected),
                                         no_targets_per_agent))

        # Checks if the movement mode has changed and prints out the movement mode if it had
        if previous_mode != self.movement_mode:
            # Print out the movement mode of the agent
            print("Agent {} is in {} mode".format(self.g_id, self.movement_mode))

    def fix_goal(self, goal):
        new_goal = goal
        if goal[0] < 0:
            new_goal[0] = 0
        elif goal[0] >= size_x:
            new_goal[0] = size_x - 1
        if goal[1] < 0:
            new_goal[1] = 0
        elif goal[1] >= size_y:
            new_goal[1] = size_y - 1

        return new_goal

    def step(self):
        """ Runs the agent through 1 movement step. Takes into account other agent information, movement mode, etc.
        """
        # Get info from other agents
        self.get_info()

        # Scan area, collecting targets and finding agents in area
        agents_in_area = self.scan_area()

        if self.all_targets_collected:
            self.goal = self.location

        # Checks to see if the agent needs to run away to avoid a collision
        if len(agents_in_area) > 0 and not self.run_away:
            self.run_away = True
            self.goal = self.escape_zone(agents_in_area)

        # Check which movement mode the agent is in
        # Exploration mode
        elif not self.run_away and len(self.destinations) != 0 and self.movement_mode == MoveModes.EXPLORE:
            # For each destination in the destinations list
            for dest in self.destinations:
                if self.get_weight(dest, self.memory) == 0:
                    self.destinations.remove(dest)
            if len(self.destinations) != 0:
                # Sort the destination list by the weight of each location
                self.destinations.sort(key=lambda x: (self.distance_from_self(x), -self.get_weight(x, self.memory)))
                # Set the goal to the destination that was found
                self.goal = self.destinations[0]
        # Path finding mode
        elif not self.run_away and self.movement_mode == MoveModes.PATHFIND and not self.all_targets_collected:
            self.goal = self.find_closest_target(self.self_targets_found, self.location).location

        # Checks which direction the agent should move in, setting it to self.direct
        # If needs to move East
        self.goal = self.fix_goal(self.goal)

        if self.location[0] < self.goal[0]:
            self.direct = Direction.E
        # If needs to move West
        elif self.location[0] > self.goal[0]:
            self.direct = Direction.W
        # If needs to move South
        elif self.location[1] < self.goal[1]:
            self.direct = Direction.S
        # If needs to move North
        elif self.location[1] > self.goal[1]:
            self.direct = Direction.N

        # If the goal was reached by the agent in exploration mode, it needs to be removed from the destination list
        if self.location == self.goal and self.movement_mode == MoveModes.EXPLORE and self.run_away is False:
            # Pop the location from the destinations list
            self.destinations.remove(self.goal)

        # If the goal was reached by the agent and was in run_away mode, make run_away False
        if self.location == self.goal and self.run_away:
            self.run_away = False

        # Checks to see if the agent can move, moving it if it can
        if self.check_move(self.direct) and self.movement_mode != MoveModes.STOP:
            self.move(self.direct)

        # Communication
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

        # Increment steps taken
        self.no_steps_taken += 1
        # Update happiness list
        self.happiness_list.append(len(self.targets_collected) / (self.no_steps_taken + 1))

        # Re-evaluate which movement mode the agent should be in for the next step cycle
        self.check_needed_movement_mode()

    def escape_zone(self, agents_to_avoid, factor=1):
        """ Determines the location for the agent to escape to in the case of a collision

        Parameters
        ----------
        agents_to_avoid : list
            The list of agents to avoid.
        factor : int
            An integer value used to increase or decrease the distance the agents need to go.

        Returns
        -------
        escape_destination : list
            The (x, y) co-ordinate list of the escape goal for the agent.
        """
        num_e = len(agents_to_avoid)
        avg_x, avg_y = 0, 0
        for e in agents_to_avoid:
            avg_x += int(e.location[0] / num_e)
            avg_y += int(e.location[1] / num_e)
        jitt_x = random.randint(0, 1)
        jitt_y = random.randint(0, 1)
        escape_destination = [factor * (2 * self.location[0] - avg_x) + jitt_x,
                              factor * (2 * self.location[1] - avg_y) + jitt_y]
        return escape_destination

    def move(self, direction):
        """ Moves the target in the given direction, updating it's memory when it moves.

        Parameters
        ----------
        direction : Direction
            The direction to move the target in
        """

        # Move the agent based on the direction given.
        if direction == Direction.N:
            self.location[1] -= speed
        elif direction == Direction.S:
            self.location[1] += speed
        elif direction == Direction.E:
            self.location[0] += speed
        elif direction == Direction.W:
            self.location[0] -= speed
        self.drawing_location = [self.location[0]-10, self.location[1]-10]

        # Update the agent's memory
        self.memorize()

    def check_move(self, direction):
        """ Check if the agent is able to move in the given direction. Checks to see if moving the agent in the given
        direction will make it leave the field.

        Parameters
        ----------
        direction : Direction
            The direction to test.

        Returns
        -------
        bool
            Whether the agent can move in the given direction.
        """
        # TODO return approved coordinates
        if direction == Direction.E and self.location[0] + speed < 100:
            return True
        elif direction == Direction.S and self.location[1] + speed < 100:
            return True
        elif direction == Direction.W and self.location[0] - speed >= 0:
            return True
        elif direction == Direction.N and self.location[1] - speed >= 0:
            return True
        else:
            return False

    @staticmethod
    def get_weight(coord, mat):
        """ Gets a weight for a given coordinate.
        """
        weight = 0
        for i in range(coord[0]-5, coord[0]+5):
            for j in range(coord[1]-5, coord[1]+5):
                if 0 <= j < 100 and 0 <= i < 100:
                    weight += mat[i][j]
        return weight

    def scan_area(self):
        """ Scans the area for game objects, updating its memory as it finds targets. Returns whether an agent is within
        its radar.

        Returns
        -------
        found_agent : list
            The list of agents that were found in the radar scan.
        """
        nearby = self.game_field.scan_radius(self)
        found_agent = []
        for obj in nearby:
            if isinstance(obj, Agent):
                # is another agent
                found_agent.append(obj)
            # is a target that belongs to the agent and belongs to the agent
            if isinstance(obj, Target) and obj.owner == self and not obj.collected:
                # Checks if target was in the self_targets_found list to remove if necessary
                if obj in self.self_targets_found:
                    self.self_targets_found.remove(obj)

                # Collects the target
                self.targets_collected.append(obj)
                obj.collect()

                if len(self.targets_collected) == no_targets_per_agent:
                    print("Agent {} collected all of its targets".format(self.g_id))
                    self.all_targets_collected = True

            elif isinstance(obj, Target) and obj.owner != self and (obj not in self.other_targets_found):
                # is a target that belongs to another agent
                self.other_targets_found.append(obj)

        return found_agent

    def memorize(self):
        """ Sets the area in the agent's radar range to seen.
        """
        for i in range(21):
            for j in range(21):
                try:
                    if 0 <= self.drawing_location[0] + j < 100 and 0 <= self.drawing_location[1] + i < 100:
                        if self.body[j + i * 21] != ' ':
                            self.memory[self.drawing_location[0] + j, self.drawing_location[1] + i] = 0
                # Ignore IndexErrors in the case an agent is setting areas outside of game_field's bounds
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
            current_distance = self.calculate_manhattan_distance(start, target.location)
            # If current_distance is smaller than the best_distance, set the current target to be best
            if current_distance < best_distance:
                best_distance = current_distance
                best_target = target

        return best_target

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

    def calculate_happiness_variables(self):
        """ Calculates the happiness variables of the agent, and return all information as a dictionary.

        Returns
        -------
        happiness_dict : dict
            The happiness dictionary
        """

        # The dictionary to be returned
        happiness_dict = dict()

        # Game mode
        happiness_dict['mode'] = self.game_field.mode

        # Agent number
        happiness_dict['agent'] = self.g_id

        # Targets collected
        happiness_dict['targets'] = len(self.targets_collected)

        # Steps taken
        happiness_dict['steps'] = self.no_steps_taken

        # Final happiness
        happiness_dict['happiness'] = self.happiness_list[-1]

        # Find the minimum and maximum happiness
        happiness_dict['min'] = min(self.happiness_list)
        happiness_dict['max'] = max(self.happiness_list)

        # Calculate average happiness
        total = 0
        for happiness in self.happiness_list:
            total += happiness
        happiness_dict['avg'] = total / len(self.happiness_list)

        # Calculate standard deviation of the agent
        happiness_dict['std'] = np.std(self.happiness_list)

        # Calculate the competitiveness of the agent
        happiness_dict['competitiveness'] = (happiness_dict['happiness'] - happiness_dict['min']) / (happiness_dict['max'] - happiness_dict['min'])

        return happiness_dict
