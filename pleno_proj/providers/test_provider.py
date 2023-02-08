from pleno_droid.analytics.wrappers.run_metrics import RunMetrics


class Provider:
    def __init__(self):
        print('tt')
    
    def get_data(self):

        pat = '/Users/stephenk/pleno-droid/test/20221121_HYP1_KR_96plex_triplicate1_Ham_10x0.3'
        print(RunMetrics(pat))
        tt = RunMetrics(pat)
        all_names = tt.data_names.copy()
        all_names.extend(tt.metrics_names)
        data = [{'label': i, 'value': i} for i in all_names]
        dims = tt.dimensions()
        default_value = {'label': "", 'value': None}
        Dim1 = [{'label': i.capitalize(), 'value': i} for i in dims].append(default_value)
        Dim2 = [{'label': i.capitalize(), 'value': i} for i in dims].append(default_value)
        Dim3 = [{'label': i.capitalize(), 'value': i} for i in dims].append(default_value)
        wells = [{'label': i, 'value': i} for i in tt.list_wells()]

        return data, Dim1, Dim2, Dim3, wells, tt
        