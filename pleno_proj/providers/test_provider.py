from pleno_droid.analytics.wrappers.run_metrics import RunMetrics
import numpy as np
import pandas as pd

class Provider:
    def __init__(self):
        print('tt')
    
    def load_data(self):

        pat = '/home/stephenk/pleno-droid/test/20221121_HYP1_KR_96plex_triplicate1_Ham_10x0.3'
        print(RunMetrics(pat))
        self.tt = RunMetrics(pat)
        all_names = self.tt.data_names.copy()
        all_names.extend(self.tt.metrics_names)
        data = [{'label': i, 'value': i} for i in all_names]
        data.sort(key=lambda e: e['label'])
        self.allowable_transforms = {
            ('nanoballs', 'hypercodes') : "AssignedHypercode"
        }
        return data, self.tt
    
    def get_dimensions(self, dims: list[str] =  None):
        if not dims:
            dims = self.tt.dimensions()
        default_value = [{'label': " ", 'value': ""}]
        Dim1 = [{'label': i.capitalize(), 'value': i} for i in dims]
        Dim1.sort(key=lambda e: e['label'])
        default_value.extend(Dim1)
        return default_value

    def get_wells(self):
        wells = [{'label': i, 'value': i} for i in self.tt.list_wells()]
        return wells

    def transform_dims(self, Dim1: str, Dim2: str, well_regex: str):

        transformer = self.tt.get_data(data_regex = self.allowable_transforms[(Dim1, Dim2)], index_dims = [Dim1], well_regex = well_regex) 
        transformer.columns = [Dim2]

        return transformer

    def check_transformability(self, Dim1: str, Dim2: str):

        if (Dim1, Dim2) in self.allowable_transforms.keys():
            return True
        return False

    def check_data(self, data_name:str, index_dims: list[str], data_type: str, well_regex: str):
        transformable = False

        if data_type == 'data':
            source = self.tt.data_dims
        else:
            source = self.tt.metric_dims

        #check if all the indicies requested are the same as the raw data.  If missing some just the data with full dimensionality
        if all(item in source[data_name] for item in index_dims):
            return source[data_name], None

        #If all the requested Dims aren't in the raw data, find exceptions and check if we have a transformation mapped already
        requested_inds = []
        existing_inds = source[data_name]
        for item in index_dims:
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

    def get_df(self, data_name: str, index_dims: list[str], well_regex:str = 'D6-tile0-0'):
        if data_name in self.tt.data_dims.keys():
            data_type = 'data'
        else:
            data_type = 'metric'

        fixed_index_dims, transformer = self.check_data(data_name=data_name, index_dims=index_dims, data_type=data_type, well_regex=well_regex)

        df = self.tt.get_data(data_regex = data_name, index_dims = fixed_index_dims, well_regex=well_regex)

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
