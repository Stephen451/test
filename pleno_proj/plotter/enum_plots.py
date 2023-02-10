import plotly.express as px
from enum import Enum
import plotly.graph_objects as go
import plotly.figure_factory as ff

class StandardSyntax:
    def __init__(self, graph: callable):
        self.graph = graph

    def plot(self, **kwargs):
        """pass in a list of dimensions and use knowledge of plotly's API to map them to usual plotly args"""
        x = kwargs.get('x', None)
        y = kwargs.get('y', None)
        df = kwargs.get('y', None)
        color = kwargs.get('color', None)

class PLOT2D(str):
    SCATTER = go.Scatter
    BAR = go.Bar
    TABLE = go.Table
    DENSITY = go.Densitymapbox
    HISTOGRAM = go.Histogram
    BOX = px.box

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs

class PLOT3D(str):
    CONTOUR = go.Contour
    HEATMAP = px.imshow
    MESH = go.Mesh3d
    SCATTER = px.scatter_3d
    SURFACE = go.Surface
    TABLE = go.Table

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs

class PLOT4D(str):
    SCATTER = px.scatter_3d
    TABLE = go.Table
    

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs
