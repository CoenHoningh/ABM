from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from lane_canvas import SimpleCanvas

# Import the implemented classes
from modelgrid import RoadSim


COLORS = {-1: "pink",
          0: "green",
          1: "#ccff33",
          2: "yellow",
          3: "orange",
          4: "#cc6600",
          5: "red",
          6: "red",
          7: "red",
          8: "red",
          9: "red"}


def agent_portrayal(agent):
    """
    Properties of the agent visualization.
    """
    portrayal = {"Shape": "circle",
                 "Color": COLORS[min((agent.max_speed-agent.speed)//2, 9)],
                 "Filled": "true",
                 "r": 6}
    return portrayal


number_of_lanes = 3
length = 1000


grid = SimpleCanvas(agent_portrayal, 300, 1000)


# Create a dynamic linegraph
chart = ChartModule([{"Label": "Avg_speed",
                      "Color": "green"}],
                    data_collector_name='datacollector')


# Create the server, and pass the grid and the graph
server = ModularServer(RoadSim,
                       [grid],
                       "Road sim yo",
                       {"lanes": number_of_lanes,
                        "length": length,
                        "spawn":
                            UserSettableParameter('slider',
                                                  "Spawn Chance",
                                                  0.5, 0.0, 1.0, 0.05),
                        "speed":
                            UserSettableParameter('slider',
                                                  'Maximum speed',
                                                  130, 0.0, 200, 1.0)})

server.port = 8526

server.launch()
