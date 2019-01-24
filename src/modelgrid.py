""" Module for the model instance.
Creates the general road model in which the car agents reside.
"""
import random
import numpy as np
from tqdm import tqdm
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
# from mesa.space import SingleGrid
from space import SingleGrid
import cargrid as car
from data_collection import avg_speed, lane_speeds, cars_in_lane


class RoadSim(Model):

    """ Hosts the road model and the mesa grid.
    Contains methods to generate new car agents and collect data.
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(self, lanes=3, length=5, gridsize=0.1, spawn=0.4,
                 speed=100, sim_time=1000, init_time=100):
        super().__init__()
        self.current_id = 0
        self.lanes = lanes
        self.spawn_chance = spawn
        self.length = int(length*1000/gridsize)
        self.init_time = init_time

        self.grid = SingleGrid(self.length, self.lanes, False)
        self.gridsize = gridsize

        self.schedule = RandomActivation(self)
        self.speed = int(speed/3.6/gridsize)
        self.occupied = set()
        self.cars = []
        self.new_car()
        self.new_car(start_lane=1)

        self.datacollector = DataCollector(
            model_reporters={
                "Avg_speed": avg_speed,
                'Lane_speeds': lane_speeds,
                'Cars_in_lane': cars_in_lane
                },
            agent_reporters={},
            tables={'Positions': ['x', 'y']})
        self.__init_sim()
        print('Starting run')

    def __init_sim(self):
        print('Initializing model')
        for _ in tqdm(range(self.init_time)):
            self.schedule.step()
            self.init_cars()

    def is_free(self, lane):
        """
        Checks if a car can spawn in a given lane.
        """
        for x in range(self.speed):
            if (x, lane) in self.occupied:
                return False
        return True and random.random() < self.spawn_chance

    def init_cars(self):
        """
        Loops over all lanes and randomly creates a new car object if
        sufficient space is available.
        """
        for start_lane in range(self.lanes):
            if self.is_free(start_lane):
                self.new_car(start_lane=start_lane)

    def new_car(self, start_lane=0):
        """
        Generates a new car object and adds it to the model scheduler.
        """
        new_car = car.Car(self.next_id(), self,
                          start_lane=start_lane, speed=self.speed)

        self.grid.position_agent(new_car, x=new_car.x, y=new_car.y)
        self.cars.append(new_car)
        self.schedule.add(new_car)
        self.occupied.add((new_car.x, new_car.y))

    def move(self, agent, pos):
        """
        Wrapper method on the mesa move agent method, also updates the
        global occupied set which allows for very fast lookups compared to
        the empties list. The agent pos variable is also updated.
        """
        # print(agent.unique_id, agent.pos, pos, agent.speed)
        self.occupied.remove(agent.pos)
        if self.grid.out_of_bounds(pos):
            # print(agent.unique_id)
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            if agent in self.cars:
                self.cars.remove(agent)
            return
        if pos in self.occupied:
            print('error')
            print('agent id', agent.unique_id)
            print('agent speed', agent.speed)
            print('pos', pos)
            print('in occupied and empties', self.occupied & self.grid.empties)
            print('agent move', agent.move)
        self.occupied.add(pos)
        self.grid.move_agent(agent, pos)
        agent.pos = pos

    def step(self):
        self.schedule.step()
        self.init_cars()
        self.datacollector.collect(self)

    def get_positions(self):
        print('saving')
        for agent in self.cars:
            self.datacollector.add_table_row('Positions',
                                             {'x': agent.x, 'y': agent.y})
        print('done')

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
