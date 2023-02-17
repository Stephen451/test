import dash
# from pages.main_page import GraphPage
import dash_bootstrap_components as dbc
from pages.test_page import GraphPage
from pages.sidebar import Sidebar
from pages.run_table import RunTable
from pages.ready_made_plots import ReadyPlots
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
sd = Sidebar(app=app)
# app = sd.app
app.layout = sd.set_layout()
gp = GraphPage(app=app)
rt = RunTable(app=app)
rp = ReadyPlots(app=app)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return rp.set_layout()
    elif pathname == "/page-2":
        return gp.set_layout()
    elif pathname == "/page-3":
        return rt.set_layout()
    # If the user tries to reach a different page, return a 404 message
    return html.P("Doesn't Exist!")

### Assemble all layouts ###
app.validation_layout = html.Div(
    children = [
        sd.set_layout(),
        gp.set_layout(),
        rt.set_layout(),
        rp.set_layout()
    ]
)

if __name__ == '__main__':

    app.run(debug=True, use_reloader=False, port = 8051)
