from mesa.visualization.ModularVisualization import VisualizationElement


class SimpleCanvas(VisualizationElement):
    local_includes = ["lane_canvas.js"]
    portrayal_method = None
    canvas_height = 300
    canvas_width = 5000

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        '''
        Instantiate a new SimpleCanvas
        '''
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Lane_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            x, y = obj.pos
            x = x / model.grid.length * 3
            #y = (y+1) / (model.grid.lanes+1)
            y = (y+1) / (model.grid.lanes+1) /3
            portrayal["x"] = x
            portrayal["y"] = y
            print(portrayal)
            space_state.append(portrayal)
        return space_state

