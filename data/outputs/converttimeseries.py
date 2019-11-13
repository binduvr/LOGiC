import pandas as pd

def convertdata(session_id):
    path = session_id+'/inputs/demands.csv'
    df = pd.read_csv(path)
    list = ['per_unit_pv_generation','wind_speed', 'residential_demand','temperature','GHI', 'per_unit_wind_generation']
    for key in list:
        series = pd.DataFrame(df[key])
        series.to_csv(session_id+'/inputs/'+key+'.csv', header = False, index = False)
