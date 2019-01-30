"""
Module for data collection and processing routines.
"""
import numpy as np


def avg_speed(model):
    """
    Computes the average speed of all cars.
    """
    speeds = [agent.max_speed - agent.speed for agent in model.schedule.agents]
    return np.average(speeds)*3.6


def lane_speeds(model):
    """
    Computes the average speed of all cars per lane.
    """
    speeds = [[] for a in range(model.lanes)]
    for agent in model.schedule.agents:
        speeds[agent.pos[1]].append(agent.speed)
    return [np.average(x)*3.6 for x in speeds]


def cars_in_lane(model):
    return len(model.schedule.agents)

def track_params(model):
    return (model.spawn_chance, model.agression)

def track_run(model):
    return model.uid
