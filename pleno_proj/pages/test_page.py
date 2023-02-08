from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from plotter.plotter import Plotter
from providers.test_provider import Provider
import plotly.graph_objects as go

class GraphPage():
    def __init__(self, app):
        self.app = app

        # self.app.callback(
        # Output(component_id='main_plot', component_property= 'figure'),
        # Input(component_id='dropdown', component_property= 'value'),
        # Input(component_id='Dim1', component_property= 'value'),
        # Input(component_id='Dim2', component_property= 'value'),
        # Input(component_id='Dim3', component_property= 'value')
        # )(self.graph_update)

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        # self.data, self.Dim1, self.Dim2, self.Dim3, self.wells, self.tt = Provider().get_data()
    
    def config_callbacks(self):
        
        @self.app.callback(
        Output(component_id='main_plot', component_property= 'figure'),
        Input(component_id='dropdown', component_property= 'value')
        )
        def method1(dropdown_value):
            print(dropdown_value)
            x = [0, 1]
            y = [0, 1]
            # fig = Plotter(data=df, index_dims=index_dims)
            fig = go.Figure()
            # fig.add_trace()
            fig.add_scatter(x = x, y = y)
            
            # fig = go.Figure([px.imshow(img = df.loc['D6-tile0-0', :])
            #                  ])
            fig.update_layout(title = dropdown_value,
                            xaxis_title = "Test",
                            yaxis_title = dropdown_value.capitalize()
                            )

            return fig
    
    def set_layout(self):
        self.app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using html components', style = {'textAlign':'center',\
                                                'marginTop':40,'marginBottom':40}),
        dcc.Dropdown( id = 'dropdown',
            options = ['test1', 'test2', 'test3'],
            value = 'test1'),
        dcc.Graph(id = 'main_plot')
        ])