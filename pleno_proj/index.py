import dash
from uuid import uuid4
# from pages.main_page import GraphPage
import dash_bootstrap_components as dbc
from components.test_page import GraphPage
from components.sidebar import Sidebar
from components.sidebar_plots import Sidebar2
from components.run_table import RunTable
from components.ready_made_plots import ReadyPlots
# from dash import Input, Output, dcc, html, MultiplexerTransform
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, dcc, html, State
from providers.provider_manager import ProviderManager

provider_manager = ProviderManager()
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = DashProxy(external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[MultiplexerTransform()], prevent_initial_callbacks=True)


def default_layout():
    
    uid = str(uuid4())
    provider_manager.create_new_provider(user_id=uid)

    layout = html.Div(children = [
        dcc.Location(id='url', refresh=True),
        dcc.Store(id='user_id', data=uid, storage_type='memory'),
        dcc.Store(id='data_path', data='', storage_type='session'),
        html.Div(id='parent')
        ]
    )

    return layout

app.layout = default_layout()

sd = Sidebar2(app=app, provider_manager=provider_manager)
# app = sd.app
# app.layout = sd.set_layout()
# gp = GraphPage(app=app)
rt = RunTable(app=app, provider_manager=provider_manager)
# app.layout = app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     rt.set_layout()
# ]
# )
rp = ReadyPlots(app=app, provider_manager=provider_manager)

@app.callback(
            Output("parent", "children"),
            Input("url", "pathname"),
            State("user_id", "data"))
def render_page_content(pathname, uid):
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
        default_layout(),
        sd.set_layout(),
        # gp.set_layout(),
        rt.set_layout(),
        rp.set_layout()
    ]
)

if __name__ == '__main__':

    app.run(debug=True, use_reloader=False, port = 8051)
