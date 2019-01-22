"""
Module for data collection and processing routines.
"""
import numpy as np


def avg_speed(model):
    """
    Computes the average speed of all cars.
    """
    speeds = [agent.speed for agent in model.schedule.agents]
    return np.average(speeds)


def lane_speeds(model):
    """
    Computes the average speed of all cars per lane.
    """
    speeds = [[]]*model.lanes
    for agent in model.schedule.agents:
        speeds[agent.lane].append(agent.speed)
    return [np.mean(x) for x in speeds]
