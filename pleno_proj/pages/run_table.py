from dash import html, no_update, ctx
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import numpy as np
import pandas as pd
import os

# Set the directory path
dir_path = "/srv/nas/"

class GraphPage():
    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()
        
    def config_callbacks(self):
        
        @self.app.callback(
        Output(component_id='run_table', component_property= 'figure'),
        Input(component_id='dropdown', component_property= 'value')
        )
        def set_graph(dropdown_value, Dim1, Dim2, Dim3, graph_type):
            triggered_id = ctx.triggered_id
            if triggered_id != 'graph_type':
                print(dropdown_value)
                self.index_dims = [i for i in [Dim1, Dim2, Dim3] if i]

                if len(self.index_dims) != len(set(self.index_dims)):
                    return no_update

                try:
                    self.df = self.data_source.get_df(dropdown_value, index_dims=self.index_dims, well_regex='^[ED]6-tile0-0')
                    x = self.df.index.get_level_values(0) 
                    y = self.df[dropdown_value]
                except Exception as e:
                    df = pd.DataFrame()
                    x = [0, 1]
                    y = [0, 1]

                if 'wells' in self.df.index.names:
                    self.index_dims.extend(['wells'])

                self.plt = Plotter(data=self.df, index_dims=self.index_dims)

                fig = self.plt.plot(dropdown_value, graph_type)

            elif triggered_id == 'graph_type':
                fig = self.plt.plot(dropdown_value, graph_type)

            return fig
        
    def set_layout(self):
        layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
            options = self.data,
            value = self.data[0]['value']),
        dcc.Graph(id = 'run_table'),
        ])

        return layout

    def get_run_data(self):
        # Create an empty list to store the folder information
        folder_info = []

        # Loop through each folder in the directory
        for folder in os.listdir(dir_path):
            folder_path = os.path.join(dir_path, folder)
            # Check if the item in the directory is a folder
            if os.path.isdir(folder_path):
                # Get the folder's date created
                date_created = os.path.getctime(folder_path)
                # Add the folder's information to the list
                folder_info.append({"Folder Name": folder, "Date Created": date_created})

        # Create a pandas data frame from the folder information list
        folder_df = pd.DataFrame(folder_info)

        return folder_df