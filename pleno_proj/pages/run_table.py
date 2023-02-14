from dash import html, no_update, ctx
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Set the directory path
dir_path = "/mnt/nas/Decoding_Experiments/"

class RunTable():
    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()
        
        self.data = self.get_run_data()
        
    def config_callbacks(self):
        
        @self.app.callback(
        Output(component_id='run_table', component_property= 'figure'),
        Input(component_id='dropdown', component_property= 'value')
        )
        def set_graph(dropdown_value):

            self.plt = Plotter(data=self.data, index_dims=[])

            fig = self.plt.plot(dropdown_value, 'TABLE')

            return fig
        
    def set_layout(self):
        layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
            options = [0,1,2],
            value = 0),
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
                datetime_created = datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S') 
                # Add the folder's information to the list
                folder_info.append({"Run Name": folder, "Date Created": datetime_created})

        # Create a pandas data frame from the folder information list
        folder_df = pd.DataFrame(folder_info)

        return folder_df