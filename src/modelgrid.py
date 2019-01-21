""" Module for the model instance.
Creates the general road model in which the car agents reside.
"""
import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import cargrid as car
from data_collection import avg_speed, lane_speeds


class RoadSim(Model):

    """ Hosts the road model and the mesa grid.
    Contains methods to generate new car agents and collect data.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, lanes=2, length=500, spawn_chance=0.3):
        super().__init__()
        self.current_id = 0
        self.lanes = lanes
        self.spawn_chance = spawn_chance
        self.length = length

        self.grid = SingleGrid(self.length, self.lanes, True)

        self.schedule = RandomActivation(self)

        self.cars = []
        self.new_car()
        self.new_car(start_lane=1, speed=2)

        self.datacollector = DataCollector(
            model_reporters={
                "Avg_speed": avg_speed,
                "Lane_speed": lane_speeds},
            agent_reporters={})

    def is_free(self, speed, lane):
        """
        Checks if a car can spawn in a given lane.
        """
        for x in range(speed):
            if not self.grid.is_cell_empty((x, lane)):
                return False
        return True and random.random() < self.spawn_chance

    def init_cars(self, speed=5):
        """
        Loops over all lanes and randomly creates a new car object if
        sufficient space is available.
        """
        for start_lane in range(self.lanes):
            if self.is_free(speed, start_lane):
                self.new_car(speed=speed, start_lane=start_lane)

    def new_car(self, start_lane=0, speed=1):
        """
        Generates a new car object and adds it to the model scheduler.
        """
        new_car = car.Car(self.next_id(), self,
                          start_lane=start_lane, speed=speed)

        self.grid.place_agent(new_car, (new_car.x, new_car.y))
        self.cars.append(new_car)
        self.schedule.add(new_car)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.init_cars()

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
