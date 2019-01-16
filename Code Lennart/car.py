from mesa import Model
from mesa import Agent
import random
import matplotlib.pyplot as plt

class Car(Agent):
    def __init__(self, unique_id, model, size=1, start_lane=0, speed=100):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.size = size
        self.start_lane = start_lane
        self.x = 0
        self.y = start_lane + 0.5
        self.pos = (self.x, self.y)
        self.speed = speed
        self.new_x = 0
        colormap = plt.get_cmap('Dark2')
        r = random.random()
        self.color = colormap(r)

    def step(self):
        self.new_x = self.x + self.speed
        if self.model.road.env.out_of_bounds((self.new_x, self.y)):
            print("hoi")
            return
        close = self.model.road.env.get_neighbors(self.pos, 2, False)
        for car in close:
            if car.y == self.y and car.x >= self.x:
                pass
                # print(f"self.x = {self.x} \t\t other.x = {car.x}")
                # print(f"self.y = {self.y} \t\t other.y = {car.y}")
        # print("-----------------------------")

    def advance(self):
        if self.model.road.env.out_of_bounds((self.new_x, self.y)):
            print("hoi")
            self.model.road.env.remove_agent(self)
            self.model.schedule.remove(self)
            print(self.pos)
            return
        self.x = self.new_x
        self.model.road.env.move_agent(self, (self.x, self.y))

    def visualize(self, plot):
        plot.scatter(self.x, self.y, s=100, marker='s')
