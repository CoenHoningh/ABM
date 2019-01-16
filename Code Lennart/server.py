from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

# Import the implemented classes
import IPython
import os
import sys
from modelgrid import *

# Change stdout so we can ignore most prints etc.
#orig_stdout = sys.stdout
#sys.stdout = open(os.devnull, 'w')
#IPython.get_ipython().magic("run Mesa_introduction.ipynb")
#sys.stdout = orig_stdout

# You can change this to whatever ou want. Make sure to make the different types
# of agents distinguishable
def agent_portrayal(agent):
    portrayal = {"Shape": "arrowHead",
                "Filled": "true",
                "Layer": 2,
                "Color": "green",
                "Filled": "true",
                "heading_x": 1,
                "heading_y": 0,
                "text": "hoi",
                "text_color": "white",
                "scale": 0.8,}
    return portrayal

number_of_lanes=3
length=500



# Create a grid of 20 by 20 cells, and display it as 500 by 500 pixels
grid = CanvasGrid(agent_portrayal, length, number_of_lanes, 5000, 50)

# Create a dynamic linegraph
# chart = ChartModule([{"Label": "Sheep",
#                       "Color": "green"},
#                       {"Label": "Wolves",
#                       "Color": "red"}],
#                     data_collector_name='datacollector')


# Create the server, and pass the grid and the graph
server = ModularServer(RoadSim,
                       [grid],
                       "WolfSheep Model",
                       {"lanes":number_of_lanes, "length":length})

server.port = 8522

server.launch()
