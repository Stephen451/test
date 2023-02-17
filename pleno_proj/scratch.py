import dash
from dash.dependencies import Input, Output, State
import  dash_bootstrap_components as dbc
from dash import html, dcc
import dash_mantine_components as dmc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dmc.Burger(id="toggle-button", opened=False),
    ], className='sidebar-toggle'),
    dmc.Drawer(
        id='sidebar',
        children=[
            # add your sidebar content here
            html.P("Sidebar content goes here.")
        ],
        padding="md",
        position="left",
        trapFocus=False,
        withOverlay=False
        # header=dmc.Button("Toggle Sidebar"),
    ),
    html.Div([
        # add your main content here
    ], className='main-content'),
])


def register_call():

    @app.callback(
        Output("sidebar", "opened"),
        [Input("toggle-button", "opened")],
        [State("sidebar", "opened")],
    )
    def toggle_sidebar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open


if __name__ == '__main__':
    register_call()
    app.run_server(debug=True, use_reloader=False)