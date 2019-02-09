"""
Module for data collection and processing routines.
"""
import numpy as np


def avg_speed(model):
    """
    Computes the average speed of all cars.
    """
    speeds = [agent.speed for agent in model.schedule.agents]
    return np.average(speeds)*3.6

def avg_slowdown(model):
    """
    Computes the average speed of all cars per lane.
    """
    speeds = [agent.max_speed - agent.speed for agent in model.schedule.agents]
    return np.average(speeds)*3.6

def cars_in_lane(model):
    return len(model.schedule.agents)//model.lanes

def track_params(model):
    return (model.spawn_chance, model.agression, model.lanes)

def track_run(model):
    return model.uid
