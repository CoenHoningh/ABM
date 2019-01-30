""" Module for the model instance.
Creates the general road model in which the car agents reside.
"""
import hashlib
import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
# from mesa.space import SingleGrid
import cargrid as car
from lane_grid import LaneSpace
from data_collection import avg_speed, cars_in_lane, track_params, track_run


class RoadSim(Model):

    """ Hosts the road model and the mesa grid.
    Contains methods to generate new car agents and collect data.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(self, lanes=3, length=5000, spawn=0.4, agression=0.1,
                 speed=100, time_step=0.1, init_time=0, min_gap=1.0):
        super().__init__()
        self.uid = hash((spawn, agression, min_gap))
        self.current_id = 0
        self.lanes = lanes
        self.spawn_chance = spawn
        self.length = int(length)
        self.init_time = init_time
        self.time_step = time_step
        self.agression = agression
        self.min_gap = min_gap

        self.grid = LaneSpace(self.length, self.lanes, self.time_step, scale=0.2)

        self.schedule = RandomActivation(self)
        self.speed = speed/3.6
        self.cars = []
        self.new_car()
        self.new_car(start_lane=1)

        self.datacollector = DataCollector(
            model_reporters={
                "Avg_speed": avg_speed,
                'Cars_in_lane': cars_in_lane,
                'Model Params': track_params,
                'Run': track_run}
            )

        if init_time:
            self.__init_sim()

    def __init_sim(self):
        for _ in range(self.init_time):
            self.schedule.step()
            self.init_cars()

    def get_free_lanes(self):
        """
        Returns a bool arary of the availability of each lane.
        """
        return np.count_nonzero(self.grid.positions < self.speed*self.time_step, axis=1) == 0

    def init_cars(self):
        """
        Loops over all lanes and randomly creates a new car object if
        sufficient space is available.
        """
        free_lanes = self.get_free_lanes()
        for i in range(self.lanes):
            if free_lanes[i] and np.random.rand()\
             < (self.spawn_chance*self.time_step):
                self.new_car(i)

    def new_car(self, start_lane=0):
        """
        Generates a new car object and adds it to the model scheduler.
        """
        new_car = car.Car(self.next_id(), self, start_lane, self.speed,
                          self.agression, self.min_gap)

        self.grid.place_agent(new_car)
        self.cars.append(new_car)
        self.schedule.add(new_car)

    def move(self, agent, new_lane):
        """
        Wrapper method on the mesa move agent method, also updates the
        global occupied set which allows for very fast lookups compared to
        the empties list. The agent pos variable is also updated.
        """
        has_moved = self.grid.move_agent(agent, new_lane)
        if not has_moved:
            # print(agent.unique_id)
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            self.cars.remove(agent)
            return

    def step(self):
        self.schedule.step()
        self.init_cars()
        self.datacollector.collect(self)
    # def stats(self):
    #     """
    #     retrieve the speed of each car to determine distribution
    #     """
    #     speed_dist = [i.speed for i in self.cars]
    #     avg_car_speed = np.average(speed_dist)
    #     print(avg_car_speed)

    # def run_sim(self, steps=500):
    #     # self.visualise()
    #     for _ in range(steps):
    #         # plt.draw()
    #         self.step()
    #         print("hoi")
    #         self.init_cars()
    #         # plt.pause(0.001)
