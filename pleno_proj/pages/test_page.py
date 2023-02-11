from dash import html, no_update, ctx
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import numpy as np
import pandas as pd

class GraphPage():
    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        self.index_dims = []

        plotter = Plotter(pd.DataFrame([0]).set_index(0), [0])
        self.available_plots = plotter.plots._graphs(plotter.plots)
        self.available_plots.sort()

        self.data_source = Provider()
        self.data, self.tt = self.data_source.load_data()
        self.Dim1 = self.data_source.get_dimensions()
        self.Dim2 = self.data_source.get_dimensions()
        self.Dim3 = self.data_source.get_dimensions()
        self.wells = self.data_source.get_wells()

        
    def config_callbacks(self):
        
        @self.app.callback(
        Output(component_id='main_plot', component_property= 'figure'),
        Input(component_id='dropdown', component_property= 'value'),
        Input(component_id='Dim1', component_property= 'value'),
        Input(component_id='Dim2', component_property= 'value'),
        Input(component_id='Dim3', component_property= 'value'),
        Input(component_id='graph_type', component_property='value'),
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
                    new_dims = ['wells']
                    new_dims.extend(self.index_dims)
                    self.index_dims = new_dims

                self.plt = Plotter(data=self.df, index_dims=self.index_dims)

                fig = self.plt.plot(dropdown_value, graph_type)

            elif triggered_id == 'graph_type':
                fig = self.plt.plot(dropdown_value, graph_type)

            return fig
        
        @self.app.callback(
            Output(component_id='Dim1', component_property= 'value'),
            Output(component_id='Dim2', component_property= 'value'),
            Output(component_id='Dim3', component_property= 'value'),
            Input(component_id='dropdown', component_property='value')
        )
        def update_data_values(dropdown):
            if dropdown in self.tt.data_dims:
                dims = self.tt.data_dims[dropdown]
            else:
                dims = self.tt.metric_dims[dropdown]
            new_dims = []
            for i in range(0,3):
                if len(dims)>i:
                    new_dims.append(dims[i])
                else:
                    new_dims.append("")
            return new_dims[0], new_dims[1], new_dims[2]
    
        @self.app.callback(
            Output(component_id='Dim1', component_property= 'options'),
            Output(component_id='Dim2', component_property= 'options'),
            Output(component_id='Dim3', component_property= 'options'),
            Input(component_id='dropdown', component_property='value')
        )
        def update_data_labels(dropdown):
            if dropdown in self.tt.data_dims:
                dims = self.tt.data_dims[dropdown]
            else:
                dims = self.tt.metric_dims[dropdown]

            new_dims = []

            for i in dims:
                for transforms in self.data_source.allowable_transforms.keys():
                    if i == transforms[0] and transforms[1] not in dims:
                        new_dims.append(transforms[1])
            new_dims.extend(dims)

            new_dims = self.data_source.get_dimensions(new_dims)

            return new_dims, new_dims, new_dims

    def set_layout(self):
        self.app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
        dcc.Dropdown( id = 'graph_type',
            options = self.available_plots,
            value = 'SCATTER'),
        dcc.Graph(id = 'main_plot'),
        dcc.Dropdown( id = 'dropdown',
            options = self.data,
            value = self.data[0]['value']),
        dcc.Dropdown( id = 'Dim1',
            options = self.Dim1,
            value = self.Dim1[0]['value']),
        dcc.Dropdown( id = 'Dim2',
            options = self.Dim2,
            value = self.Dim2[0]['value']),
        dcc.Dropdown( id = 'Dim3',
            options = self.Dim3,
            value = self.Dim3[0]['value']),
        ])
