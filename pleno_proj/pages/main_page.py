from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import plotly.graph_objects as go

class GraphPage():
    def __init__(self, app):
        self.app = app
        self.app.callback(
        Output(component_id='main_plot', component_property= 'figure'),
        Input(component_id='dropdown', component_property= 'value'),
        Input(component_id='Dim1', component_property= 'value'),
        Input(component_id='Dim2', component_property= 'value'),
        Input(component_id='Dim3', component_property= 'value')
        )(self.graph_update)

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        self.data, self.Dim1, self.Dim2, self.Dim3, self.wells, self.tt = Provider().get_data()
    
    def config_callbacks(self):
        
        @self.app.callback(
        Output(component_id='main_plot', component_property= 'figure'),
        Input(component_id='dropdown', component_property= 'value'),
        Input(component_id='Dim1', component_property= 'value'),
        Input(component_id='Dim2', component_property= 'value'),
        Input(component_id='Dim3', component_property= 'value')
        )
        def method1(dropdown_value, Dim1, Dim2, Dim3):
            print(dropdown_value)
            index_dims = [i for i in [Dim1, Dim2, Dim3] if i]
            try:
                df = self.tt.get_data(data_regex = dropdown_value, index_dims = index_dims).loc['D6-tile0-0', :]
                x = df.index.get_level_values(0) 
                y = df[dropdown_value]
            except Exception:
                x = [0, 1]
                y = [0, 1]
            fig = Plotter(data=df, index_dims=index_dims)
            


            # fig = go.Figure()
            # # fig.add_trace()
            # fig.add_scatter(x = x, y = y)
            
            # # fig = go.Figure([px.imshow(img = df.loc['D6-tile0-0', :])
            # #                  ])
            # fig.update_layout(title = 'Well Data',
            #                 xaxis_title = Dim1.capitalize(),
            #                 yaxis_title = dropdown_value.capitalize()
            #                 )

            return fig
    
    def set_layout(self):
        self.app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
                                                
            dcc.Dropdown( id = 'dropdown',
            options = self.data,
            value = self.data[0]['value']),
            dcc.Dropdown( id = 'Dim1',
            options = self.Dim1,
            value = self.data[0]['value']),
            dcc.Dropdown( id = 'Dim2',
            options = self.Dim2,
            value = self.data[0]['value']),
            dcc.Dropdown( id = 'Dim3',
            options = self.Dim3,
            value = self.data[0]['value']),
            dcc.Graph(id = 'main_plot')
        ])
    
        print('set layout')
    
    # @app.callback(
    #     Output(component_id='main_plot', component_property= 'figure'),
    #     Input(component_id='dropdown', component_property= 'value'),
    #     Input(component_id='Dim1', component_property= 'value'),
    #     Input(component_id='Dim2', component_property= 'value'),
    #     Input(component_id='Dim3', component_property= 'value'),
    #     )
    def graph_update(self, dropdown_value, Dim1, Dim2, Dim3):
        print(dropdown_value)
        index_dims = [i for i in [Dim1, Dim2, Dim3] if i]
        try:
            df = self.tt.get_data(data_regex = dropdown_value, index_dims = index_dims).loc['D6-tile0-0', :]
            x = df.index.get_level_values(0) 
            y = df[dropdown_value]
        except Exception:
            x = [0, 1]
            y = [0, 1]
        # fig = Plotter(data=df, index_dims=index_dims)
        fig = go.Figure()
        # fig.add_trace()
        fig.add_scatter(x = x, y = y)
        
        # fig = go.Figure([px.imshow(img = df.loc['D6-tile0-0', :])
        #                  ])
        fig.update_layout(title = 'Well Data',
                        xaxis_title = Dim1.capitalize(),
                        yaxis_title = dropdown_value.capitalize()
                        )

        return fig
