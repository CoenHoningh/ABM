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
        self.index = self.unique_id % model.length
        # self.loc = 0.0
        # self.lane = start_lane
        self.pos = (0.0, start_lane)
        self.max_speed = speed+(np.random.rand()/agression)
        self.speed = self.max_speed
        self.agression = agression
        self.gap = np.random.rand()*2*agression + min_gap
        self.switch_delay = int(30/self.model.time_step)
        self.switched = self.switch_delay

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
        self.switched -= 1
        self.switched = max(0, self.switched)
        FRONT, BACK = self.model.grid.get_neighbors(self)
        rf, mf, lf = FRONT
        rb, mb, lb = BACK
        self.match_speed(mf)
        # print(FRONT, BACK)
        # print(self.pos, self.speed)
        # print('-------')
        while True:
            # gaps, times, min_r, min_l = self.compute_pars(FRONT, BACK)
            can_left = lf[0]-self.pos[0] > self.gap*self.speed*self.agression and self.pos[0]-lb[0]> 0.5*self.speed*self.agression and self.pos[1] < (self.model.lanes - 1) and self.switched == 0
            can_right = rf[0]-self.pos[0] > self.gap*self.speed*self.agression and self.pos[0]-rb[0]> 0.5*self.speed*self.agression and self.pos[1] > 0 and self.switched == 0
            if mf[0]-self.pos[0] > self.gap*self.speed:
                if can_right and np.random.rand() < self.agression:
                    self.switched = self.switch_delay
                    self.match_speed(rf)
                    return -1
                if self.speed < self.max_speed:
                    self.check_speed(mf[0]-self.pos[0])
                return 0
            if can_left and can_right:
                if rf[0] < lf[0]:
                    self.match_speed(lf)
                    self.switched = self.switch_delay
                    return 1
                if self.speed < 10:
                    self.match_speed(rf)
                    self.switched = self.switch_delay
                    return -1
                return 1
            if can_left:
                self.match_speed(lf)
                self.switched = self.switch_delay
                return 1
            if can_right and (np.random.rand() > self.agression or self.speed < 10):
                self.match_speed(rf)
                self.switched = self.switch_delay
                return -1
            self.speed -= np.random.rand()*self.model.time_step/self.agression
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

    def match_speed(self, front_car):
        """
        Check if the agent is below their maximum speed
        """
        f_pos, f_speed = front_car
        speed_diff = f_speed - self.speed
        if abs(speed_diff) > 0.8*self.max_speed:
            return
        gap = (f_pos - self.pos[0])/10
        self.speed += speed_diff*self.model.time_step/gap

    def check_speed(self, gap):
        """
        Check if the car has recently braked and otherwise can speed up.
        """
        diff = self.max_speed - self.speed
        space = (gap-self.speed)/self.speed/self.gap/self.agression
        speedup = max(np.random.rand()/self.agression, np.log(diff*space))*self.model.time_step
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
