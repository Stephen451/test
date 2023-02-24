from components.test_page import GraphPage
from components.sidebar import Sidebar
from components.sidebar_plots import Sidebar2
from components.run_table import RunTable
from components.ready_made_plots import ReadyPlots
from dash import Input, Output, dcc, html

class TablePage:
    def __init__(self, app):
        self.app = app
    
    def setup_layout(self):
        rt = RunTable(self.app)
        return rt.set_layout()

def layout():
    raise NotImplementedError
    