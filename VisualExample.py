from bearlibterminal import terminal
import numpy as np
import time
import random
from threading import Thread

class Target:
    def __init__(self, coordinates, owner):
        self.loc = coordinates
        self.centre_x = self.loc[0]
        self.centre_y = self.loc[1]
        self.owner = owner
        self.collected = False
        self.body = "T{}".format(owner.name)
        self.age = 10

    def collect(self):
        self.collected = True
        self.body = "Collected={}=".format(self.owner.name)

    def set_field(self, field):
        self.field = field

    def age_down(self):
        if self.age > 0:
            self.age -= 1
        if self.age == 2:
            self.body = "X"
        elif self.age == 1:
            self.body = "*"

class Agent:
    def __init__(self, name, s_x, s_y, targets_to_collect):
        self.name = name
        self.body = \
            "      +++++++++      " \
            "    ++         ++    " \
            "   +             +   " \
            "  +               +  " \
            " +                 + " \
            " +                 + " \
            "+                   +" \
            "+                   +" \
            "+                   +" \
            "+                   +" \
            "+         {}         +"\
            "+                   +" \
            "+                   +" \
            "+                   +" \
            "+                   +" \
            " +                 + " \
            " +                 + " \
            "  +               +  " \
            "   +             +   " \
            "    ++         ++    " \
            "      +++++++++      ".format(self.name)

        self.direct_x = 1
        self.direct_y = 1
        self.velocity_x = 1
        self.velocity_y = 1
        self.loc_x = s_x
        self.loc_y = s_y
        self.centre_x = self.loc_x + 11
        self.centre_y = self.loc_y + 11
        self.field = None
        self.target_list = targets_to_collect
        self.targets_found = []
        self.winner = False

    def reverse(self, z):
        if z == 0:
            self.direct_x *= -1
            self.velocity_x = self.direct_x * random.choice([1, 2, 2, 2, 4])
        elif z == 1:
            self.direct_y *= -1
            self.velocity_y = self.direct_y * random.choice([1, 2, 2, 2, 4])
        elif z == 2:
            self.direct_x *= -1
            self.velocity_x = self.direct_x * random.choice([1, 2, 2, 2, 4])
            self.direct_y *= -1
            self.velocity_y = self.direct_y * random.choice([1, 2, 2, 2, 4])
            self.velocity_x *= -1
            self.velocity_y *= -1

    def set_field(self, field):
        self.field = field

    def force_x(self, f):
        self.velocity_x = f * random.choice([1, 2, 2, 2, 4])

    def force_y(self, f):
        self.velocity_y = f * random.choice([1, 2, 2, 2, 4])

    def move(self):
        if self.field != None:
            nearby = self.field.scan_radius(self, 10)
            for obj in nearby:
                if isinstance(obj, Agent):
                    if self.loc_x <= obj.loc_x:
                        self.force_x(-1)
                        obj.force_x(1)
                    else:
                        self.force_x(1)
                        obj.force_x(-1)

                    if self.loc_y <= obj.loc_y:
                        self.force_y(-1)
                        obj.force_y(1)
                    else:
                        self.force_y(1)
                        obj.force_y(-1)

                if isinstance(obj, Target) and obj.owner == self and not obj.collected:
                    obj.collect()
                    self.found_target(obj)

            if self.centre_x >= 100 and self.velocity_x > 0 or self.centre_x <= 1 and self.velocity_x < 0:
                self.reverse(0)

            if self.centre_y >= 100 and self.velocity_y > 0 or self.centre_y <= 1 and self.velocity_y < 0:
                self.reverse(1)

            self.loc_x += self.velocity_x
            self.loc_y += self.velocity_y
            self.centre_x = self.loc_x + 11
            self.centre_y = self.loc_y + 11
        else:
            print("No Field to move on")

    def found_target(self, tar):
        if not tar in self.targets_found:
            self.targets_found.append(tar)
        if(len(self.targets_found) == self.target_list):
            self.winner = True


class game_board:
    def __init__(self, objects, dimensions):
        self.dimensions = dimensions
        self.object_list = objects

        for x in self.object_list:
            x.set_field(self)


    def scan_radius(self, agent, radius):
        origin = (agent.centre_x, agent.centre_y)
        surroundings = []

        for obj in self.object_list:
            if obj != agent:
                loc = (obj.centre_x, obj.centre_y)
                distance = np.sqrt((loc[0] - origin[0]) ** 2 + (loc[1] - origin[1]) ** 2)

                if distance <= radius:
                    surroundings.append(obj)

        return surroundings

def print_agent(terminal, agent):
    for i in range(21):
        for j in range(21):
            if agent.body[j + i * 21] != ' ':
                terminal.printf(agent.loc_x + j, agent.loc_y + i, agent.body[j + i * 21])

aa = Agent("A", 0, 0, 5)
ab = Agent("B", 50, 50, 5)
ac = Agent("C", 0, 0, 5)
ad = Agent("D", 50, 50, 5)
ae = Agent("E", 0, 0, 5)
'''
ta1 = Target((50, 3), aa)
ta2 = Target((20, 80), aa)
ta3 = Target((90, 90), aa)

#agent_list = [aa, ab, ac, ad, ae]
agent_list = [aa, ab]

target_list = [ta1, ta2, ta3]
object_list = agent_list + target_list

aa.add_target(target_list)

'''

agent_list = [aa, ab, ac, ad, ae]
target_list = []
refresh = 0.1

for agent in agent_list:
    for i in range(5):
        temp = Target((random.randint(0,98), random.randint(0,98)), agent)
        target_list.append(temp)

object_list = agent_list + target_list
terminal.open()
terminal.set("window: size=100x100, cellsize=8x8")

board = game_board(object_list, (100, 100))

winner_list = []

while True:
    for target in target_list:
        if(target.collected):
            target.age_down()
        terminal.printf(target.loc[0], target.loc[1], target.body)

    for agent in agent_list:
        print_agent(terminal, agent)
        agent.move()
        if(agent.winner == True and not agent in winner_list):
            winner_list.append(agent)

    for i in range(len(winner_list)):
        terminal.printf(0, i*2, "Winner: {}".format(winner_list[i].name))
    time.sleep(refresh)
    terminal.refresh()
    terminal.clear()

terminal.close()

