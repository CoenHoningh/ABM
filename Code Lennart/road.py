from mesa import Model
from mesa.space import SingleGrid
from mesa.space import ContinuousSpace
import matplotlib.pyplot as plt

# For a road where the cars can drive continuously over the lanes. This needs a
# restriction for the car on which lane it drives for the y-coordinate.
class RoadContinuous():
    def __init__(self, length=500, lanes=1):
        self.length = length
        self.lanes = lanes

        self.env = ContinuousSpace(self.length, self.lanes * 10, torus=False)

    def visualise(self, plot):
        plot.hlines(range(self.lanes + 1), 0, self.length)


# road1 = RoadContinuous(lanes=5)

# plt.figure(figsize=(2500, 5 * 10), dpi=80)
# road1.visualise(plt)
# plt.show()


# For a road where the lanes are also a grid.
class RoadGrid():
    def __init__(self, length=500, lanes=1):
        self.width = length
        self.height = lanes
        self.env = SingleGrid(self.width, self.height, True)

# road2 = RoadGrid(lanes=3)

# plt.figure(figsize=(2500, 5 * 10), dpi=80)
# road2.visualise(plt)
# plt.show()
