import pandas as pd
import numpy as np
from plotter.enum_plots import PLOT2D, PLOT3D, PLOT4D  #noqa
import plotly.graph_objects as go
from typing import Union

class DataFormatter:
    def __init__(self, data: pd.DataFrame, index_dims: list[str]):
        self.data = data
        self.index_dims = index_dims
        self.shape = self.data.shape
        self.index_shape = len(self.data.index.names)
        
        self.statistical = False
        
        #If the requested dimensionality > dimensionality of the underlying data, reduce the request
        if len(self.index_dims) > len(self.data.index.names):
            self.filtered_dims = self.index_dims[0:len(self.data.index.names)]
        else:
            self.filtered_dims = self.index_dims
        self.n_dim = len(self.filtered_dims)

        #if the order of requested dimensions don't match the current layout of the data, reshape the dataframe
        if self.data.index.names[0:len(self.filtered_dims)] != self.filtered_dims:
            self.filtered_data = self.reorder(self.data, self.filtered_dims)
        else:
            self.filtered_data = self.data

        #If the requested dimensionality < dimensionality of the underlying data, reduce the dimensionality of the data
        if self.n_dim != self.index_shape:
            self.filtered_data = self.reduct(self.filtered_data, self.filtered_dims)

    def reduct(self, data: pd.DataFrame, index_dims: list[str]):

        data = data.groupby(level=index_dims).mean()
        return data

    def reorder(self, data: pd.DataFrame, index_dims: list[str]):
        #reshape a dataframe to match a requested dimension array
        current_dims = list(data.index.names).copy()
        future_dims = []

        for i in index_dims:
            if i in current_dims:
                future_dims.append(i)
                current_dims.remove(i)
        future_dims.extend(current_dims)
        data = data.reorder_levels(future_dims)

        return data

    def format(self):
        """pass in a list of dimensions and use knowledge of plotly's API to map them to usual plotly args"""

        """number of dimensions
        Length of dimension data
        order of dimensions
        statistical distribution y/n
        
        """

        raise NotImplementedError


class Plotter:
    def __init__(self, data: Union[pd.DataFrame, np.ndarray], index_dims: list[str]):
        self.data = data
        self.index_dims = index_dims
        formatter = DataFormatter(self.data, self.index_dims)

        self.choose_plot()

    def choose_plot(self):
        #This is where I'll include all the logic for what plots are available given the dropdown selections
        num_dims = len(self.index_dims)
        if num_dims <= 2:
            self.plots = PLOT2D
        elif num_dims == 3:
            self.plots = PLOT3D
        elif num_dims == 4:
            self.plots = PLOT4D

        self.allowed_plots = self.plots._graphs(self.plots)

    def sanity_check_plot_choice(self, plot_func):
        if np.max(self.data.shape) > 1000:
            plot_func = self.plots.SCATTER
        return plot_func

    def plot(self, dropdown, graph_name: str = None):
        fig = go.Figure()
        if graph_name and graph_name in self.allowed_plots:
            plot_type = graph_name
        else:
            plot_type = self.allowed_plots[-1]
        plot_func = getattr(self.plots, plot_type)
        # plot_func = self.sanity_check_plot_choice(plot_func)

        traces = []
        for well, data in self.data.groupby(level=0):
            new_trace = plot_func.copy()
            new_trace['x'] = data.index.get_level_values(1)
            new_trace['y'] = data[dropdown]
            new_trace['name'] = well
            traces.append(new_trace)
        
        fig.add_traces(traces)
            
        # fig = go.Figure([px.imshow(img = df.loc['D6-tile0-0', :])
        #                  ])
        fig.update_layout(title = 'Well Data',
                        xaxis_title = self.index_dims[0].capitalize(),
                        yaxis_title = dropdown.capitalize()
                        )

        return fig
