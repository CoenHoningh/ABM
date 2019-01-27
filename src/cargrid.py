""" Module which defines the car agents
"""
import random
from mesa import Agent
import numpy as np
from scipy.stats import truncnorm, norm


class Car(Agent):
    """
    Defines the properties and behaviour of each car agent.
    """
    def __init__(self, unique_id, model, start_lane, speed):
        super().__init__(unique_id, model)
        self.start_lane = start_lane
        self.index = self.unique_id % model.length
        # self.loc = 0.0
        # self.lane = start_lane
        self.pos = (0.0, start_lane)
        self.max_speed = speed+(np.random.rand()*5)
        self.speed = self.max_speed
        self.gap = np.random.rand()*2 + 1

    # def compute_pars(self, FRONT, BACK):

    #     S = (self.pos[0], self.speed)
    #     PA, PB, PC = FRONT
    #     FA, FB, FC = BACK

    #     # Gaps before change
    #     G_PB = PB[0] - S[0]
    #     G_FB = S[0] - FB[0]

    #     # Gaps to the right
    #     G_PA = PA[0] - S[0]
    #     G_FA = S[0] - FA[0]

    #     # Gaps to the left
    #     G_PC = PC[0] - S[0]
    #     G_FC = S[0] - FC[0]

    #     GAPS = [G_PA, G_PB, G_PC, G_FA, G_FB, G_FC]

    #     # Collision times before change
    #     T_PB = G_PB/(S[1]-PB[1])
    #     T_FB = G_FB/(FB[1]-S[1])

    #     # Collision times to the right
    #     T_PA = G_PA/(S[1]-PA[1])
    #     T_FA = G_FA/(FA[1]-S[1])

    #     # Collision times to the left
    #     T_PC = G_PC/(S[1]-PC[1])
    #     T_FC = G_FC/(FC[1]-S[1])

    #     TIMES = [T_PA, T_PB, T_PC, T_FA, T_FB, T_FC]

    #     # Distances
    #     # D_A = PA[0] - FA[0]
    #     # D_C = PC[0] - FC[0]

    #     # DISTS = [D_A, D_C]

    #     G_PA_min = np.exp(1 + 1.541 * max(0, S[1]-PA[1]) +
    #                       6.210*min(0, S[1]-PA[1])+0.13*PA[1]-0.008*self.v[0]+self.e[0])

    #     G_FA_min = np.exp(1.5 + 1.426 * max(0, FA[1]-S[1])+0.64*FA[1]
    #                       - 0.205 * self.v[1]+self.e[1])

    #     G_PC_min = np.exp(1 + 1.541 * max(0, S[1]-PC[1]) +
    #                       6.210*min(0, S[1]-PC[1])+0.13*PC[1]-0.008*self.v[0]+self.e[0])

    #     G_FC_min = np.exp(1.5 + 1.426 * max(0, FC[1]-S[1])+0.64*FC[1]
    #                       - 0.205 * self.v[1]+self.e[1])

    #     min_gaps_r = (G_PA_min, G_FA_min)
    #     min_gaps_l = (G_PC_min, G_FC_min)

    #     return GAPS, TIMES, min_gaps_r, min_gaps_l

    def get_move(self):
        '''
        Checks if the lane is free.
            view: how many places to look ahead
            lane: which lane to check: -1 = right, 0 = same, 1 = left
        '''
        FRONT, BACK = self.model.grid.get_neighbors(self)
        # print(FRONT, BACK)
        # print(self.pos, self.speed)
        # print('-------')
        while True:
            # gaps, times, min_r, min_l = self.compute_pars(FRONT, BACK)
            rf, mf, lf = FRONT
            rb, mb, lb = BACK
            if mf[0]-self.pos[0] > self.gap*self.speed:
                if self.speed < self.max_speed:
                    self.check_speed(mf[0]-self.pos[0])
                return 0
            can_left = lf[0]-self.pos[0] > self.gap*self.speed and self.pos[0]-lb[0]> 0.5*self.speed and self.pos[1] < (self.model.lanes - 1)
            can_right = rf[0]-self.pos[0] > self.gap*self.speed and self.pos[0]-rb[0]> 0.5*self.speed and self.pos[1] > 0
            if can_left and can_right:
                if rf[0] < lf[0]:
                    return 1
                if self.speed < 10:
                    return -1
                return 1
            if can_left:
                return 1
            if can_right:
                return -1
            self.speed -= np.random.rand()*self.gap*self.model.time_step
            # print('-----')
            # print(self.pos[1])
            # print('middle')
            # print(mf[0]-self.pos[0], self.pos[0]-mb[0], self.speed)
            # print('right')
            # print(rf[0]-self.pos[0], self.pos[0]-rb[0], self.speed)
            # print('left')
            # print(lf[0]-self.pos[0], self.pos[0]-lb[0], self.speed)
            # print('slowed')
        # front_view = int(self.speed*self.distance+view)
        # back_view = -1*abs(int(5*self.speed/self.max_speed)*lane)
        # if front_view == 0:
        #     return (self.x+1, self.y+lane) in self.model.grid.empties
        # if not self.model.lanes > (self.y + lane) >= 0:
        #     return False
        # for x in range(front_view, back_view, -1):
        #     if (self.x+x, self.y+lane) in self.model.occupied:
        #         return False
        # return True

    def is_slowed(self):
        """
        Check if the agent is below their maximum speed
        """
        return self.speed < self.max_speed

    def check_speed(self, gap):
        """
        Check if the car has recently braked and otherwise can speed up.
        """
        diff = self.max_speed - self.speed
        space = (gap-self.speed)/self.speed/self.gap
        speedup = max(np.random.rand(), np.log(diff*space))*self.model.time_step
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
            self.speed -= np.random.rand()*self.gap*self.model.time_step

        # if self.is_slowed():
        #     self.check_speed()

    # def advance(self):
    #     """
    #     Perform the closing scheduled agent step.
    #     """
