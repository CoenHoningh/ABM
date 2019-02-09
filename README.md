# AABMSHTC
An agent based model for the simulation of highway traffic congestion.
![Demo simulation run](gifs/norm_aggressie.gif)
## Visualization Usage
There are multiple ways of using the model. An interactive server can
be started by changing to the source directory and running the server.py
file.
```
cd src
python server.py
```
This will open up a browser window where parameters can be selected,
and the result visualized.
![Interactive server](gifs/server.png)
Use the sliders to change the initial conditions and press reset to commit
the changes to the model, finally press start to begin the run.
The colors of the dots represent the speed, with bright green indicating
that a car is at its maximum speed, and dark red indicating that a car is
severly slowed.
The line graph below shows how the average speed and number of cars per lane
varies over time.

## Interactive data analysis
Along with the visual browser app is is also possible to perform individual runs through
the `interactive_data_analysis` jupyter notebook, included in the `Data-analysis` directory.
This notebook allows the user to specify parameters and perform a run for a selected number of timesteps.
After the run is complete the results can be graphed through the `plot()` method.

## Sensitivity analysis: OFAT
Due to the length of sensitivity analysis runs a python script is provided instead of a notebook.
The `batch_run.py` file allows the user to perform an OFAT like analysis by running through all posible
combinations in the `br_params` dictionary. The results are put in a `csv` file whose name is also
specified in the script. The created `csv` file can then be used for further data analysis in
the `Interactive_OFAT_analysis` jupyter notebook, located in the `Data-analysis/OFAT` directory.
In this notebook examples are provided of both 2D and 3D scatter plots which allow for quick
visual analysis of the results.

## Sensitivity analysis: Sobol
Finally, Sobol analysis can be performed through the `SA.py` file in the `src` directory.
As it is the most expensive analysis only a python script is provided. The variables are specified
in the `problem` dictionary, along with the bounds of these variables. The script exports the figures
in the `src/plots` directory, along with a `Sobol_result.csv` file to allow the user to create their
own plots.


# Modifiying the code
In addition to the provided analysis tools, it is also possible for the user to create their own
analysis or even change the model itself. All model source files in the `src` directory are thourougly
comented, providing the user with information on each class and method.
