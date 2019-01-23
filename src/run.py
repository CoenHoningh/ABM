from modelgrid import RoadSim
import pandas as pd

yo = RoadSim()
for a in range(1005):
    yo.step()
speeds = yo.datacollector.get_model_vars_dataframe()
posities = yo.datacollector.get_table_dataframe('Positions')

speeds.to_csv('snelheden.csv')
posities.to_csv('posities.csv')
