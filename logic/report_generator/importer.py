'''
function reads all the relevant input and ouput data and puts it in a dictionary called 
data. Then organizes the data required in dataframes (for tables) and values or strings 
(for mentioning in the text); which are stored in the report dictionary
'''

import pandas as pd
import numpy as np
import json
import logic.settings
from logic.report_generator.functions.makedftable import maketable, selectvariables, selectunits
def importer(session_id):

    folder = '/data/outputs/'+session_id
    
    
    settings = {**setting.PARAMETERS_CONSTANT_VALUES,**json.load(open(folder+'/input.json'))['additional_parameters']}
    with open(folder+'/input.json') as file: inputs = json.load(file)
    active_components = inputs[active_components]
    #MAKE TECHNICAL INPUT TABLE
    names = []
    keys  = []
    titles = []
    techinputtable = maketable(names,keys,titles,settings)


    # MAKE INVESTMENT INPUT TABLE check order
    namelist = ['Solar','Wind', 'Backup generator','Storage capacity', 'Storage power',]
    keylist  = ['pv_cost_investment', 'wind_cost_investment', 'genset_cost_investment', 'storage_capacity_cost_investment','storage_power_cost_investment']
    unitlist = ['kW','kWp','kW','kWh','kW',]
    it = ['solar','wind','dieselgen','storage','storage','grid_connection']

    names,keys = selectvariables(namelist,keylist,it,active_components)
    del namelist, keylist
    
    units = selectunits(unitlist,it,active_components)
    del unitlist
    
    titles = ['Component', 'Per unit investment']
    investinputtable = maketable(names,keys,titles,settings)
    investinputtable['Units'] = units
    investinputtable['Investment'] = round(investinputtable['Investment'],2)
    
    del names, keys, titles, units
    
    # MAKE OPEX INPUT TABLE check order
    namelist = ['Solar panels', 'Wind turbines', 'Backup generator', 'Storage capacity', 'Storage power']
    keylist  = ['pv_cost_opex','wind_cost_opex', 'genset_cost_opex','storage_capacity_cost_opex', 'storage_power_cost_opex']
    unitlist = ['kWp','kW','kW','kWh','kW']
    it = ['solar','wind','dieselgen','storage','storage','grid_connection']

    names,keys = selectvariables(namelist,keylist,it,active_components)
    del namelist, keylist
    
    units = selectunits(unitlist,it,active_components)
    del unitlist
    
    ##optionally append names and keys with costs always present
    #names.append('Distribution grid')
    #keys.append('distribution_grid_cost_investment')
    #units = units.append('Total')
    titles = ['Component', 'Annual per unit operational expenditure']
    opexinputtable = maketable(names,keys,titles, settings)
    opexinputtable['Units'] = units
    opexinputtable['Annual per unit operational expenditure']=round(opexinputtable['Annual per unit operational expenditure'],2)
    del names, keys, titles
    
    # MAKE VAR COST INPUT TABLE check order,
    names = ['Solar panels', 'Wind turbines', 'Backup generator', 'Storage facility']
    keys = ['pv_cost_var','wind_cost_var', 'genset_cost_var', 'storage_cost_var']
    unitlist = ['kWh','kWh','kWh','year']
    it = ['solar','wind','dieselgen','storage','storage','grid_connection']

    names,keys = selectvariables(namelist,keylist,it,active_components)
    del namelist, keylist
    
    units = selectunits(unitlist,it)
    del unitlist
    
    titles = ['Component', 'Per unit varible cost']
    varinputtable = maketable(names,keys,titles,settings)
    varinputtable['Units'] = units
    del names, keys, titles
    
    # MAKE REQUIREMENT TABLE
    names = []
    keys = []
    units = []
    titles = ['Requirement','Value']
    requirementtable = maketable(names,keys,titles,settings)
    requirementtable['Units'] = units
    ##########################################
    #  OUTPUT VALUE TABLES
    ##########################################
    data = pd.read_csv(folder+'/test_results.csv') # reads the test results
    
    
    systemtable['Capacity'] = round(systemtable['capacity'],3)
        
    
    
    ## PUT TABLES IN THE REPORTDICT
    reportdict['techinputtable'] = techinputtable # as centertable
    reportdict['econinputtable'] = econinputtable # as centermoneytable
    reportdict['systemtable'] = systemtable # as centertable
    reportdict['investtable'] = investtable # as centermoneytable
    reportdict['opextable'] = opextable # as moneytable
    reportdict['reportname'] = 'Name of the report tex and pdf'
    return reportdict
    
    
     