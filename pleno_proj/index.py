import dash
# from pages.main_page import GraphPage
import dash_bootstrap_components as dbc
from components.test_page import GraphPage
from components.sidebar import Sidebar
from components.sidebar_plots import Sidebar2
from components.run_table import RunTable
from components.ready_made_plots import ReadyPlots
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id = 'parent')
]
)

sd = Sidebar2(app=app)
# app = sd.app
# app.layout = sd.set_layout()
# gp = GraphPage(app=app)
rt = RunTable(app=app)
app.layout = app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    rt.set_layout()
]
)
rp = ReadyPlots(app=app)

@app.callback(Output("parent", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/page-1"]:
        return sd.set_layout(content=rp.set_layout())
    elif pathname == "/page-2":
        return "Page 2" #gp.set_layout()
    elif pathname in ["/", "/page-3"]:
        return rt.set_layout()
    # If the user tries to reach a different page, return a 404 message
    return html.P("Doesn't Exist!")

### Assemble all layouts ###
app.validation_layout = html.Div(
    children = [
        sd.set_layout(),
        # gp.set_layout(),
        rt.set_layout(),
        rp.set_layout()
    ]
)

if __name__ == '__main__':

    app.run(debug=True, use_reloader=False, port = 8051)
