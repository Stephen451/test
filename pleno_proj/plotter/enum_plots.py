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

class PLOT2D(str, Enum):
    SCATTER = StandardSyntax(px.scatter)
    BAR = px.bar
    TABLE = ff.create_table
    DENSITY = px.density_heatmap
    HISTOGRAM = px.histogram
    BOX = px.box

    def __str__(self) -> str:
        return self.value


class PLOT3D(str, Enum):
    CONTOUR = go.Contour
    HEATMAT = px.imshow
    MESH = go.Mesh3d
    SCATTER = px.scatter_3d
    SURFACE = go.Surface
    TABLE = go.Table

    def __str__(self) -> str:
        return self.value

class PLOT4D(str, Enum):
    SCATTER = px.scatter_3d
    TABLE = go.Table
    

    def __str__(self) -> str:
        return self.value

