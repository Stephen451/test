from pleno_droid.analytics.wrappers.run_metrics import RunMetrics
from pleno_droid.utils.exceptions import InvalidRunFolderError
from pleno_common.models.plenoid_library import find_plenoid_library_files
import yaml
import numpy as np
import pandas as pd

class Provider:
    def __init__(self, path: str = None):
        
        self.path = path
        self.allowable_transforms = {
            ('nanoballs', 'hypercodes') : "AssignedHypercode"
        }
        if self.path:
            self.load_data()
        self.config = {'PanelInfo':{'panel_flow_count': 8}}
    
    def load_data(self):
        #### TODO make this smarter - should reload already loaded data
        print('LOADING MORE DATA')
        if not self.path:
            self.path = '/Users/stephenk/pleno-droid/test/20221121_HYP1_KR_96plex_triplicate1_Ham_10x0.3'

        try:
            # print(RunMetrics(self.path))
            self.rm = RunMetrics(self.path)
            all_names = self.rm.data_names.copy()
            all_names.extend(self.rm.metrics_names)
            self.data = [{'label': i, 'value': i} for i in all_names]
            self.data.sort(key=lambda e: e['label'])
            with open(find_plenoid_library_files(self.path)[0][1]) as f:
                self.config = yaml.safe_load(f)
  
        except (AssertionError, InvalidRunFolderError, ValueError, IndexError):
            print("run_info.yaml doesn't exist inside this folder")
            self.rm = RunMetrics(self.path)
            all_names = self.rm.data_names.copy()
            all_names.extend(self.rm.metrics_names)
            self.data = [{'label': i, 'value': i} for i in all_names]
            self.data.sort(key=lambda e: e['label']) 
            self.config = {'PanelInfo':{'panel_flow_count':8}}
    
    def get_dimensions(self, dims: list[str] =  None):
        if not dims:
            dims = self.rm.dimensions()
        default_value = [{'label': " ", 'value': ""}, {'label': "Wells", 'value': "wells"}]
        Dim1 = [{'label': i.capitalize(), 'value': i} for i in dims]
        Dim1.sort(key=lambda e: e['label'])
        default_value.extend(Dim1)
        return default_value

    def get_wells(self):
        if hasattr(self, 'rm'):
            wells = [{'label': i, 'value': i} for i in self.rm.list_wells()]
        else:
            wells = []
        return wells
        
    def transform_dims(self, Dim1: str, Dim2: str, well_regex: str):

        transformer = self.rm.get_data(data_regex = self.allowable_transforms[(Dim1, Dim2)], index_dims = [Dim1], well_regex = well_regex) 
        transformer.columns = [Dim2]

        return transformer

    def check_transformability(self, Dim1: str, Dim2: str):

        if (Dim1, Dim2) in self.allowable_transforms.keys():
            return True
        return False

    def check_data(self, data_name:str, index_dims: list[str], data_type: str, well_regex: str, skip_dims: list[str] = None):
        transformable = False

        if data_type == 'data':
            source = self.rm.data_dims
        else:
            source = self.rm.metric_dims

        if skip_dims:
            temp_dims = [i for i in index_dims if i not in skip_dims]
        else:
            temp_dims = index_dims

        #check if all the indicies requested are the same as the raw data.  If missing some just return the data with full dimensionality
        if all(item in source[data_name] for item in temp_dims):
            return source[data_name], None

        #If all the requested Dims aren't in the raw data, find exceptions and check if we have a transformation mapped already
        requested_inds = []
        existing_inds = source[data_name]
        for item in temp_dims:
            if item not in existing_inds:
                requested_inds.append(item)
            else:
                existing_inds = np.delete(existing_inds, np.where(existing_inds == item))
        if len(requested_inds) == 1 and len(existing_inds) == 1:
            transformable = self.check_transformability(existing_inds[0], requested_inds[0])

        if transformable:
            transformer = self.transform_dims(existing_inds[0], requested_inds[0], well_regex)
            return source[data_name], {(existing_inds[0], requested_inds[0]): transformer}

        return index_dims, None

    def get_df(self, data_name: str, index_dims: list[str], well_regex:str = None, skip_dims: list[str] = []):
        if data_name in self.rm.data_dims.keys():
            data_type = 'data'
        else:
            data_type = 'metric'

        if not well_regex:
            well_regex = "^[A-Z][0-9]{1,2}(-tile[0-9]-[0-9])?$"

        fixed_index_dims, transformer = self.check_data(data_name=data_name, index_dims=index_dims, data_type=data_type, well_regex=well_regex)

        df = self.rm.get_data(data_regex = data_name, index_dims = fixed_index_dims, well_regex=well_regex, skip_dims=skip_dims)

        if transformer:
            transform_keys = list(transformer.keys())[0]
            transform_data = list(transformer.values())[0]
            new_df = pd.DataFrame()
            for well, data in df.groupby(level=0):
                joined_data = data.join(transform_data.loc[well], how='inner')
                new_ind = [i if i is not transform_keys[0] else transform_keys[1] for i in joined_data.index._names]
                joined_data = joined_data.reset_index()
                new_df = pd.concat([new_df, joined_data])
            
            new_df = new_df.set_index(new_ind)
            new_df = new_df.drop(labels=transform_keys[0], axis = 1)
            levels = [int(i) for i in np.arange(0,len(new_ind))]
            df = new_df.groupby(level=levels).mean()
        
        if len(df) > 10000:
            df = df.sample(10000)
        return df

    def filter_df(self, data: pd.DataFrame, filter_dim: str, filter_type:str, index_dims: list[str]):
        agg_levels = [i for i in data.index.names if i != filter_dim]

        if filter_type == 'mean':
            temp_df = data.groupby(level=agg_levels).mean()
        if filter_type == 'std':
            temp_df = data.groupby(level=agg_levels).mean()

        new_dims = [i for i in index_dims if i != filter_dim]

        return temp_df, new_dims