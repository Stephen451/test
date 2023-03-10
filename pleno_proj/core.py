import dash
# from pages.main_page import GraphPage
import dash_bootstrap_components as dbc
from pages.test_page import GraphPage


def setup():
    app = dash.Dash()

    # df = px.data.stocks()

    gp = GraphPage(app=app)
    
    app.layout = gp.set_layout()
    # app = gp.app
    return app


if __name__ == '__main__':
    app = setup()

    app.run(debug=True, use_reloader=False)
