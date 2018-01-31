import settings
from game_field import GameField
from agent import Agent
from target import Target

if __name__ == '__main__':

    field = GameField()

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



    for i in range(15):
        print("\nMy location: {}".format(agent1.get_location()))
        print("My field size is: {}x{}".format(agent1.field.width, agent1.field.length))
        for go in field.scan_radius(agent1, 10):
            print("{0:<3}\t{1:<10}\t{2}".format(go.__class__.__name__, go.get_name(), go.get_location()))
            if go.__class__.__name__ == "Target" and go.agent == agent1:
                go.is_found()

        agent1.move(settings.Direction.E, 4)


