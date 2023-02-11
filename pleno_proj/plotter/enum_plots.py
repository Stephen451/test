import plotly.graph_objects as go


class StandardSyntax:
    def __init__(self, x, name, y = None, color = None, size = None):
        # NOTE TO FUTURE ME - PICK UP HERE, FIGURE OUT HOW TO TIE PLOT BASESTRINGS TO THESE PARAMS, ADD THESE TO THE DICT AND RETURN TO THE PLOTTER
        self.x = x
        self.name = name
        if y:
            self.y = y
        if color:
            self.color = color
        if size:
            self.size = size

class PLOT2D(str):
    SCATTER = {'type': 'scatter', 'mode': 'markers'}
    BAR = {'type': 'bar'}
    VIOLIN = {'type': 'violin'}
    TABLE = {'type': 'table'}   
    HISTOGRAM = {'type': 'histogram'}  
    BOX = {'type': 'box'}

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs

class PLOT3D(str):
    CONTOUR = {'type': 'contour'}  
    HEATMAP = {'type': 'heatmap'}
    HISTOGRAM = {'type': 'histogram'}  
    VIOLIN = {'type': 'violin'}
    HISTOGRAM = {'type': 'histogram2d'}  
    SCATTER = {'type': 'scatter', 'mode': 'markers'}  
    SCATTER3D = {'type': 'scatter3d', 'mode': 'markers'}  
    SURFACE = {'type': 'surface'}  
    TABLE = {'type': 'table'}  

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs

class PLOT4D(str):
    SCATTER = {'type': 'scatter', 'mode': 'markers'}  
    SCATTER3D = {'type': 'scatter3d', 'mode': 'markers'}  
    TABLE = {'type': 'table'}
    VOLUME ={'type': 'volume'}
    

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs
