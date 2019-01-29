from SALib.sample import saltelli
from SALib.analyze import sobol
from mesa.batchrunner import BatchRunner
from modelgrid import *
from IPython.display import clear_output
from tqdm import tqdm



# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['spawn', 'agression', 'min_gap'],
    'bounds': [[0.3, 1], [0.1, 0.9], [0.5, 5]]
}

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 2 #10
max_steps = 100
distinct_samples = 10

# We get all our samples here
param_values = saltelli.sample(problem, distinct_samples)

# Set the outputs
model_reporters={
                "Avg_speed": avg_speed,
                'Cars_in_lane': cars_in_lane}

# READ NOTE BELOW CODE
batch = BatchRunner(RoadSim,
                    max_steps=max_steps,
                    variable_parameters={name:[] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
for i in tqdm(range(replicates)):
    for vals in param_values:
        # Change parameters that should be integers
        vals = list(vals)
        # vals[0] = int(vals[0])
        # vals[3] = int(vals[3])

        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val

        batch.run_iteration(variable_parameters, tuple(vals), count)
        count += 1

        # clear_output()
        # print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')

data = batch.get_model_vars_dataframe()

data.to_csv('Sobol_result.csv', sep='\t', index=False)

print(data)