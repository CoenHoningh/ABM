from mesa import Model
from mesa.time import SimultaneousActivation
import matplotlib.pyplot as plt

import road
import car


class RoadSim(Model):
    def __init__(self, lanes=1):
        self.current_id=0
        self.lanes = 1

        self.road = road.RoadContinuous()

        self.schedule = SimultaneousActivation(self)

        # car1 = car.Car()
        self.cars = []
        self.new_car()


    def new_car(self):
        new_car = car.Car(self.next_id())

        self.road.env.place_agent(new_car, (new_car.x, new_car.y))
        self.cars.append(new_car)
        getattr(self, f'schedule').add(new_car)

    def step(self):
        self.schedule.step()
        self.visualise()

    def run_sim(self, steps=200):
        for _ in range(steps):
            self.step()
    
    def visualise(self):
        self.fig = plt.figure(figsize=(50, 5), dpi=80)
        self.plot = self.fig.gca()
        self.road.visualise(self.plot)

        for cari in self.cars:
            cari.visualize(self.plot)
        plt.show()




mod1 = RoadSim()

# mod1.visualise()

mod1.run_sim()