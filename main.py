import settings
from game_field import GameField
from agent import Agent
from target import Target
import random


def testing():
    """ The function to be ran for testing purposes."""
    field = GameField(list(), 50, 50)

    agent1 = Agent(settings.Mode.COLLABORATION, [0, 0], "E-Bert")
    agent2 = Agent(settings.Mode.COLLABORATION, [0, 1], "A-Bert")
    target1 = Target(agent2, 4, [30, 15], "Other-Bert")
    target2 = Target(agent2, 4, [10, 1], "Egg-Bert")
    target3 = Target(agent1, 4, [25, 30], "Steve-Bert")

    field.add_object(agent1)
    field.add_object(agent2)
    field.add_object(target1)
    field.add_object(target2)
    field.add_object(target3)

    tracked_agent = agent1
    for i in range(15):
        print("\n{} location: {}".format(tracked_agent.name, tracked_agent.get_location()))
        print("My field size is: {}x{}".format(tracked_agent.field.width, tracked_agent.field.length))
        for go in field.scan_radius(tracked_agent, 10):
            print("{0:<3}\t{1:<10}\t{2}".format(go.__class__.__name__, go.get_name(), go.get_location()))
            if go.__class__.__name__ == "Target" and go.agent == tracked_agent:
                go.is_found()
        tracked_agent.move_agent_random(10)
        agent2.move_agent_random(10)


def setup_game():
    """ Sets up the game by creating the game field, agents, and targets.

    Returns
    -------
    GameField
        Returns the game field that will be used for the game the is set up

    """
    # Gets desired mode from user
    mode_input = -1
    while not (1 <= int(mode_input) <= 3):
        mode_input = int(input("Please input desired mode. 1 = Competition, 2 = Collaboration, 3 = Compassionate\n>"))

    if mode_input == 1:
        mode_input = settings.Mode.COMPETITION
    elif mode_input == 2:
        mode_input = settings.Mode.COLLABORATION
    elif mode_input == 3:
        mode_input = settings.Mode.COMPASSIONATE

    # Temporary lists for the agents and targets, to be added to the game_field when initialized
    agents = list()
    targets = list()
    # Begins creating the agents
    for agent_id in range(settings.no_agents):
        # TODO get origin for agent by rng
        origin = (0, 0)
        agent = Agent(mode_input, origin, name='Agent {}'.format(agent_id))
        agents.append(agent)
    # Begins creating the targets
    for agent in agents:
        for target_id in range(settings.no_targets_per_agent):
            # TODO get origin for agent by rng
            origin = (0, 0)
            target = Target(agent, i, origin, name='Target {}-{}'.format(agent.name, i))
            targets.append(target)

    # Creates the game objects list to pass to the game field
    game_objects = agents
    game_objects.extend(targets)

    # Creates the game field
    field = GameField(game_objects)

    # Returns the game field
    return field


if __name__ == '__main__':
    testing()
