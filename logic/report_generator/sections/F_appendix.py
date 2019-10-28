from logic.report_generator.functions.L_figuremaker import multicolfigure as figure
enter = '\r\n'
import os
def appendix(reportdict):
    impath = reportdict['folder']+'/electricity_mg/'
    pvyield = reportdict['PVprod']*reportdict['PVinst']
    windyield = reportdict['windprod']*reportdict['windinst']
    pvyield = str(round(pvyield))
    windyield = str(round(windyield))
    res = str(reportdict['residential_demand'])
    com = str(reportdict['commercial_demand'])
    indus = str(reportdict['industrial_demand'])

    app = '\\appendix'+enter+\
    '\\section*{Used input data and method}'+enter+\
    'The timeseries used in and resulting from the calculations are '+\
    'listed on this page.'+enter+\
    figure('per_unit_pv_generation.png', 'Time series of the solar '+\
    'energy production in kW per kWp of installed solar power','perunitpv')+\
    enter+enter+\
    figure('per_unit_wind_generation.png', 'Time series of the wind '+\
    'energy production in kW per kW of installed wind power','perunitwind')+\
    enter+enter+\
    ''+\
    ''+\
    ''+\
    ''
    return app
