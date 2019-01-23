from tqdm import tqdm
from modelgrid import RoadSim

tot_time = 20000
yo = RoadSim(lanes=3, length=10, gridsize=0.5, spawn=[0.3, 0.6], speed=100,
             sim_time=tot_time, init_time=1000)
for a in tqdm(range(tot_time)):
    yo.step()
yo.get_positions()
speeds = yo.datacollector.get_model_vars_dataframe()
posities = yo.datacollector.get_table_dataframe('Positions')

speeds.to_csv('snelheden.csv')
posities.to_csv('posities.csv')
