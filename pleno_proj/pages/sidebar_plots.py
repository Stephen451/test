import dash
from dash.dependencies import Input, Output, State
import  dash_bootstrap_components as dbc
from dash import html, dcc
import dash_mantine_components as dmc

from pleno_droid.analytics.plots import HypercodePlots, Position

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

class Sidebar2():
# the style arguments for the sidebar. We use position:fixed and a fixed width

    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        self.available_plots = HypercodePlots.get_registered_functions()

    def build_accordion(self):
        accordion_items = []
        button_no = 0
        for i, field in enumerate(self.available_plots.items()):
                
                button_list = []
                for button in field[1]:
                    button_list.append(
                        dmc.Button(
                        button['label'],
                        id = {"type": f"ready-sidebar-button", "value": button['value']},
                        fullWidth=True,
                        variant='outline'
                        )
                    )
                    button_no += 1

                item = dbc.AccordionItem(
                    button_list,
                    title=field[0],
                    item_id=f"accordion_{i}"
                    )
                accordion_items.append(item)
        return accordion_items

    def set_layout(self):
        button = html.Div([
                dmc.Burger(id="toggle-button", opened=False),
            ], className='sidebar-toggle',
            style={"position": "absolute", "top": 10, "left": 10})

        sidebar = dmc.Drawer(
                id='sidebar',
                children=[
                    dbc.Accordion(
                                self.build_accordion(),
                                # vertical=True,
                                # pills=True,
                                start_collapsed=True,
                                flush=True
                            )],
                padding="md",
                position="left",
                trapFocus=False,
                withOverlay=True,
                opened=False,
                closeOnEscape=True,
                # header=dmc.Button("Toggle Sidebar"),
            )

        content = html.Div(html.H1("TEST"),

            id="page-content",
            style={ "height": "100%",
            "margin": "0"})

        layout = html.Div(
        [
            dcc.Store(id='side_click'),
            dcc.Location(id="url"),
            button,
            sidebar,
            content,
        ],
        )

        return layout


    def config_callbacks(self):

        @self.app.callback(
            Output("sidebar", "opened"),
            [Input("toggle-button", "opened")],
            [State("sidebar", "opened")],
        )
        def toggle_sidebar(n_clicks, is_open):
            if n_clicks:
                return not is_open
            return is_open

    # @app.callback(
    #     Output("toggle-button", "opened"),
    #     [Input("sidebar", "opened")],
    # )
    # def toggle_sidebar(is_open):
    #     if is_open:
    #         return is_open 


if __name__ == '__main__':
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    sd = Sidebar2(app=app)
    app.layout = sd.set_layout()
    app.run_server(debug=True, use_reloader=False)
