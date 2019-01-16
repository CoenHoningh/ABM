from mesa import Model
from mesa import Agent
import random
import matplotlib.pyplot as plt

class Car(Agent):
    def __init__(self, unique_id, model, start_lane=0, speed=1):
        super().__init__(unique_id, model)
        self.start_lane = start_lane
        self.x = 0
        self.y = start_lane
        self.pos = (self.x, self.y)
        self.speed = speed
        self.new_x = 0
        self.colormap = plt.get_cmap('Dark2')
        r = random.random()
        self.color = self.colormap(r)

    def step(self):
        print('yoyo')
        self.pos = (self.x, self.y)
        print(self.pos)
        self.new_x = self.x + self.speed
        if self.model.grid.out_of_bounds((self.new_x, self.y)):
            print("hoi")
            return
        close = self.model.grid.get_neighbors(self.pos, 3, False)
        self.color = self.colormap(len(close))
        for car in close:
            if car.y == self.y and car.x >= self.x:
                pass
                # print(f"self.x = {self.x} \t\t other.x = {car.x}")
                # print(f"self.y = {self.y} \t\t other.y = {car.y}")
        # print("-----------------------------")
        self.advance()

    def advance(self):
        if self.model.grid.out_of_bounds((self.new_x, self.y)):
            print("hoi")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            print(self.pos)
            return
        self.x = self.new_x
        self.model.grid.move_agent(self, (self.x, self.y))
