'''
function reads all the relevant input and ouput data and puts it in a dictionary called 
data. Then organizes the data required in dataframes (for tables) and values or strings 
(for mentioning in the text); which are stored in the report dictionary
'''

import pandas as pd
import numpy as np
import json
import settings
def import(session_id):
    folder = '/data/outputs/'+session_id
    
    
    ##READ COMMAND FOR THE JSON; something like
    
    settings = {**setting.PARAMETERS_CONSTANT_VALUES,**json.load(open(folder+'/input.json'))['additional_parameters']}
       
    
    data = pd.read_csv(folder+'/test_results.csv') # reads the test results
     
     
    ### SYSTEM TABLE
    if active_components['solar']:
        systemtable = pd.DataFrame({'System component':['Installed solar power'],'Capacity': [data['capacity_pv_kWp'][0]], 'Unit':['kWp']})
        if active_components['wind']:
            systemtable = systemtable.append(pd.DataFrame({'System component':['Installed wind power'],'Capacity': [data['capacity_wind_kW'][0]], 'Unit':['kW']}))
        if active_components['storage']:
            systemtable = systemtable.append(pd.DataFrame({'System component':['Storage capacity', 'Storage power'],'Capacity': [data['capacity_storage_kWh'][0],data['power_storage_kW'][0]], 'Unit':['kWh','kW']}))
        systemtable = systemtable.append(pd.DataFrame({'System component':['Backup power'],'Capacity': [data['capacity_genset_kW'][0]], 'Unit':['kW']}))
    elif active_components['wind']:
            systemtable = pd.DataFrame({'System component':['Installed wind power'],'Capacity': [data['capacity_wind_kW'][0]], 'Unit':['kW']})
            if active_components['storage']:
                systemtable = systemtable.append(pd.DataFrame({'System component':['Storage capacity', 'Storage power'],'Capacity': [data['capacity_storage_kWh'][0],data['power_storage_kW'][0]], 'Unit':['kWh','kW']}))
            systemtable = systemtable.append(pd.DataFrame({'System component':['Backup power'],'Capacity': [data['capacity_genset_kW'][0]], 'Unit':['kW']}))
    else:
        systemtable = pd.DataFrame({'System component':['Backup power'],'Capacity': [data['capacity_genset_kW']], 'Unit':['kW']})

    systemtable['Capacity'] = round(systemtable['capacity'],3)
    
    ### CAPACITY TABLE
    if active_components['solar']:
        investtable = pd.DataFrame([{'System component':['Solar modules'],'Investment': [data['costs_pv'][0]])
        if active_components['wind']:
            investtable = investtable.append(pd.DataFrame([{'System component':['Wind turbines'],'Investment': [data['costs_wind'][0]])
        if active_components['storage']:
            investtable = investtable.append(pd.DataFrame([{'System component':['Storage facility'],'Investment': [data['costs_storage'][0]]}))
        investtable = investtable.append(pd.DataFrame([{'System component':['Backup generator'],'Investment': [data['costs_genset'][0]]}))
    elif active_components['wind']:
            investtable = pd.DataFrame([{'System component':['Wind turbines'],'Investment': [data['costs_wind'][0]]})
        if active_components['storage']:
            investtable = investtable.append(pd.DataFrame([{'System component':['Storage unit'],'Investment': [data['costs_storage'][0]]}))
        investtable = investtable.append(pd.DataFrame([{'System component':['Backup power'],'Investment': [data['costs_genset'][0]]}))
    else:
        investtable = pd.DataFrame([{'System component':['Backup power'],'Investment': [data['costs_genset'][0]]})
        
    investtable['Investment'] = round(investtable['Investment'],2)
    
    reportdict['techinputtable'] = techinputtable # as centertable
    reportdict['econinputtable'] = econinputtable # as centermoneytable
    reportdict['systemtable'] = systemtable # as centertable
    reportdict['investtable'] = investtable # as centermoneytable
    reportdict['opextable'] = opextable
    return reportdict
    
    
    ### PUT THESE LINES OF CODE IN THE REPORT GENERATION FUNCTIONS
    systemtable = table(systemtable, '|l|r|c|', systemtable, 'Size of the system components')
    systemtable = table(systemtable, '|l|r|c|', systemtable, 'Size of the system components')
    