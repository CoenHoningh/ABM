from mesa import Model
from mesa import Agent
import random

class Car(Agent):
    def __init__(self, unique_id, size=1, start_lane=0):
        self.unique_id = unique_id
        self.size = size
        self.start_lane = start_lane
        self.x = 0
        self.y = start_lane + 0.5

    def visualize(self, plot):
        print(self.x)
        print(self.y)
        plot.scatter(self.x, self.y, s=100, marker='s')
