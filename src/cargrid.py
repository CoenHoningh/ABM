""" Module which defines the car agents
"""
from mesa import Agent
import numpy as np


class Car(Agent):
    """
    Defines the properties and behaviour of each car agent.
    """
    def __init__(self, unique_id, model, start_lane, speed, agression, min_gap):
        super().__init__(unique_id, model)
        self.start_lane = start_lane
        self.index = self.unique_id % model.grid.length
        # self.loc = 0.0
        # self.lane = start_lane
        self.pos = (0.0, start_lane)
        self.max_speed = speed+(abs(np.random.randn())*agression)
        self.speed = self.max_speed
        self.agression = agression
        self.gap = np.random.rand() / agression + min_gap
        self.switch_delay = int(5 / agression / self.model.time_step)
        self.switched = self.switch_delay

    def compute_pars(self, FRONT, BACK):
        rf, mf, lf = FRONT
        rb, mb, lb = BACK

        can_left = lf-self.pos[0] > 0.7*self.gap * self.speed and\
            self.pos[0]-lb > 0.5 * self.speed and\
            self.pos[1] < (self.model.lanes - 1) and\
            self.switched == 0

        can_right = rf-self.pos[0] > 0.7*self.gap * self.speed and\
            self.pos[0]-rb > 0.2 * self.speed and\
            self.pos[1] > 0 and\
            self.switched == 0

        can_middle = mf - self.pos[0] > self.gap*self.speed

        return can_left, can_middle, can_right

    def get_move(self):
        '''
        Checks if the lane is free.
            view: how many places to look ahead
            lane: which lane to check: -1 = right, 0 = same, 1 = left
        '''
        self.switched -= 1
        self.switched = max(0, self.switched)
        FRONT, BACK = self.model.grid.get_neighbors(self)
        rf, mf, lf = FRONT
        rb, mb, lb = BACK
        # self.match_speed(mf)
        # print(FRONT, BACK)
        # print(self.pos, self.speed)
        # print('-------')
        while True:
            cl, cm, cr = self.compute_pars(FRONT, BACK)
            if cm:
                if cr:
                    self.switched = self.switch_delay
                    return -1
                if self.speed < self.max_speed:
                    self.check_speed(FRONT[1]-self.pos[0])
                return 0
            if cl and cr:
                if rf < lf:
                    self.switched = self.switch_delay
                    return 1
                if self.speed < self.max_speed:
                    self.switched = self.switch_delay
                    return -1
                return 1
            if cl and (np.random.rand() < self.agression):
                self.switched = self.switch_delay
                return 1
            if cr:
                self.switched = self.switch_delay
                return -1
            self.speed -= np.random.rand()*self.model.time_step

    def check_speed(self, gap):
        """
        Check if the car has recently braked and otherwise can speed up.
        """
        diff = self.max_speed - self.speed
        space = (gap-self.speed)/self.speed/self.gap/self.agression
        speedup = max(abs(np.random.randn()), np.log(diff*space))*self.model.time_step
        self.speed += speedup

    def step(self):
        """
        Perform the initial scheduled agent step.
        """
        # self.move = -1
        # if self.speed == 0:
        #     if self.is_free(0):
        #         self.move = 1
        #         self.x += 1
        #     elif self.is_free(-1):
        #         self.move = 2
        #         self.x += 1
        #         self.y -= 1
        #     elif self.is_free(1):
        #         self.move = 3
        #         self.x += 1
        #         self.y += 1

        # elif self.is_free(0):
        #     '''
        #     Move ahead if the current speed allows
        #     '''
        #     self.move = 4
        #     if (self.is_free(-1) and (random.random() < self.agression)):
        #         '''
        #         Move a lane to the right if speed allows
        #         '''
        #         self.move = 5
        #         self.y -= 1
        #         self.x += self.speed
        #     else:
        #         self.x += self.speed

        # elif self.is_free(1):
        #     '''
        #     Move a lane to the left if the speed allows
        #     '''
        #     self.x += self.speed
        #     self.y += 1
        #     self.move = 6

        # elif self.is_free(-1):
        #     self.x += self.speed
        #     self.y -= 1
        #     self.move = 7

        # else:
        #     '''
        #     Slow down 1 tick if none are possible
        #     '''
        #     self.move = 8
        #     self.braked = 2
        #     self.speed = max(self.speed-1, 0)
        #     while self.speed and not\
        #             self.is_free(0):
        #         self.speed = max(self.speed-1, 0)
        #         self.move += 1
        #     self.x += self.speed

        # self.model.move(self, (self.x, self.y))
        move = self.get_move()
        self.model.move(self, move)
        if self.speed > self.max_speed:
            self.speed -= np.random.rand()*self.model.time_step

        # if self.is_slowed():
        #     self.check_speed()

    # def advance(self):
    #     """
    #     Perform the closing scheduled agent step.
    #     """
