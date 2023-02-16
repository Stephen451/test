import numpy as np


class StandardSyntax:
    def __init__(self, base_key):
        # NOTE TO FUTURE ME - PICK UP HERE, FIGURE OUT HOW TO TIE PLOT BASESTRINGS TO THESE PARAMS, ADD THESE TO THE DICT AND RETURN TO THE PLOTTER@
        """X is the x axis, y is y, additional dimensions can be assigned to whatever is needed.  name is usually Well which dictates color by default"""
        self.base_key = base_key


    def make_graph(self, **kwargs):
        """append stuff, each kwarg should be a key:value (str:str) pair"""
        graph_root = self.base_key.copy()

        if 'main' in kwargs.keys():
            graph_root['x'] = kwargs.get('main')
        if 'name' in kwargs.keys():
            name = kwargs.get('name') 
            if type(name) == str:
                graph_root['name'] = name
            else:
                graph_root['name'] = str(name[0])
            # name = self.enforce_type('name', str, name, kwargs.get('main'))      
            # graph_root['name'] = name    
        if 'secondary' in kwargs.keys():
            graph_root['y'] = kwargs.get('secondary')
        if 'size' in kwargs.keys():
            graph_root['marker_size'] = kwargs.get('size')
        if 'color' in kwargs.keys():
            graph_root['color'] = kwargs.get('color')

        # for f in kwargs.items():5
        #     graph_root[f[0]] = f[1]

        return graph_root

    # def enforce_type(self, var_name, req_type, var, x):
    #     if type(var_name) == req_type:
    #         return var
    #     elif hasattr(var, '__iter__'):
    #         if type(var[0]) == req_type and len(var) == len(x):
    #             return var
    #     else:
    #         if len(np.unique(var)) < 10:
    #             return var.astype(str)
            

class MatrixSyntax:
    def __init__(self, base_key):
        # NOTE TO FUTURE ME - PICK UP HERE, FIGURE OUT HOW TO TIE PLOT BASESTRINGS TO THESE PARAMS, ADD THESE TO THE DICT AND RETURN TO THE PLOTTER@
        """X is the z intensity, y is the x axis, z is y???????, additional dimensions can be assigned to whatever is needed.  
        name is usually Well which dictates color by default.
        See if I can add a slider so z isn't an aggregate but possible a single value (for live filltering)"""
        self.base_key = base_key

    def make_graph(self, **kwargs):
        """append stuff, each kwarg should be a key:value (str:str) pair"""
        graph_root = self.base_key.copy()

        if 'main' in kwargs.keys():
            graph_root['x'] = kwargs.get('main')
        if 'name' in kwargs.keys():
            graph_root['name'] = kwargs.get('name')
        if 'secondary' in kwargs.keys():
            graph_root['y'] = kwargs.get('secondary')
        if 'color' in kwargs.keys():
            graph_root['color'] = kwargs.get('color')
        if 'size' in kwargs.keys():
            graph_root['marker_size'] = kwargs.get('size')
        # for f in kwargs.items():
        #     graph_root[f[0]] = f[1]

        return graph_root

class TableSyntax:
    def __init__(self, base_key):
        # NOTE TO FUTURE ME - PICK UP HERE, FIGURE OUT HOW TO TIE PLOT BASESTRINGS TO THESE PARAMS, ADD THESE TO THE DICT AND RETURN TO THE PLOTTER@
        """reduce all the data to a table array"""
        self.base_key = base_key

    def make_graph(self, **kwargs):
        """append stuff, each kwarg should be a key:value (str:str) pair"""
        graph_root = self.base_key.copy()

        if 'header' in kwargs.keys():
            graph_root['header'] = kwargs.get('header')
        if 'cells' in kwargs.keys():
            graph_root['cells'] = kwargs.get('cells')
        if 'secondary' in kwargs.keys():
            graph_root['y'] = kwargs.get('secondary')
        if 'color' in kwargs.keys():
            graph_root['color'] = kwargs.get('color')
        if 'size' in kwargs.keys():
            graph_root['marker_size'] = kwargs.get('size')
        # for f in kwargs.items():
        #     graph_root[f[0]] = f[1]

        return graph_root

class PLOT2D(str):
    SCATTER = StandardSyntax({'type': 'scatter', 'mode': 'markers'})
    BAR = StandardSyntax({'type': 'bar'})
    VIOLIN = StandardSyntax({'type': 'violin'})
    TABLE = TableSyntax({'type': 'table'}   )
    HISTOGRAM = StandardSyntax({'type': 'histogram'})
    BOX = StandardSyntax({'type': 'box'})

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs

class PLOT3D(str):
    CONTOUR = MatrixSyntax({'type': 'contour'})
    HEATMAP = MatrixSyntax({'type': 'heatmap'})
    HISTOGRAM = StandardSyntax({'type': 'histogram'})
    VIOLIN = StandardSyntax({'type': 'violin'})
    HISTOGRAM2D = StandardSyntax({'type': 'histogram2d'})
    SCATTER = StandardSyntax({'type': 'scatter', 'mode': 'markers'})
    SCATTER3D = StandardSyntax({'type': 'scatter3d', 'mode': 'markers'})
    SURFACE = MatrixSyntax({'type': 'surface'})
    TABLE = TableSyntax({'type': 'table'})

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs

class PLOT4D(str):
    SCATTER = StandardSyntax({'type': 'scatter', 'mode': 'markers'})
    SCATTER3D = StandardSyntax({'type': 'scatter3d', 'mode': 'markers'})
    TABLE = TableSyntax({'type': 'table'})
    VOLUME = MatrixSyntax({'type': 'volume'})
    

    # def __str__(self) -> str:
    #     return self.value

    def _graphs(self) -> list:
        graphs = [i for i in vars(self) if not i.startswith("_")]
        graphs.sort()
        return graphs
