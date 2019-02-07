""" Module for mixed systems with both a discrete and continuous axis """
import numpy as np


class LaneSpace:
    """
    The LaneSpace class creates a discrete number of horizontal lanes,
    each with a continuous length. This can be used to model systems
    where one axis is best represented by a discrete integer value e.g.
    the lanes on a highway. Whilst the other axis is continuous in natue,
    such as the distance traveled on the highway.

    The postion of each agent is stored in a numpy array, indexed to the
    unique_id of the agent modulo the size of the lane. Although this limits
    the number of agents it allows for extremely quick operation as no lists
    or dictionaries have to be maintained. If the number of agents exceeds
    array capacity the array is dynamically expanded.

    Attributes:
        length (int): Scaled length of the array; the number of agents
            each lane can contain.
        lanes (int): Number of lanes
        time_step (float): Amount of time to advance each step in seconds.
        positions ((n, l) array): Contains the horizontal position
            of each agent. These positions are indexed by the current lane and
            unique id of the agent, where n is simply the lane number and
            l the unique_id of an agent modulo the length of the space.
            If multiple agents can occupy a meter the scale argument can be
            used to increase the capacity of each lane. The position index
            of each agent should then computed modulo the length of the scaled
            system.
    """

    def __init__(self, length, lanes, time_step=1.0, scale=1.0):
        """
        Initialize the highway space.

        Args:
            length (float): The length of the highway in meters
            lanes (int): The number of lanes
            time_step (float): Amount of time to advance each step in seconds.
            scale (float): Value to scale the position array by, relative to
                the system length. Can be used to increase the capacity
                of decrease memory usage.
        """
        self._init_len = length
        self._scale = scale
        self.length = int(length*scale)
        self.lanes = lanes
        self.time_step = time_step
        self.positions = np.full((self.lanes, self.length), np.nan)

    def place_agent(self, agent):
        """
        Place an agent on the highway space. Determines if the agent index
        is already occupied and increases the scale of the grid if the
        number of agents exceeds the capacity.

        Args:
            agent (obj): an agent instance which should have a speed and
                index property. Representing the agent speed and unique_id
                modulo length respectively

        Returns:
            A boolean value if the placement was succesfull.
        """
        loc, lane = agent.pos
        if np.isnan(self.positions[lane, agent.index]):
            self.positions[lane, agent.index] = loc
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
        """
        Private method to resize the grid if needed. A new array is created
        with double the capacity, the current positions array is copied to
        the first half of this array.
        """
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
            agent (obj): An agent instance which is expected to have the
                current postition as a 2-tuple named pos.
            lane_switch (int): Indicates the next lane of an agent: -1 moves a
                lane to the right, 0 retains the current lane, and 1 moves a
                lane to the left.

        Returns:
            A boolean value if the move was succesfull or not,
            i.e. out of bounds
        """
        loc, lane = agent.pos
        if loc+agent.speed > agent.model.length:
            return False
        new_loc = loc + (agent.speed * self.time_step)
        new_lane = lane + lane_switch
        if lane_switch:
            self.positions[lane, agent.index] = np.nan
        self.positions[new_lane, agent.index] = new_loc
        agent.pos = (new_loc, new_lane)
        return True

    def remove_agent(self, agent):
        """
        Remove an agent from the highway space.

        Args:
            agent (obj): An agent instance to be removed from the space.
        """
        lane = agent.pos[1]
        self.positions[lane, agent.index] = np.nan

    def get_neighbors(self, agent):
        """
        Returns the postition and speed of all 6 possible neighbours of a car:
        the cars in front and behind on the left, current, and right lane.
        Used to compute the utility of the possible move of an agent.

        Args:
            agent (obj): An agent instance with a pos property.

        Returns:
            fronts ([3] list): Contains the positions of the cars in front on
                right, middle and left respectively.
            backs ([3] list): Contains the positions of the cars behind on the
                right, middle and left respectively.
        """
        fronts = [agent.model.length*2,
                  agent.model.length*2,
                  agent.model.length*2]
        backs = [-100, -100, -100]

        for i in range(0, 3):
            j = agent.pos[1]-1+i
            if 0 <= j < self.lanes:
                # All cars in front of the current car
                f_ind = self.positions[j][(agent.pos[0] <
                                           self.positions[j]).nonzero()]
                # All cars behind the current car
                b_ind = self.positions[j][(agent.pos[0] >
                                           self.positions[j]).nonzero()]

                """
                Directly using the min/max ufuncs is considerably faster
                than the amin/amax numpy functions.
                """
                if len(f_ind):
                    # The closest car in front
                    fronts[i] = np.minimum.reduce(f_ind)
                if len(b_ind):
                    # The closest car behind
                    backs[i] = np.maximum.reduce(b_ind)
        return fronts, backs
