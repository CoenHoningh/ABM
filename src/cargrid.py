from mesa import Agent
import numpy as np


class Car(Agent):
    def __init__(self, unique_id, model, size=1, start_lane=0, speed=1):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.size = size
        self.start_lane = start_lane
        self.lane = start_lane
        self.maxlane = self.model.lanes-1
        self.x = 0
        self.y = start_lane
        self.pos = (self.x, self.y)
        self.speed = speed
        self.max_speed = speed
        self.new_x = 0
        self.new_y = start_lane
        self.braked = 0

    def is_free(self, _view, _lane=0):
        '''
        Checks if the lane is free.
            _view: how many places to look ahead
            _lane: which lane to check: -1 = right, 0 = same, 1 = left
        '''
        _a = 0
        if _lane == 0:
            '''
            Dont check current spot if staying in the same lane
            '''
            _a = 1
        if _view == 0:
            return True
        if self.maxlane < self.y + _lane < 0:
            return False
        _view = min(self.model.length-self.x-1, _view)
        bool_list = [self.model.grid.is_cell_empty((self.x+x, self.y+_lane))
                     for x in range(_a, _view+1)]
        if not bool_list:
            return True
        return all(bool_list)

    def is_slowed(self):
        return self.speed < self.max_speed

    def check_speed(self):
        if self.braked:
            self.braked -= 1
        elif self.is_free(self.speed+1):
            self.speed += 1

    def step(self):
        self.pos = (self.x, self.y)
        if not self.speed:
            if self.is_free(1):
                self.new_x = self.x + 1
                self.speed = 1
            elif self.is_free(1, -1):
                self.new_x = self.x + 1
                self.new_y = self.y - 1
                self.speed = 1
            elif self.is_free(1, 1):
                self.new_x = self.x + 1
                self.new_y = self.y + 1
                self.speed = 1

        elif self.is_free(int(self.speed*1.3)+1):
            '''
            Move ahead if the current speed allows
            '''
            self.new_x = self.x + self.speed
            # self.speed = min(self.max_speed, self.speed+1)
            if self.y > 0:
                if self.is_free(int(self.speed*1.3)+1, -1):
                    '''
                    Move a lane to the right if speed allows
                    '''
                    self.new_y = self.y - 1
            if self.is_slowed():
                self.check_speed()

        elif self.y < self.maxlane and self.is_free(int(self.speed*1.3)+1, 1):
            '''
            Move a lane to the left if the speed allows
            '''
            self.new_x = self.x + self.speed + 1
            self.new_y = self.y + 1
            if self.is_slowed():
                self.check_speed()
            # self.speed = min(self.max_speed, self.speed+1)

        else:
            '''
            Slow down 1 tick if none are possible
            '''
            self.braked = 5
            self.speed = max(self.speed-1, 0)
            while self.speed and not\
                    self.is_free(int((self.speed+1)*self.speed)):
                self.speed = max(self.speed-1, 0)
            self.new_x = self.x + self.speed
            self.new_y = self.y
            if not self.model.grid.is_cell_empty((self.new_x, self.new_y)):
                print('Not empty')
                print(self.speed)

        if self.model.grid.out_of_bounds((self.new_x, self.y)):
            return

        # close = self.model.grid.get_neighbors(self.pos, 3, False)
        # for car in close:
        #     if car.y == self.y and car.x >= self.x:
        #         pass
        self.x = self.new_x
        self.y = self.new_y
        self.model.grid.move_agent(self, (self.x, self.y))
        # self.model.stats()

    def advance(self):
        if self.model.grid.out_of_bounds((self.new_x+10, self.new_y)):
            print("hoi")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            print(self.pos)
            return

    def visualize(self, plot):
        plot.scatter(self.x, self.y, s=100, marker='s')
