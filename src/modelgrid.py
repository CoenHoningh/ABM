""" Module for the model instance.
Creates the general road model in which the car agents reside.
"""
import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
# from mesa.space import SingleGrid
import cargrid as car
from lane_grid import LaneSpace
from data_collection import avg_speed, cars_in_lane, track_params
from data_collection import track_run, avg_slowdown


class RoadSim(Model):

    """
    Hosts the road model and the mesa grid.
    Contains methods to generate new car agents and collect data.

    Attributes:
        uid (int): Hash of specific model parameters, used to
            conveniently group duplicate runs for data analysis.
        current_id (int): Initial value of the agent id generator,
            advances by 1 each time an id is generated through the
            next_id() method from the mesa scheduler.
        length (int): Length in meters of the highway lanes.
            Floored to an integer if a float is provided.
        lanes (int): Number of lanes in the highway model
        spawn_chance (float): Probability to generate a car each
            second, scales with the relative time_step to maintain
            a consistent spawn rate.
        time_step (float): How many seconds each iteration advances,
            e.g. 0.1 -> 10 steps for a second in 'real time'.
        agression (float): Agression of the car agents.
        min_gap (float): Minimal gap the car agents maintain.
        grid (obj): Instance of the LaneSpace class, contains
            the grid with all cars' locations.
        schedule (obj): Instance of the mesa scheduler.
        speed (float): Speed of the cars in m/s
        cars (list): List of all car agent objects.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(self, lanes=3, length=5000, spawn=0.4, agression=0.1,
                 speed=100, time_step=0.1, min_gap=1.6):
        super().__init__()
        self.uid = hash((spawn, agression, lanes))
        self.current_id = 0
        self.length = int(length)
        self.lanes = lanes
        self.spawn_chance = spawn
        self.time_step = time_step
        self.agression = agression
        self.min_gap = min_gap

        self.grid = LaneSpace(self.length, self.lanes, self.time_step,
                              scale=0.5)

        self.schedule = RandomActivation(self)
        self.speed = speed/3.6
        self.cars = []
        self.new_car()
        self.new_car(start_lane=1)

        self.datacollector = DataCollector(
            model_reporters={
                "Avg_speed": avg_speed,
                'Cars_in_lane': cars_in_lane,
                'Avg_slowdown': avg_slowdown,
                'Model Params': track_params,
                'Run': track_run}
            )

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

        while not self.grid.place_agent(new_car):
            new_car = car.Car(self.next_id(), self, start_lane, self.speed,
                              self.agression, self.min_gap)
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
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            self.cars.remove(agent)
            return

    def step(self):
        self.schedule.step()
        self.init_cars()
        self.datacollector.collect(self)
