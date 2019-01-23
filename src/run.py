from modelgrid import RoadSim
import pandas as pd
from tqdm import tqdm

yo = RoadSim(lanes=3, length=10, gridsize=0.5, spawn_chance=0.45, speed=100)
for a in tqdm(range(10005)):
    yo.step()
speeds = yo.datacollector.get_model_vars_dataframe()
posities = yo.datacollector.get_table_dataframe('Positions')

speeds.to_csv('snelheden.csv')
posities.to_csv('posities.csv')
