'''
function reads all the relevant input and ouput data and puts it in a dictionary called
data. Then organizes the data required in dataframes (for tables) and values or strings
(for mentioning in the text); which are stored in the report dictionary
'''

import pandas as pd
import numpy as np
import json
import logic.settings as settings
from logic.report_generator.functions.makedftable import maketable, selectvariables, selectunits
def import_data(session_id):

    folder = settings.OUTPUT_DIRECTORY + session_id #for local use
    reportdict = {'folder' : folder}

    sets = {**settings.PARAMETERS_CONSTANT_VALUES,**json.load(open(folder+'/inputs/input.json'))['additional_parameters']}
    with open(folder+'/inputs/input.json') as file:
        inputs = json.load(file)
    active_components = inputs['active_components']
    # MAKE TECHNICAL INPUT TABLE
    names = []
    keys  = []
    titles = ['Property','Value']
    techinputtable = maketable(names,keys,titles,sets)

    # MAKE ECONOMIC ENVIRONMENTAL INPUT TABLE
    namelist = ['Maingrid electricity price', 'Maingrid feedin tariff', 'Fuel price', 'Annual change in fuel price', 'Import tax', 'WACC']
    keylist = ['maingrid_electricity_price','maingrid_feedin_tariff','fuel_price','fuel_price_change_annual','tax','wacc']
    titles = ['Parameter', 'Value']
    #convert wacc and tax to percent
    unitlist = ['\\euro per kWh','\\euro per kWh','\\euro per liter','\\euro per liter','\\%','\\%']
    it = ['grid_connection','grid_connection','dieselgen','dieselgen','dieselgen','dieselgen']

    units = selectunits(unitlist,it,active_components)
    names,keys = selectvariables(namelist,keylist,it,active_components)
    econinputtable = maketable(names,keys,titles,sets)
    econinputtable['Units'] = units
    del namelist,keylist,titles,unitlist,names,keys,units

    # MAKE MAIN GRID TABLE
    if active_components['grid_connection']:
        names = ['Average blackout duration', 'Blackout duration standard deviation', 'Blackout frequency', 'Blackout frequency standard devation', 'Main grid renewable energy share', 'Distance to main grid']
        keys = ['blackout_duration','blackout_duration_std_deviation','blackout_frequency','blackout_frequency_std_deviation']
        units = ['Hours','\%','per month','\%','\%','km']

        gridpropertytable = maketable(names,keys,titles,sets)
        gridpropertytable['Units'] = Units
        del names,keys,units

    # MAKE INVESTMENT INPUT TABLE check order
    namelist = ['Solar','Wind', 'Backup generator','Storage capacity', 'Storage power',]
    keylist  = ['pv_cost_investment', 'wind_cost_investment', 'genset_cost_investment', 'storage_capacity_cost_investment','storage_power_cost_investment']
    unitlist = ['kW','kWp','kW','kWh','kW']
    it = ['solar','wind','dieselgen','storage','storage','grid_connection']

    names,keys = selectvariables(namelist,keylist,it,active_components)
    del namelist, keylist

    units = selectunits(unitlist,it,active_components)
    del unitlist

    titles = ['Component', 'Investment costs']
    investinputtable = maketable(names,keys,titles,sets)
    investinputtable['Units'] = units
    investinputtable['Investment costs'] = round(investinputtable['Investment costs'],2)

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
    titles = ['Component', 'Annual pu OPEX']
    opexinputtable = maketable(names,keys,titles, sets)
    opexinputtable['Units'] = units
    opexinputtable['Annual pu OPEX']=round(opexinputtable['Annual pu OPEX'],2)
    del names, keys, titles

    # MAKE VAR COST INPUT TABLE check order,
    namelist = ['Solar panels', 'Wind turbines', 'Backup generator', 'Storage facility']
    keylist = ['pv_cost_var','wind_cost_var', 'genset_cost_var', 'storage_cost_var']
    unitlist = ['kWh','kWh','kWh','year']
    it = ['solar','wind','dieselgen','storage','storage','grid_connection']

    names,keys = selectvariables(namelist,keylist,it,active_components)
    del namelist, keylist

    units = selectunits(unitlist,it,active_components)
    del unitlist

    titles = ['Component', 'Per unit variable cost']
    varinputtable = maketable(names,keys,titles,sets)
    varinputtable['Units'] = units
    del names, keys, titles

    # MAKE REQUIREMENT TABLE
    names = []
    keys = []
    units = []
    titles = ['Requirement','Value']
    requirementtable = maketable(names,keys,titles,sets)
    requirementtable['Units'] = units
    ##########################################
    #  OUTPUT VALUE TABLES
    ##########################################
    res = pd.read_csv(folder+'/test_results.csv') # reads the test results
    results = {}
    cols = res.columns[1:len(res.columns)]
    for col in cols:
        results[col] = res[col][0]
    ##########################################
    #  END OF IMPORT COMMAND
    ##########################################
    # MAKE CAPACITIES TABLE
    namelist = ['Installed solar power','Installed wind power','Installed backup power','Installed storage capacity','Power of storage facility']
    keylist = ['capacity_pv_kWp', 'capacity_wind_kW', 'capacity_genset_kW','capacity_storage_kWh','power_storage_kW']
    unitlist = ['kWp','kW','kW','kWh','kW']
    it = ['solar','wind','dieselgen','storage','storage']
    names,keys = selectvariables(namelist,keylist,it,active_components)
    units = selectunits(unitlist, it,active_components)
    del namelist, keylist, unitlist, it
    titles = ['Component','Capacity']
    systemtable = maketable(names,keys,titles,results)
    del names,keys,titles
    #systemtable['Capacity'] = round(systemtable['Capacity'],0)
    #systemtable['Capacity'] = round(systemtable['Capacity'],0)
    #systemtable = str(systemtable)

    # MAKE INVEST TABLE
    namelist = ['Solar modules','Wind turbines', 'Backup generator', 'Storage facility', 'Main grid extension']
    keylist = ['costs_pv','costs_wind','costs_genset','costs_storage', 'costs_maingrid_extension']
    it = ['solar','wind','dieselgen', 'storage','grid_connection']
    names,keys = selectvariables(namelist,keylist, it, active_components)
    titles = ['Component', 'Investment cost']
    investtable = maketable(names,keys,titles,results)

    ## PUT TABLES IN THE REPORTDICT
    reportdict['techinputtable'] = techinputtable # as centertable
    reportdict['econinputtable'] = econinputtable # as centermoneytable
    reportdict['opexinputtable'] = opexinputtable # as moneytable
    reportdict['systemtable'] = systemtable # as centertable
    reportdict['investtable'] = investtable # as centermoneytable
    ## PUT OTHER VALUES IN REPORTDICT
    reportdict['residential_demand'] = inputs['demands']['residential_demand']
    reportdict['commercial_demand'] = inputs['demands']['commercial_demand']
    reportdict['industrial_demand'] = inputs['demands']['industrial_demand']
    reportdict['address'] = 'dumadr'
    reportdict['active_components'] = active_components
    reportdict['PVinst'] = results['capacity_pv_kWp']
    reportdict['windinst'] = results['capacity_wind_kW']
    #reportdict['windprod'] = results['fulload_hours_wind']
    #reportdict['PVprod'] = results['fulload_hours_PV']
    reportdict['PVprod'] = 900
    reportdict['windprod'] = 2100

    reportdict['lcoe'] = round(results['lcoe'],2)
    reportdict['res_share'] = round(results['res_share']/100,2)

    reportdict['reportname'] = settings.REPORT_NAME
    return reportdict
