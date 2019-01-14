from mesa import Model
import matplotlib.pyplot as plt

import road
import car


class RoadSim(Model):
    def __init__(self, lanes=1):
        self.current_id=0
        self.lanes = 1

        self.road = road.RoadContinuous()

        # car1 = car.Car()
        self.cars = []
        self.new_car()


    def new_car(self):
        new_car = car.Car(self.next_id())

        self.road.env.place_agent(new_car, (new_car.x, new_car.y))
        self.cars.append(new_car)
    
    def visualise(self):
        self.fig = plt.figure(figsize=(2500, 5 * 10), dpi=80)
        self.plot = self.fig.gca()
        self.road.visualise(self.plot)

        for cari in self.cars:
            cari.visualize(self.plot)
        plt.show()




mod1 = RoadSim()

mod1.visualise()