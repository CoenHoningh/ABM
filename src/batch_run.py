from mesa.batchrunner import BatchRunnerMP
from mesa.datacollection import DataCollector
import pandas as pd
from modelgrid import RoadSim


br_params = {"length": [1000, 5000, 10000, 15000, 20000]}

fixed_params = {"lanes": 3,
                "spawn": 0.5,
                "agression": 0.5,
                "speed": 100,
                "min_gap": 1.0,
                "time_step": 0.1,
                "init_time": 0}

br = BatchRunnerMP(RoadSim,
                   nr_processes=8,
                   variable_parameters=br_params,
                   fixed_parameters=fixed_params,
                   iterations=1,
                   max_steps=50000,
                   model_reporters={"Data Collector":
                                    lambda m: m.datacollector})

if __name__ == '__main__':
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    br_step_data.to_csv("yoyoyo.csv")
