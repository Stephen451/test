import dash
import dash_bootstrap_components as dbc

# from pages.main_page import GraphPage

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

from components.test_page import GraphPage
from components.sidebar import Sidebar
from components.sidebar_plots import Sidebar2
from components.run_table import RunTable
from components.ready_made_plots import ReadyPlots
from dash import Input, Output, dcc, html



sd = Sidebar2(app=app)
# app = sd.app
# app.layout = sd.set_layout()
# gp = GraphPage(app=app)
rt = RunTable(app=app)
# app.layout = rt.set_layout()
# app.layout.append(dcc.Location(id="url", refresh=False))
rp = ReadyPlots(app=app)



app.layout = dbc.Container([
    dbc.NavbarSimple(
        [dbc.NavItem(dbc.NavLink(dash.page_registry[page]['name'], href=dash.page_registry[page]['path'])) for page in dash.page_registry]
    ),
    
    dash.page_container
])


# @app.callback(Output("parent", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname in ["/page-1"]:
#         return sd.set_layout(content=rp.set_layout())
#     elif pathname == "/page-2":
#         return "Page 2" #gp.set_layout()
#     elif pathname in ["/", "/page-3"]:
#         return rt.set_layout()
#     # If the user tries to reach a different page, return a 404 message
#     return html.P("Doesn't Exist!")

### Assemble all layouts ###
app.validation_layout = html.Div(
    children = [
        sd.set_layout(),
        rt.set_layout(),
        rp.set_layout()
    ]
)

if __name__ == '__main__':

    app.run(debug=True, use_reloader=False, port = 8051)
