from mesa import Model
from mesa import Agent
import random
import matplotlib.pyplot as plt

class Car(Agent):
    def __init__(self, unique_id, model, size=1, start_lane=0, speed=1):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.size = size
        self.start_lane = start_lane
        self.lane = start_lane
        self.x = 0
        self.y = start_lane
        self.pos = (self.x, self.y)
        self.speed = speed
        self.max_speed = speed
        self.new_x = 0
        self.new_y = start_lane

    def _is_free(self, _view, _lane):
        '''
        Checks is the lane is free.
            _view: how many places to look ahead
            _lane: which lane to check: -1 = right, 0 = same, 1 = left
        '''
        if _lane != 0:
            _a = 0
        else:
            _a = 1
        if _view == 0:
            return True
        _view = min(self.model.length-self.x-1, _view)
        bool_list = [self.model.grid.is_cell_empty((self.x+x, self.y+_lane))
                     for x in range(_a, _view)]
        if not bool_list:
            return True
        return all(bool_list)

    def step(self):
        self.pos = (self.x, self.y)
        if self._is_free(self.speed*2+1, 0):
            '''
            Move ahead if the current speed allows
            '''
            self.new_x = self.x + self.speed
            #self.speed = min(self.max_speed, self.speed+1)
            if self.y > 0:
                if self._is_free(self.speed*2+1, -1):
                    '''
                    Move a lane to the right if speed allows
                    '''
                    self.new_y = self.y - 1

        elif self.y < (self.model.lanes-1) and self._is_free(self.speed*2+1, 1):
            '''
            Move a lane to the left if the speed allows
            '''
            self.new_x = self.x + self.speed +1
            self.new_y = self.y + 1
            #self.speed = min(self.max_speed, self.speed+1)

        else:
            '''
            Slow down 1 tick if none are possible
            '''
            self.speed = max(self.speed-1, 0)
            while not self._is_free((self.speed+1)*self.speed, 0):
                self.speed = max(self.speed-1, 0)
            self.new_x = self.x + self.speed
            self.new_y = self.y
            if not self.model.grid.is_cell_empty((self.new_x, self.new_y)):
                print('Not empty')
                print(self.speed)

        if self.model.grid.out_of_bounds((self.new_x, self.y)):
            return

        close = self.model.grid.get_neighbors(self.pos, 3, False)
        for car in close:
            if car.y == self.y and car.x >= self.x:
                pass
                # print(f"self.x = {self.x} \t\t other.x = {car.x}")
                # print(f"self.y = {self.y} \t\t other.y = {car.y}")
        # print("-----------------------------")
        self.x = self.new_x
        self.y = self.new_y
        self.model.grid.move_agent(self, (self.x, self.y))
        self.model.stats()

    def advance(self):
        if self.model.grid.out_of_bounds((self.new_x+10, self.new_y)):
            print("hoi")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            print(self.pos)
            return


    def visualize(self, plot):
        plot.scatter(self.x, self.y, s=100, marker='s')
