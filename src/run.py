from tqdm import tqdm
from modelgrid import RoadSim
from mesa.batchrunner import BatchRunnerMP
from mesa.datacollection import DataCollector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import numpy as np
mpl.rcParams['figure.dpi'] = 150
sns.set()


class RunSimulation:

    def __init__(self, lanes=10, length=5000, spawn=0.9, agression=0.5,
                 speed=100, time_step=0.1, min_gap=1.6):
        self.lanes = lanes
        self.length = length
        self.spawn = spawn
        self.agression = agression
        self.speed = speed
        self.time_step = time_step
        self.min_gap = min_gap
        self.sim = RoadSim(self.lanes, self.length, self.spawn, self.agression,
                           self.speed, self.time_step, self.min_gap)

    def run(self, steps=1000):
        for a in tqdm(range(steps)):
            self.sim.step()

    def reset(self):
        self.sim = RoadSim(self.lanes, self.length, self.spawn, self.agression,
                           self.speed, self.time_step, self.min_gap)

    def plot(self):
        mpl.rcParams['figure.dpi'] = 150
        data = self.sim.datacollector.get_model_vars_dataframe()
        x1 = np.array(data['Avg_speed'])
        x2 = np.array(data['Cars_in_lane'])
        y = np.arange(len(x1))/3600
        fig, ax1 = plt.subplots()
        ax1.plot(y, x1, color='b', label='Average speed')
        ax1.set_xlabel('time (h)')
        ax1.set_ylabel('Average speed (km/h)')
        ax1.tick_params('y', colors='b')
        ax2 = ax1.twinx()
        ax2.plot(y, x2, color='r', label='Intensity')
        ax2.set_ylabel('Intensity (cars per lane)')
        ax2.tick_params('y', colors='r')
        plt.show()
