from dash import html, no_update, ctx, dash_table, ALL, register_page
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from plotter.plotter import Plotter
from providers.test_provider import Provider
import json
import pandas as pd
import numpy as np
import string
import urllib
from pdc.wellplate import wellplate
from pleno_droid.analytics.plots import BasePlotter, HypercodePlots, Position, HypercodePerformance

FULL_IMAGE_SIZE = 2048 
X_WELLS = 24
Y_WELLS = 16
# potential max size of flows + colors + tiles
FLOWS = 10
COLORS = 4
fake_images = [[[[{} for y in range(Y_WELLS)] for x in range(X_WELLS)] for z in range(COLORS)] for a in range(FLOWS)]
BASE_URL = '/Users/stephenk/pleno-droid/test/20221121_HYP1_KR_96plex_triplicate1_Ham_10x0.3'
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

        self.fake_images = [[[[{} for y in range(Y_WELLS)] for x in range(X_WELLS)] for z in range(COLORS)] for a in range(FLOWS)]

        # automatically resize the wellplate control on page reload.
        self.app.clientside_callback(
            """
            function(href) {
                var w = window.innerWidth;
                var h = window.innerHeight;
                //return [JSON.stringify({'height': h, 'width': w}),w,h];
                console.log("w="+w+",h="+h);
                return [w-100,Math.round(h*0.75),Math.min(Math.round(w/3),Math.round(h*0.55)),
                        w*0.48,Math.round(h*0.75),0];
            }
            """,
            #Output('viewport-container', 'children'),
            Output('ready_plots_wellplate_1', 'width'),
            Output('ready_plots_wellplate_1', 'height'),
            Output('ready_plots_wellplate_1', 'full_pixels'),
            Input('url', 'href'),
        )

    def config_callbacks(self):
        
        @self.app.callback(
            Output('hidden-div1', component_property='children'),
            # Output('ready_plots_wells_1', component_property='options'),
            # Output('ready_plots_wells_1', component_property='value'),
            [Input('url', 'search')])  #, Input('url', 'searchdata')]) 
        def display_page(search):
            parsed = urllib.parse.urlparse(search)
            parsed_dict = urllib.parse.parse_qs(parsed.query)

            self.file_path = parsed_dict['path'][0]
    
            self.refresh_data()

            return json.dumps('page_content')#, self.wells, self.wells[0]['value']

        @self.app.callback(
        Output(component_id='plotting', component_property= 'figure'),
        Input({'type': "ready-sidebar-button", "value": ALL}, "n_clicks"),
        Input(component_id='ready_plots_wellplate_1', component_property='selected_wells_x'),
        Input(component_id='ready_plots_wellplate_1', component_property='selected_wells_y'), prevent_initial_call=True,
        )
        def set_graph(clicked_button, selected_wells_x, selected_wells_y):
            if hasattr(ctx.triggered_id, 'keys'):
                self.graph_type = ctx.triggered_id['value']

            wells = self.selected_wells_to_well_name(selected_wells_x=selected_wells_x, selected_wells_y=selected_wells_y)
            wells = self.list_of_wells_to_regex(wells)

            if self.graph_type:

                plot_func = self.find_plot_func(self.graph_type) 

                fig = plot_func(self.data_source.rm, well_regex = wells)
                fig.update_layout({'width': 700, 'height': 700})

                return fig

    def set_layout(self):
        layout = dbc.Row([
        dbc.Col(width=.7),
        dbc.Col(dbc.Container([
        # html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
        html.Div(id='hidden-div1', style={'display':'none'}),
        dbc.Row([

            dbc.Col([
                # dcc.Dropdown( id = 'ready_plots_wells_1',
                #     options = self.wells,
                #     value = self.wells[0]['value'],
                #     multi=True), 
                    wellplate.Wellplate(id="ready_plots_wellplate_1",  mode='report',  width=1500, height=800,  microns_per_pixel=0.600, # fake value!
                    width_wells=12, height_wells=9, wells_array=self.fake_images, color_slider=0, flow_slider=0,
                    selected_color='red', image_pixels=FULL_IMAGE_SIZE, full_pixels=800, base_url=BASE_URL,
                    single_thumbnail={},current_location={},selected_well_x=0,selected_well_y=0, #selected_wells_x = [0], selected_wells_y = [0],
                    label_margin=30),], 
                    width=6,
            ),
            dbc.Col(
                dcc.Graph(id = 'plotting', style={'width': '40vw', 'height': '40vw'}),
                    width=6),
        ])
        ], fluid=True), width = 10.6),
        dbc.Col(width=.7)
        ])

        return layout

    def selected_wells_to_well_name(self, selected_wells_x, selected_wells_y):
        assert len(selected_wells_x) == len(selected_wells_y)

        wells = []
        for i in range(0, selected_wells_x):
            x = selected_wells_x[i] + 1
            y = string.ascii_uppercase[selected_wells_y[i]]
            wells.append(y+str(x))

        return wells

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
