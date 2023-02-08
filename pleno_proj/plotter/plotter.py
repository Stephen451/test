import pandas as pd
import numpy as np
from plotter.enum_plots import PLOT2D, PLOT3D, PLOT4D  #noqa
import plotly.graph_objects as go
from typing import Union



class Plotter:
    def __init__(self, data: Union[pd.DataFrame, np.ndarray], index_dims: list[str]):
        self.data = data
        self.index_dims = index_dims
        self.num_dims = len(index_dims)
        self.choose_plot

    def choose_plot(self):
        #This is where I'll include all the logic for what plots are available given the dropdown selections
        if self.num_dims <= 2:
            self.plots = PLOT2D
        elif self.num_dims == 3:
            self.plots = PLOT3D
        elif self.num_dims == 4:
            self.plots = PLOT4D

    def plot(self):
        fig = go.Figure()
        fig.add_trace()
        fig.add_scatter(x = rr.index.get_level_values(0), y = rr[dropdown_value])
        
        # fig = go.Figure([px.imshow(img = df.loc['D6-tile0-0', :])
        #                  ])
        fig.update_layout(title = 'Well Data',
                        xaxis_title = Dim1.capitalize(),
                        yaxis_title = dropdown_value.capitalize()
                        )

        return fig