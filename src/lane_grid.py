""" Module for mixed systems with both a discrete and continuous axis """
import numpy as np


class LaneSpace:
    """
    The LaneSpace class creates a discrete number of horizontal lanes,
    each with a continuous length. This can be used to model systems
    where one axis is best represented by a discrete integer value e.g.
    the lanes on a highway. Whilst the other axis is continuous in natue,
    such as the distance traveled on the highway.

    The postion and speed of each agent is stored in a numpy array, indexed
    to the unique_id of the agent. Although this limits the number of agents
    it allows for extremely quick operation as no lists or dictionaries have
    to be maintained.

    Properties:
        positions: A (n, l) numpy array which contains the horizontal position
            of each agent. These positions are indexed by the current lane and
            unique id of the agent, where n is simply the lane number and
            l the unique_id of an agent modulo the length of the space.
            If multiple agents can occupy a meter the scale argument can be
            used to increase the capacity of each lane. The position index
            of each agent should then computed modulo the length of the scaled
            system.
        speeds: A (n, l) numpy array which contains the speeds of each agent,
            indexed following the same rules as the positions array.
    """

    def __init__(self, length, lanes, time_step=1, scale=1):
        """
        Initialize the highway space.

        Args:
            length: The length of the highway in meters
            lanes: The number of lanes
            scale: Value to scale the position array by, relative to
                the system length. Can be used to increase the capacity
                of decrease memory usage.
        """
        self._init_len = length
        self._scale = scale
        self.length = int(length*scale)
        self.lanes = lanes
        self.time_step = time_step
        self.positions = np.full((self.lanes, self.length), np.nan)
        # self.speeds = np.full((self.lanes, self.length), np.nan)

    def place_agent(self, agent):
        """
        Place an agent on the highway space.

        Args:
            agent: an agent instance which should have a speed and
                index property. Representing the agent speed and unique_id
                modulo length respectively
        """
        loc, lane = agent.pos
        if np.isnan(self.positions[lane, agent.index]):
            self.positions[lane, agent.index] = loc
            # self.speeds[lane, agent.index] = agent.speed
            agent.pos = (loc, lane)
            return True
        if len(agent.model.cars) > self.length:
            print('agent index not empty')
            print('rescaling array')
            self._resize_grid()
        else:
            print('index not empty but space available')
        return False

    def _resize_grid(self):
        self._scale = self._scale * 2
        new_len = int(self._init_len*self._scale)
        new_pos = np.full((self.lanes, new_len), np.nan)
        new_pos[:, :self.length] = self.positions
        self.positions = new_pos.copy()
        self.length = new_len

    def move_agent(self, agent, lane_switch):
        """
        Move an agent to a new postition on the highway space.

        Args:
            agent: An agent instance which is expected to have the current
                postition as a 2-tuple pos, the speed, and the postion index.
            lane_switch: An integer which indicates the next lane of an agent.
                -1 moves a lane to the right, 0 retains the current lane, and
                1 moves a lane to the left.

        Returns:
            False: if the agent has moved out of the defined space
            True: if the move was succesfull.
        """
        loc, lane = agent.pos
        if loc+agent.speed > agent.model.length:
            return False
        new_loc = loc + (agent.speed * self.time_step)
        new_lane = lane + lane_switch
        if lane_switch:
            self.positions[lane, agent.index] = np.nan
            # self.speeds[lane, agent.index] = np.nan
        self.positions[new_lane, agent.index] = new_loc
        # self.speeds[new_lane, agent.index] = agent.speed
        agent.pos = (new_loc, new_lane)
        return True

    def remove_agent(self, agent):
        """
        Remove an agent from the highway space.

        Args:
            agent: An agent instance to be removed from the space.
        """
        lane = agent.pos[1]
        self.positions[lane, agent.index] = np.nan
        # self.speeds[lane, agent.index] = np.nan

    def get_neighbors(self, agent):
        """
        Returns the postition and speed of all 6 possible neighbours of a car:
        the cars in front and behind on the left, current, and right lane.
        Used to compute the utility of the possible move of an agent.

        Args:
            agent: An agent instance with a speed and pos property.

        Returns:
            fronts: A (3,2) list which contains the position and speed of
                the cars in front on the right, current, and left lane.
                If no cars are in front, or the car is on one of the outer
                most lanes, -1 is returned for both values.
            backs: A (3,2) list which has the postition and speed of the
                cars behind.
        """
        fronts = [agent.model.length*2, agent.model.length*2, agent.model.length*2]
        backs = [-100, -100, -100]
        for i in range(0, 3):
            j = agent.pos[1]-1+i
            if 0 <= j < self.lanes:
                f_ind = self.positions[j][(agent.pos[0] < self.positions[j]).nonzero()]
                b_ind = self.positions[j][(agent.pos[0] > self.positions[j]).nonzero()]
                if len(f_ind):
                    fronts[i] = np.minimum.reduce(f_ind)
                if len(b_ind):
                    backs[i] = np.maximum.reduce(b_ind)
        return fronts, backs
