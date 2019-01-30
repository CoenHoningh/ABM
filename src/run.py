from tqdm import tqdm
from modelgrid import RoadSim

tot_time = 5000
yo = RoadSim(lanes=3, length=50000, spawn=0.9, agression=0.5, speed=100,
             time_step=0.1, init_time=0)
for a in tqdm(range(tot_time)):
    yo.step()
# speeds = yo.datacollector.get_model_vars_dataframe()
# speeds.to_csv('snelheden.csv')
