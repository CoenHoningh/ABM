from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

# Import the implemented classes
from modelgrid import RoadSim


COLORS = {-1: "pink",
          0: "green",
          1: "#ccff33",
          2: "yellow",
          3: "orange",
          4: "#cc6600",
          5: "red"}


def agent_portrayal(agent):
    """
    Properties of the agent visualization.
    """
    portrayal = {"Shape": "arrowHead",
                 "Layer": 10,
                 "Color": COLORS[agent.max_speed-agent.speed],
                 "Filled": "true",
                 "heading_x": 1,
                 "heading_y": 0,
                 "text": agent.unique_id,
                 "text_color": "white",
                 "scale": 10.0}
    return portrayal


number_of_lanes = 3
length = 1000


# grid = CanvasGrid(agent_portrayal, length,
#                   number_of_lanes, 5000, 30 * number_of_lanes)


# Create a dynamic linegraph
chart = ChartModule([{"Label": "Avg_speed",
                      "Color": "green"}],
                    data_collector_name='datacollector')


# Create the server, and pass the grid and the graph
server = ModularServer(RoadSim,
                       [chart],
                       "Road sim yo",
                       {"lanes": number_of_lanes,
                        "length": length,
                        "spawn_chance":
                            UserSettableParameter('slider',
                                                  "Spawn Chance",
                                                  0.5, 0.0, 1.0, 0.05),
                        "speed":
                            UserSettableParameter('slider',
                                                  'Maximum speed',
                                                  130, 0.0, 200, 1.0)})

server.port = 8526

server.launch()
