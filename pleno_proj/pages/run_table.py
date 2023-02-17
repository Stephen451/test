from dash import html, no_update, ctx
from dash import dcc, dash_table
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
import numpy as np
import pandas as pd
import os
from datetime import datetime
from urllib.request import pathname2url, quote
from pathlib import Path

# Set the directory path
# dir_path = "/mnt/nas/Decoding_Experiments/"
dir_path = Path("/Volumes/bio_data/Decoding_Experiments")
dir_path2 = Path("/Volumes/bio_data/Decoding_Experiments_Processed")

class RunTable():
    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()
        
        self.data = self.get_run_data()
        
    # def config_callbacks(self):
        
        # @self.app.callback(
        # Output(component_id='run_table', component_property= 'figure'),
        # Input(component_id='dropdown', component_property= 'value')
        # )
        # def set_graph(dropdown_value):

        #     self.plt = Plotter(data=self.data, index_dims=[])

        #     fig = self.plt.plot(dropdown_value, 'TABLE')

        #     return fig
        
    def set_layout(self):
        layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
            options = [0,1,2],
            value = 0),
        # dcc.Graph(id = 'run_table'),
        dash_table.DataTable(
        id="table",
        data=self.data.to_dict("records"),
        columns=[
            {"id": "Run Name", "name": "Run Name", "presentation": "markdown"},
            {"id": "Date Created", "name": "Date Created", "presentation": "markdown"},
            {"id": "Decode", "name": "Decode", "presentation": "markdown"},
            {"id": "Path", "name": "Path", "presentation": "markdown"},
        ],
        markdown_options={"html": True}, 
        sort_action='native',
        filter_action='native'
        )
        
        ])

        return layout

    def get_run_data(self):
        # Create an empty list to store the folder information
        folder_info = []

        # Loop through each folder in the directory
        for i, path in enumerate([dir_path, dir_path2]):
            # for folder in path.glob(([0-9] * 8)*)
            if i == 0:
                for folder in path.glob("[0-9]*8*"):
                    if folder.is_dir():
                        # Get the folder's date created
                        date_created = os.path.getctime(folder)
                        datetime_created = datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S') 
                        # Add the folder's information to the list
                        path_url = quote(str(folder), safe = '')
                        decode = ""
                        folder_info.append({"Run Name": f"<a href='http://127.0.0.1:8051/page-1?path={path_url}' target='_blank'>{folder.stem}</a>", "Date Created": datetime_created, "Decode": decode, "Path": str(folder)})
            elif i == 1:
               for folder in path.glob("*/[0-9]*8*"):
                    if folder.is_dir():
                        # Get the folder's date created
                        date_created = os.path.getctime(folder)
                        datetime_created = datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S') 
                        # Add the folder's information to the list
                        path_url = quote(str(folder), safe = '')
                        decode = folder.parent.stem
                        folder_info.append({"Run Name": f"<a href='http://127.0.0.1:8051/page-1?path={path_url}' target='_blank'>{folder.stem}</a>", "Date Created": datetime_created, "Decode": decode, "Path": str(folder)}) 

        # Create a pandas data frame from the folder information list
        folder_df = pd.DataFrame(folder_info)
        folder_df = folder_df.sort_values('Date Created', ascending=False)

        return folder_df