from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import plotly.graph_objects as go

class GraphPage():
    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

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
        Input(component_id='Dim3', component_property= 'value')
        )
        def set_graph(dropdown_value, Dim1, Dim2, Dim3):
            print(dropdown_value)
            index_dims = [i for i in [Dim1, Dim2, Dim3] if i]
            try:
                df = self.data_source.get_df(dropdown_value, index_dims=index_dims, well_regex='^[BD]6-tile0-0')
                x = df.index.get_level_values(0) 
                y = df[dropdown_value]
            except Exception as e:
                df = None
                x = [0, 1]
                y = [0, 1]
            plt = Plotter(data=df, index_dims=index_dims)

            fig = plt.plot(dropdown_value)
            # fig = go.Figure()
            # # fig.add_trace()
            # for well, data in df.groupby(level=0):
            #     x = data.index.get_level_values(1) 
            #     y = data[dropdown_value]
            #     fig.add_trace(go.Scatter(x = x, y = y, mode='markers', name=well))
            
            # # fig = go.Figure([px.imshow(img = df.loc['D6-tile0-0', :])
            # #                  ])
            # fig.update_layout(title = dropdown_value,
            #                 xaxis_title = "Test",
            #                 yaxis_title = dropdown_value.capitalize()
            #                 )

            return fig

        
        @self.app.callback(
            Output(component_id='Dim1', component_property= 'value'),
            Output(component_id='Dim2', component_property= 'value'),
            Output(component_id='Dim3', component_property= 'value'),
            Input(component_id='dropdown', component_property='value')
        )
        def update_data_dropdown(dropdown):
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
            print(new_dims)
            return new_dims[0], new_dims[1], new_dims[2]
    
    def set_layout(self):
        self.app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
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
        dcc.Graph(id = 'main_plot')
        ])
