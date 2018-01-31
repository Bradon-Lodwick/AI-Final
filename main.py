import settings
from game_field import GameField
from agent import Agent
from target import Target
import random

if __name__ == '__main__':

    field = GameField(50,50)

    agent1 = Agent(settings.Mode.COLLABORATION, [0,0], "E-Bert")
    agent2 = Agent(settings.Mode.COLLABORATION, [0,1], "A-Bert")
    target1 = Target(agent2, 4, [1,1], "Other-Bert")
    target2 = Target(agent2, 4, [10,1], "Egg-Bert")
    target3 = Target(agent1, 4, [25,1], "Steve-Bert")

    field.add_object(agent1)
    field.add_object(agent2)
    field.add_object(target1)
    field.add_object(target2)
    field.add_object(target3)


    moving_agent = agent1
    for i in range(15):
        possible_directions = [settings.Direction.N, settings.Direction.E, settings.Direction.S, settings.Direction.W]
        print("\nMy location: {}".format(moving_agent.get_location()))
        print("My field size is: {}x{}".format(moving_agent.field.width, moving_agent.field.length))
        for go in field.scan_radius(moving_agent, 10):
            print("{0:<3}\t{1:<10}\t{2}".format(go.__class__.__name__, go.get_name(), go.get_location()))
            if go.__class__.__name__ == "Target" and go.agent == moving_agent:
                go.is_found()

        if moving_agent.location[0] == 0:
            possible_directions.remove(settings.Direction.W)
        if moving_agent.location[0] == moving_agent.field.width:
            possible_directions.remove(settings.Direction.E)
        if moving_agent.location[1] == 0:
            possible_directions.remove(settings.Direction.S)
        if moving_agent.location[1] == moving_agent.field.length:
            possible_directions.remove(settings.Direction.N)

        moving_agent.move(random.choice(possible_directions), 4)


