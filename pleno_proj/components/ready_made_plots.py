from dash import html, no_update, ctx, dash_table, ALL, register_page
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from plotter.plotter import Plotter
from providers.test_provider import Provider
import json
import pandas as pd
import numpy as np
import urllib
from pleno_droid.analytics.plots import BasePlotter, HypercodePlots, Position, HypercodePerformance

# register_page(__name__)
class ReadyPlots():
    def __init__(self, app):
        print('creating a new plot page')
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        self.file_path = None
        self.available_plots = {}

        # self.reg_functions = BasePlotter.get_registered_functions()
        self.available_plots = {}
        # for ctx in self.reg_functions.keys():
        #     self.available_plots[ctx] = self.reg_functions[ctx]
        for plot_class in [HypercodePerformance, HypercodePlots, Position]:
            self.available_plots[plot_class] = plot_class.get_registered_functions()[plot_class.DISPLAY_NAME]

        self.graph_type = None

        #NOTE ALL IDS SHOULD BE LINKED TO THE PAGE THEY"RE ON FOR CLARITY I.E. id=readyplots_table_1
        self.data_source = Provider(self.file_path)
        self.wells = self.data_source.get_wells()
        self.rm = self.data_source.rm

    def config_callbacks(self):
        
        @self.app.callback(
            Output('hidden-div1', component_property='children'),
            Output('ready_plots_wells_1', component_property='options'),
            Output('ready_plots_wells_1', component_property='value'),
            [Input('url', 'search')])  #, Input('url', 'searchdata')]) 
        def display_page(search):
            parsed = urllib.parse.urlparse(search)
            parsed_dict = urllib.parse.parse_qs(parsed.query)

            self.file_path = parsed_dict['path'][0]
    
            self.refresh_data()

            return json.dumps('page_content'), self.wells, self.wells[0]['value']

        @self.app.callback(
        Output(component_id='plotting', component_property= 'figure'),
        Input({'type': "ready-sidebar-button", "value": ALL}, "n_clicks"),
        Input(component_id='ready_plots_wells_1', component_property='value'), prevent_initial_call=True,
        )
        def set_graph(clicked_button, wells):
            if hasattr(ctx.triggered_id, 'keys'):
                self.graph_type = ctx.triggered_id['value']
            wells = self.list_of_wells_to_regex(wells)

            if self.graph_type:

                plot_func = self.find_plot_func(self.graph_type) 

                fig = plot_func(self.data_source.rm, well_regex = wells)
                fig.update_layout({'width': 700, 'height': 700})

                return fig

    def set_layout(self):
        layout = dbc.Container([
        # html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
        html.Div(id='hidden-div1', style={'display':'none'}),
        dbc.Row([

            dbc.Col(
                dcc.Dropdown( id = 'ready_plots_wells_1',
                    options = self.wells,
                    value = self.wells[0]['value'],
                    multi=True), 
                    width=6,
            ),
            dbc.Col(
                dcc.Graph(id = 'plotting'),#, style={'width': '50vw', 'height': '50vw'}),
                    width=6),
        ])
        ])
        # ])

        return layout

    def refresh_data(self):

        if self.file_path != self.data_source.path:
            self.data_source = Provider(self.file_path)
            # self.data = self.data_source.data
            self.rm = self.data_source.rm
            self.wells = self.data_source.get_wells()
            
    def list_of_wells_to_regex(self, well_list: list):
        """Converts a list of well names into a valid regex expression to use in the analytics classes"""
        # if type(well_list) == str:
        #     return well_list
        # else:
        return r"(?=(" + "|".join(well_list) + r"))"

    def find_plot_func(self, label: str):
        for plot_class in self.available_plots.items():
            plot_funcs = [i['value'] for i in plot_class[1]]
            if label in plot_funcs:
                    return plot_class[0]().__getattribute__(label)
