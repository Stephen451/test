from dash import html, no_update, ctx
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import json
import pandas as pd
import urllib

class GraphPage():
    def __init__(self, app):
        print('creating a new plot page')
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        self.index_dims = []

        self.plt = Plotter(pd.DataFrame([0]).set_index(0), [0])
        self.available_plots = self.plt.plots._graphs(self.plt.plots)
        self.available_plots.sort()

        self.file_path = None
        self.data_source = Provider(self.file_path)
        self.data = self.data_source.data
        self.rm = self.data_source.rm
        self.Dim1 = self.data_source.get_dimensions()
        self.Dim2 = self.data_source.get_dimensions()
        self.Dim3 = self.data_source.get_dimensions()
        self.Dim4 = self.data_source.get_dimensions()

        self.reduction_types = [{'label': " ", 'value': ""}, {'label': "mean", 'value': "mean"}, 
            {'label': "std", 'value': "std"}, {'label': "p90", 'value': "p90"}, {'label': "p10", 'value': "p10"}]

    def config_callbacks(self):
        
        @self.app.callback(Output('hidden-div', component_property='children'),
             [Input('url', 'search')])  #, Input('url', 'searchdata')]) 
        def display_page(search):
            parsed = urllib.parse.urlparse(search)
            parsed_dict = urllib.parse.parse_qs(parsed.query)

            self.file_path = parsed_dict['path'][0]

            return json.dumps('page_contenttt')
        
        @self.app.callback(
        Output(component_id='main_plot', component_property= 'figure'),
        Output(component_id='graph_type', component_property= 'options'),
        Output(component_id='graph_type', component_property= 'value'),
        Input(component_id='dropdown', component_property= 'value'),
        Input(component_id='Dim1', component_property= 'value'),
        Input(component_id='Dim2', component_property= 'value'),
        Input(component_id='Dim3', component_property= 'value'),
        Input(component_id='Dim4', component_property= 'value'),
        Input(component_id='graph_type', component_property='value'),
        Input(component_id='dim2_reduce', component_property='value'),
        )
        def set_graph(dropdown_value, Dim1, Dim2, Dim3, Dim4, graph_type, dim2_reduce):
            self.refresh_data()
            triggered_id = ctx.triggered_id
            if triggered_id != 'graph_type':
                print(dropdown_value)
                self.index_dims = [i for i in [Dim1, Dim2, Dim3, Dim4] if i]

                #If the same index is selected twice, don't try to plot anything
                if len(self.index_dims) != len(set(self.index_dims)):
                    return no_update

                #If wells in the index dims, remove it temporarily for the RunMetrics API
                self.temp_dims = [i for i in self.index_dims if i != 'wells']

                try:
                    self.df = self.data_source.get_df(dropdown_value, index_dims=self.temp_dims) #, well_regex='^[ED]6-tile0-0')
                except Exception as e:
                    self.df = pd.DataFrame()

                #Apply reductions
                if dim2_reduce:
                    self.filtered_df, self.filtered_index_dims = self.data_source.filter_df(self.df, self.index_dims[1], dim2_reduce, self.index_dims)
                else:
                    self.filtered_df = self.df
                    self.filtered_index_dims = self.index_dims

                self.plt = Plotter(data=self.filtered_df, index_dims=self.filtered_index_dims)

                fig = self.plt.plot(dropdown_value, graph_type)

            elif triggered_id == 'graph_type':
                fig = self.plt.plot(dropdown_value, graph_type)

            # Now check the plotter dropdown list for accuracy
            self.available_plots = self.plt.plots._graphs(self.plt.plots)
            self.available_plots.sort()
            if graph_type not in self.available_plots:
                graph_type = "Scatter"

            return fig, self.available_plots, graph_type
        
        @self.app.callback(
            Output(component_id='Dim1', component_property= 'value'),
            Output(component_id='Dim2', component_property= 'value'),
            Output(component_id='Dim3', component_property= 'value'),
            Output(component_id='Dim4', component_property= 'value'),
            Input(component_id='dropdown', component_property='value')
        )
        def update_data_values(dropdown):
            self.refresh_data()
            if dropdown in self.rm.data_dims:
                dims = self.rm.data_dims[dropdown]
            else:
                dims = self.rm.metric_dims[dropdown]
            new_dims = ['wells']
            for i in range(0,3):
                if len(dims) > i:
                    new_dims.append(dims[i])
                else:
                    new_dims.append("")
            return new_dims[0], new_dims[1], new_dims[2], new_dims[3]
    
        @self.app.callback(
            Output(component_id='Dim1', component_property= 'options'),
            Output(component_id='Dim2', component_property= 'options'),
            Output(component_id='Dim3', component_property= 'options'),
            Output(component_id='Dim4', component_property= 'options'),
            Input(component_id='dropdown', component_property='value'),
        )
        def update_data_labels(dropdown):
            self.refresh_data()
            if dropdown in self.rm.data_dims:
                dims = self.rm.data_dims[dropdown]
            else:
                dims = self.rm.metric_dims[dropdown]

            new_dims = []

            for i in dims:
                for transforms in self.data_source.allowable_transforms.keys():
                    if i == transforms[0] and transforms[1] not in dims:
                        new_dims.append(transforms[1])
            new_dims.extend(dims)

            new_dims = self.data_source.get_dimensions(new_dims)

            return new_dims, new_dims, new_dims, new_dims

    def set_layout(self):
        layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
        html.Div(id='hidden-div', style={'display':'none'}),
        # dcc.Location(id='url', refresh=False),
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
        dcc.Dropdown( id = 'Dim4',
            options = self.Dim4,
            value = self.Dim4[0]['value']),
        dcc.Dropdown( id = 'dim2_reduce',
            options = self.reduction_types,
            value = self.reduction_types[0]['value']),
        ])

        return layout

    def refresh_data(self):

        if self.file_path != self.data_source.path:
            self.data_source = Provider(self.file_path)
            self.data = self.data_source.data
            self.rm = self.data_source.rm
            self.Dim1 = self.data_source.get_dimensions()
            self.Dim2 = self.data_source.get_dimensions()
            self.Dim3 = self.data_source.get_dimensions()
            self.Dim4 = self.data_source.get_dimensions()