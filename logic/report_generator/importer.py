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

    # sets = {**settings.PARAMETERS_CONSTANT_VALUES,**json.load(open(folder+'/inputs/input.json'))['additional_parameters']}
    # with open(folder+'/inputs/input.json') as file:
    #     inputs = json.load(file)
    with open(folder+'/inputs/input.json') as file:
        inputs = json.load(file)

    # Replace empty values with defaults
    additional_parameters = {}
    for key in inputs['additional_parameters'].keys():
        current_parameter = inputs['additional_parameters'][key]
        if current_parameter != '':
            additional_parameters[key] = inputs['additional_parameters'][key]

    sets = {**settings.PARAMETERS_CONSTANT_VALUES.copy(),**additional_parameters}

    active_components = inputs['active_components']

    # make percentages from fractions
    list = ['tax', 'wacc','blackout_frequency_std_deviation', 'blackout_duration_std_deviation', 'maingrid_renewable_share']
    for key in list:
        sets[key] = sets[key]*100
    del list

    # MAKE TECHNICAL INPUT TABLE
    names = []
    keys  = []
    titles = ['Property','Value']
    techinputtable = maketable(names,keys,titles,sets)

    # MAKE ECONOMIC ENVIRONMENTAL INPUT TABLE
    namelist = ['Maingrid electricity price', 'Maingrid feedin tariff', 'Fuel price', 'Annual change in fuel price', 'Import tax', 'WACC']
    keylist = ['maingrid_electricity_price','maingrid_feedin_tariff','fuel_price','fuel_price_change_annual','tax','wacc']
    titles = ['Variable', 'Value']
    #convert wacc and tax to percent
    unitlist = ['\\euro /kWh','\\euro /kWh','\\euro /liter','\\euro /liter','\\%','\\%']
    it = ['grid_connection','grid_connection','dieselgen','dieselgen','dieselgen','dieselgen']

    units = selectunits(unitlist,it,active_components)
    names,keys = selectvariables(namelist,keylist,it,active_components)
    econinputtable = maketable(names,keys,titles,sets)
    econinputtable['Units'] = units
    econinputtable['Value'] = econinputtable['Value'].map('{:,.2f}'.format)
    del namelist,keylist,titles,unitlist,names,keys,units

    # MAKE MAIN GRID TABLE
    if active_components['grid_connection']:
        names = ['Average blackout duration', 'Blackout duration standard deviation', 'Blackout frequency', 'Blackout frequency standard devation', 'Main grid renewable energy share', 'Distance to main grid']
        keys = ['blackout_duration','blackout_duration_std_deviation','blackout_frequency','blackout_frequency_std_deviation', 'maingrid_renewable_share', 'maingrid_distance']
        units = ['Hours','\%','per month','\%','\%','km']

        titles = ['Property', 'Value']
        gridpropertytable = maketable(names,keys,titles,sets)
        #gridpropertytable['Value'] = gridpropertytable['Value'].map('{:,.2f}'.format)
        gridpropertytable['Unit'] = units
        del names,keys,units

    # MAKE INVESTMENT INPUT TABLE check order
    namelist = ['Solar','Wind', 'Backup generator','Storage capacity', 'Storage power',]
    keylist  = ['pv_cost_investment', 'wind_cost_investment', 'genset_cost_investment', 'storage_capacity_cost_investment','storage_power_cost_investment']
    unitlist = ['kWp','kW','kW','kWh','kW']
    it = ['solar','wind','dieselgen','storage','storage','grid_connection']

    names,keys = selectvariables(namelist,keylist,it,active_components)
    del namelist, keylist

    units = selectunits(unitlist,it,active_components)
    del unitlist

    titles = ['Component', 'Investment costs']
    investinputtable = maketable(names,keys,titles,sets)
    investinputtable['Units'] = units
    investinputtable['Investment costs'] = abs(investinputtable['Investment costs']).map('{:,.2f}'.format)

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
    opexinputtable['Annual pu OPEX'] = abs(opexinputtable['Annual pu OPEX']).map('{:,.2f}'.format)
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

    titles = ['Component', 'pu variable cost']
    varinputtable = maketable(names,keys,titles,sets)
    varinputtable['Units'] = units
    varinputtable['pu variable cost'] = abs(varinputtable['pu variable cost']).map('{:,.2f}'.format)
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
    systemtable['Capacity'] = abs(systemtable['Capacity']).map('{:,.2f}'.format)
    systemtable['Unit'] = units

    # MAKE INVEST TABLE
    namelist = ['Solar modules','Wind turbines', 'Backup generator', 'Storage facility', 'Main grid extension']
    keylist = ['costs_pv','costs_wind','costs_genset','costs_storage', 'costs_maingrid_extension']
    it = ['solar','wind','dieselgen', 'storage','grid_connection']
    names,keys = selectvariables(namelist,keylist, it, active_components)
    titles = ['Component', 'Investment cost']
    investtable = maketable(names,keys,titles,results)
    investtable['Investment cost'] = abs(investtable['Investment cost']).map('{:,.2f}'.format)

    ################################
    # order all the report stuff in the report dictionary
    ################################

    ## PUT TABLES IN THE REPORTDICT
    reportdict['techinputtable'] = techinputtable # as centertable
    reportdict['econinputtable'] = econinputtable # as centermoneytable
    reportdict['opexinputtable'] = opexinputtable # as moneytable
    reportdict['systemtable'] = systemtable # as centertable
    reportdict['investtable'] = investtable # as centermoneytable
    reportdict['varinputtable'] = varinputtable # as centermoneytable
    reportdict['investinputtable'] = investinputtable #as centermoneytable
    ## PUT DEMAND VALUES IN REPORTDICT
    reportdict['residential_demand'] = inputs['demands']['residential_demand']
    reportdict['commercial_demand'] = inputs['demands']['commercial_demand']
    reportdict['industrial_demand'] = inputs['demands']['industrial_demand']

    ## PUT INPUT VALUES IN REPORTDICT
    list = ['address','longitude','latitude']
    for key in list:
        reportdict[key] = inputs[key]
    del list

    ## PUT RESULT VALUES IN REPORTDICT
    list =['capacity_pv_kWp','capacity_wind_kW','lcoe','res_share']
    for key in list:
        reportdict[key] = results[key]
    reportdict['co2_mg_per_kwh'] = results['CO2_mg_per_kWh']
    del list
    reportdict['res_share']=reportdict['res_share']*100
    reportdict['PVinst'] = results['capacity_pv_kWp']
    reportdict['windinst'] = results['capacity_wind_kW']

    reportdict['active_components'] = active_components
    #reportdict['windprod'] = results['fulload_hours_wind']
    #reportdict['PVprod'] = results['fulload_hours_PV']
    reportdict['PVprod'] = 900
    reportdict['windprod'] = 2100

    ## PUT SETTINGS VALUES IN REPORTDICT
    reportdict['co2_pv_per_kwh'] = settings.CO2_PV_PER_KWH
    reportdict['co2_grid_per_kwh'] = settings.CO2_GRID_PER_KWH
    reportdict['co2_wind_per_kwh'] = settings.CO2_WIND_PER_KWH
    reportdict['co2_diesel_per_kwh'] = settings.CO2_DIESEL_PER_KWH

    reportdict['reportname'] = settings.REPORT_NAME
    return reportdict
