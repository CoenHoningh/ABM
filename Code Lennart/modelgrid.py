from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
import matplotlib.pyplot as plt
import random

import road
import cargrid as car


class RoadSim(Model):
    def __init__(self, lanes=3, length=500):
        super().__init__()
        self.current_id = 0
        self.lanes = lanes
        self.spawn_chance = 0.03

        self.grid = road.RoadGrid(lanes=self.lanes)
        #self.grid = SingleGrid(length, self.lanes, True)

        self.schedule = SimultaneousActivation(self)

        # car1 = car.Car()
        self.cars = []
        self.new_car()
        # self.new_car(start_lane=1, speed=2)

    def init_cars(self):
        r = random.random()
        if r < self.spawn_chance:
            speed = random.randint(1,3)
            start_lane = random.randint(0, self.lanes)
            free_space = [self.grid.env.is_cell_empty((start_lane, x)) for x in range(10)]
            if all(free_space):
                self.new_car(speed=speed, start_lane=start_lane)


    def new_car(self, start_lane=0, speed=1):
        new_car = car.Car(self.next_id(), self,
                            start_lane=start_lane, speed=speed)

        self.grid.env.place_agent(new_car, (new_car.x, new_car.y))
        self.cars.append(new_car)
        getattr(self, f'schedule').add(new_car)

    def step(self):
        self.schedule.step()
        # self.carplot.set_offsets([(car[0], car[1])
        #                                 for car in self.road.env._agent_points])
        # self.carplot.set_color([car.color for car in self.cars])
        # self.visualise()

    def run_sim(self, steps=500):
        for _ in range(steps):
            self.step()
            self.init_cars()
