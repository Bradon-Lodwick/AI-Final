import settings
from game_field import GameField
from agent import Agent
from target import Target
import random

if __name__ == '__main__':

    field = GameField(50,50)

    agent1 = Agent(settings.Mode.COLLABORATION, [0,0], "E-Bert")
    agent2 = Agent(settings.Mode.COLLABORATION, [0,1], "A-Bert")
    target1 = Target(agent2, 4, [30,15], "Other-Bert")
    target2 = Target(agent2, 4, [10,1], "Egg-Bert")
    target3 = Target(agent1, 4, [25,30], "Steve-Bert")

    field.add_object(agent1)
    field.add_object(agent2)
    field.add_object(target1)
    field.add_object(target2)
    field.add_object(target3)


    tracked_agent = agent1
    for i in range(15):
        """
        print("\n{} location: {}".format(tracked_agent.name, tracked_agent.get_location()))
        print("My field size is: {}x{}".format(tracked_agent.field.width, tracked_agent.field.length))
        for go in field.scan_radius(tracked_agent, 10):
            print("{0:<3}\t{1:<10}\t{2}".format(go.__class__.__name__, go.get_name(), go.get_location()))
            if go.__class__.__name__ == "Target" and go.agent == tracked_agent:
                go.is_found()
        """
        tracked_agent.move_agent_random(10)
        agent2.move_agent_random(10)
