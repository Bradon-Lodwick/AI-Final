import settings
from game_field import GameField
from agent import Agent
from target import Target


def setup_game():
    """ Sets up the game by creating the game field, agents, and targets.

    Returns
    -------
    GameField
        Returns the game field that will be used for the game the is set up

    """
    # Gets desired mode from user
    mode_input = None
    while int(mode_input) < 1 or int(mode_input) > 3:
        input("Please input desired mode. 1 = Competition, 2 = Collaboration, 3 = Compassionate\n>")

    if mode_input == 1:
        mode_input == settings.Mode.COMPETITION
    elif mode_input == 2:
        mode_input == settings.Mode.COLLABORATION
    elif mode_input == 3:
        mode_input == settings.Mode.COMPASSIONATE

    # Temporary lists for the agents and targets, to be added to the game_field when initialized
    agents = list()
    targets = list()
    # Begins creating the agents
    for i in range(settings.no_agents):
        # TODO get origin for agent by rng
        origin = (0, 0)
        agent = Agent(mode_input, origin, name='Agent {}'.format(i))
    # Begins creating the targets
    for agent in agents:
        for i in range(settings.no_targets_per_agent):
            # TODO get origin for agent by rng
            origin = (0, 0)
            target = Target(agent, i, origin, name='Target {}-{}'.format(agent.name, i))

    # Creates the game objects list to pass to the game field
    game_objects = agents
    game_objects.extend(targets)

    # Creates the game field
    field = GameField(game_objects)

    # Returns the game field
    return field


if __name__ == '__main__':
    # Sets up the game.
    game_field = setup_game()
