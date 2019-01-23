"""
Module for data collection and processing routines.
"""
import numpy as np


def avg_speed(model):
    """
    Computes the average speed of all cars.
    """
    speeds = [agent.speed for agent in model.schedule.agents]
    return np.average(speeds)*3.6*model.gridsize


def lane_speeds(model):
    """
    Computes the average speed of all cars per lane.
    """
    speeds = [[] for a in range(model.lanes)]
    for agent in model.schedule.agents:
        speeds[agent.y].append(agent.speed)
    return [np.average(x)*3.6*model.gridsize for x in speeds]


def cars_in_lane(model):
    nums = [0 for a in range(model.lanes)]
    for agent in model.schedule.agents:
        nums[agent.y] += 1
    return nums
