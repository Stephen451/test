from dash import html, no_update, ctx
from dash import dcc, dash_table, register_page
from dash.dependencies import Input, Output, State
from plotter.plotter import Plotter
import numpy as np
import pandas as pd
import os
from datetime import datetime
from urllib.request import pathname2url, quote
from pathlib import Path
from components.base_page import BasePage


# Set the directory path
# dir_path = "/mnt/nas/Decoding_Experiments/"
dir_path = Path("/Volumes/bio_data/Decoding_Experiments")
dir_path2 = Path("/Volumes/bio_data/Decoding_Experiments_Processed")

# register_page(__name__, path='/')

class RunTable(BasePage):
    def __init__(self, app, provider_manager):
        super().__init__(app, provider_manager)
        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()
        
        self.data = self.get_run_data()
        
    def config_callbacks(self):
        
        @self.app.callback(
        Output(component_id='data_path', component_property= 'data'),
        Input(component_id='table', component_property= 'active_cell'),
        State('user_id', 'data'),
        )
        def update_path(active_cell, uid):
            if active_cell:
                row_id = active_cell['row_id']
                # col_id = active_cell['column_id']
                col_id = 'Path'
                folder_path = self.data.loc[row_id,col_id]

                self.provider_manager.get_provider_by_uid(uid).path = folder_path    

                return folder_path
            
            else:
                return ''
        
    def set_layout(self):
        table = dash_table.DataTable(
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
        
        layout = html.Div(id = 'parent', children = [
            html.H1('Styling using html components', id = 'H1', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
            # dropdown,
            table
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
        if "Date Created" in folder_df.columns:
            folder_df = folder_df.sort_values('Date Created', ascending=False, ignore_index=True)
        
        folder_df['id'] = folder_df.index

        return folder_df