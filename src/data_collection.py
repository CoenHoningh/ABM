import numpy as np


def avg_speed(model):
    speeds = [agent.speed for agent in model.schedule.agents]
    return np.average(speeds)


def lane_speeds(model):
    speeds = [[]]*model.lanes
    for agent in model.schedule.agents:
        speeds[agent.lane].append(agent.speed)
    return [np.mean(x) for x in speeds]
