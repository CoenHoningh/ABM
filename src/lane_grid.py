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

    def __init__(self, lanes, length, scale=1):
        """
        Initialize the highway space.

        Args:
            lanes: The number of lanes
            length: The length of the highway in meters
            scale: Value to scale the position array by, relative to
                the system length. Can be used to increase the capacity
                of decrease memory usage.
        """
        self.lanes = lanes
        self.length = int(length*scale)
        print(f"Using {self.length*self.lanes*16/1000000}MB of memory")
        self.positions = np.full((self.lanes, self.length), np.nan)
        self.speeds = np.full((self.lanes, self.length), np.nan)

    def place_agent(self, agent, pos):
        """
        Place an agent on the highway space.

        Args:
            agent: an agent instance which should have a speed and
                index property. Representing the agent speed and unique_id
                modulo length respectively
            pos: The position the agent is placed at, should be a 2-tuple
                containing the horizontal position and lane number.
        """
        loc, lane = pos
        self.positions[lane, agent.index] = loc
        self.speeds[lane, agent.index] = agent.speed
        agent.pos = (loc, lane)

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
        if loc+agent.speed > self.length:
            return False
        if lane_switch:
            self.positions[lane, agent.index] = np.nan
            self.speeds[lane, agent.index] = np.nan
        self.positions[lane+lane_switch, agent.index] = (loc+agent.speed)
        self.speeds[lane+lane_switch, agent.index] = (agent.speed)
        return True

    def remove_agent(self, agent):
        """
        Remove an agent from the highway space.

        Args:
            agent: An agent instance to be removed from the space.
        """
        lane = agent.pos[1]
        self.positions[lane, agent.index] = np.nan
        self.speeds[lane, agent.index] = np.nan

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
        fronts = [(-1, -1) for x in range(3)]
        backs = [(-1, -1) for x in range(3)]
        for i in range(0, 3):
            j = agent.pos[1]-1+i
            if 0 <= j < self.lanes:
                f_ind = np.nonzero(agent.pos[0] < self.positions[j])
                b_ind = np.nonzero(agent.pos[0] > self.positions[j])
                if np.shape(f_ind)[1]:
                    f_pos = self.positions[j][f_ind]
                    f_speed = self.speeds[j][f_ind]
                    f = np.argmin(f_pos)
                    fronts[i] = (f_pos[f], f_speed[f])
                if np.shape(b_ind)[1]:
                    b_pos = self.positions[j][b_ind]
                    b_speed = self.speeds[j][f_ind]
                    b = np.argmax(b_pos)
                    backs[i] = (b_pos[b], b_speed[b])
        return fronts, backs
