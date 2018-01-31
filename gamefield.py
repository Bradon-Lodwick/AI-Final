import numpy as np
import settings

class GameField:
    length = None
    width = None

    agent_list = []
    target_list = []

    def __init__(self):
        self.length = settings.length
        self.width = settings.width

    def add_agent(self, agent):
        self.agent_list.appened(agent)

    def add_target(self, target):
        self.target_list.append(target)

    