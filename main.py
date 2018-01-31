import settings
from game_field import GameField
from agent import Agent
from target import Target

if __name__ == '__main__':

    field = GameField()

    agent1 = Agent(settings.Mode.COLLABORATION, [0,0], "E-Bert")
    agent2 = Agent(settings.Mode.COLLABORATION, [0,1], "A-Bert")
    target1 = Target("steve", 4, [1,1], "Other-Bert")
    target2 = Target("steve", 4, [10,1], "Egg-Bert")
    target3 = Target("steve", 4, [25,1], "Steve-Bert")

    field.add_objects(agent1)
    field.add_objects(agent2)
    field.add_objects(target1)
    field.add_objects(target2)
    field.add_objects(target3)



    for i in range(5):
        print("\nMy location: {}".format(agent1.get_location()))
        for go in field.scan_radius(agent1, 10):
            print("{0:<3}\t{1:<10}\t{2}".format(go[0], go[1], go[2]))
        agent1.move(settings.Direction.E, 4)


