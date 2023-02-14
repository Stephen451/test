import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from dash.dependencies import Input, Output, State

class Sidebar():
# the style arguments for the sidebar. We use position:fixed and a fixed width
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 62.5,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "height": "100%",
        "z-index": 1,
        "overflow-x": "hidden",
        "transition": "all 0.5s",
        "padding": "0.5rem 1rem",
        "background-color": "#f8f9fa",
    }

    SIDEBAR_HIDDEN = {
        "position": "fixed",
        "top": 62.5,
        "left": "-16rem",
        "bottom": 0,
        "width": "16rem",
        "height": "100%",
        "z-index": 1,
        "overflow-x": "hidden",
        "transition": "all 0.5s",
        "padding": "0rem 0rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
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

    def __init__(self, app):
        self.app = app

        if self.app is not None and hasattr(self, 'config_callbacks'):
            self.config_callbacks()

        

    def set_layout(self):
        navbar = dbc.NavbarSimple(
            children=[
                dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
                dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("More pages", header=True),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 3", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                ),
            ],
            brand="Brand",
            brand_href="#",
            color="dark",
            dark=True,
            fluid=True,
        )


        sidebar = html.Div(
            [
                html.H2("Sidebar", className="display-4"),
                html.Hr(),
                html.P(
                    "A simple sidebar layout with navigation links", className="lead"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                        dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                        dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            id="sidebar",
            style=self.SIDEBAR_STYLE,
        )

        content = html.Div(

            id="page-content",
            style=self.CONTENT_STYLE)

        layout = html.Div(
        [
            dcc.Store(id='side_click'),
            dcc.Location(id="url"),
            navbar,
            sidebar,
            content,
        ],
        )
        return layout

    def config_callbacks(self):
        @self.app.callback(
            
            Output("sidebar", "style"),
            Output("page-content", "style"),
            Output("side_click", "data"),
            Input("btn_sidebar", "n_clicks"),
            State("side_click", "data")
        )
        def toggle_sidebar(n, nclick):
            if n:
                if nclick == "SHOW":
                    sidebar_style = self.SIDEBAR_HIDDEN
                    content_style = self.CONTENT_STYLE1
                    cur_nclick = "HIDDEN"
                else:
                    sidebar_style = self.SIDEBAR_STYLE
                    content_style = self.CONTENT_STYLE
                    cur_nclick = "SHOW"
            else:
                sidebar_style = self.SIDEBAR_STYLE
                content_style = self.CONTENT_STYLE
                cur_nclick = 'SHOW'

            return sidebar_style, content_style, cur_nclick

        # this callback uses the current pathname to set the active state of the
        # corresponding nav link to true, allowing users to tell see page they are on
        @self.app.callback(
            [Output(f"page-{i}-link", "active") for i in range(1, 4)],
            [Input("url", "pathname")],
        )
        def toggle_active_links(pathname):
            if pathname == "/":
                # Treat page 1 as the homepage / index
                return True, False, False
            return [pathname == f"/page-{i}" for i in range(1, 4)]


