from SALib.sample import saltelli
from SALib.analyze import sobol
from mesa.batchrunner import BatchRunnerMP
from modelgrid import *
from IPython.display import clear_output
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from itertools import combinations
import seaborn as sns
from matplotlib import rcParams

sns.set()
rcParams.update({'figure.autolayout': True})

# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['spawn', 'agression', 'min_gap'],
    'bounds': [[0.3, 0.8], [0.2, 0.8], [0.5, 2.0]]
}

data = pd.read_csv('./Sobol_result.csv')

print(data)

Si_Speed = sobol.analyze(problem, data['Total_Avg_speed'].as_matrix(), print_to_console=False)
print("\n")
Si_Cars = sobol.analyze(problem, data['Total_Cars_in_lane'].as_matrix(), print_to_console=False)


def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
    fig = plt.gcf()
    fig.set_size_inches(8, 5)

typename = ["Average_speed", "Number_of_cars"]
for i, Si in enumerate((Si_Speed, Si_Cars)):
    # First order
    plot_index(Si, problem['names'], '1', 'First order sensitivity  -  ' + typename[i])
    plt.savefig('plots/First_order_sensitivity_|_' + typename[i] + '.png')
    plt.clf()

    # Second order
    plot_index(Si, problem['names'], '2', 'Second order sensitivity  -  ' + typename[i])
    plt.savefig('plots/Second_order_sensitivity_|_' + typename[i] + '.png')
    plt.clf()

    # Total order
    plot_index(Si, problem['names'], 'T', 'Total order sensitivity  -  ' + typename[i])
    plt.savefig('plots/Total_order_sensitivity_|_' + typename[i] + '.png')
    plt.clf()
