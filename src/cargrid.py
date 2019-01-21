""" Module which defines the car agents
"""
from mesa import Agent
import numpy as np


class Car(Agent):
    """
    Defines the properties and behaviour of each car agent.
    """
    def __init__(self, unique_id, model, start_lane=0, speed=1):
        super().__init__(unique_id, model)
        self.start_lane = start_lane
        self.lane = start_lane
        self.maxlane = self.model.lanes-1
        self.x = 0
        self.y = start_lane
        self.pos = (self.x, self.y)
        self.speed = speed
        self.max_speed = speed
        self.braked = 0

    def is_free(self, _view, _lane=0):
        '''
        Checks if the lane is free.
            _view: how many places to look ahead
            _lane: which lane to check: -1 = right, 0 = same, 1 = left
        '''
        _a = -2
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
        cells = [(self.x+x, self.y+_lane) for x in range(_a, _view+1)]
        contents = self.model.grid.get_cell_list_contents(cells)
        return not contents
        # bool_list = [self.model.grid.is_cell_empty((self.x+x, self.y+_lane))
        #              for x in range(_a, _view+1)]
        # if not bool_list:
        #     return True
        # return all(bool_list)

    def is_slowed(self):
        """
        Check if the agent is below their maximum speed
        """
        return self.speed < self.max_speed

    def check_speed(self):
        """
        Check if the car has recently braked and otherwise can speed up.
        """
        if self.braked:
            self.braked -= np.random.randint(0, self.braked+1)
        elif self.is_free(self.speed+1):
            self.speed += 1

    def step(self):
        """
        Perform the initial scheduled agent step.
        """
        self.pos = (self.x, self.y)
        if not self.speed:
            if self.is_free(1):
                self.x += 1
            elif self.is_free(1, -1):
                self.x += 1
                self.y -= 1
            elif self.is_free(1, 1):
                self.x += 1
                self.y += 1

        elif self.is_free(int(self.speed*1.3)+1):
            '''
            Move ahead if the current speed allows
            '''
            self.x += self.speed
            if self.y > 0:
                if self.is_free(int(self.speed*1.3)+1, -1):
                    '''
                    Move a lane to the right if speed allows
                    '''
                    self.y -= 1

        elif self.y < self.maxlane and self.is_free(int(self.speed*1.3)+1, 1):
            '''
            Move a lane to the left if the speed allows
            '''
            self.x += self.speed + 1
            self.y += 1

        else:
            '''
            Slow down 1 tick if none are possible
            '''
            self.braked = 5
            self.speed = max(self.speed-1, 0)
            while self.speed and not\
                    self.is_free(int((self.speed+1)*self.speed)):
                self.speed = max(self.speed-1, 0)
            self.x += self.speed

        if self.model.grid.out_of_bounds((self.x, self.y)):
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        self.model.grid.move_agent(self, (self.x, self.y))

        self.pos = (self.x, self.y)
        if self.is_slowed():
            self.check_speed()

    # def advance(self):
    #     """
    #     Perform the closing scheduled agent step.
    #     """
