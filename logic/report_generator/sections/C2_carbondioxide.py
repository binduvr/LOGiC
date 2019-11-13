
enter = '\r\n'
import os
import re
from logic.report_generator.functions.L_tablemaker import centertable as table
def co2saving(reportdict):
    co2 = '\\subsection*{Carbon emission reduction}' + enter + \
    'As mentioned, sustainability is one of the incentives for consiering microgrids. ' + enter +\
    'Therefore the amount of CO$_{2}$ emission that is reduced with respect to the alternative ' +enter+\
    'is an interesting number to study. For this assessment the CO$_{2}$ emissions are assumed as '+\
    str(format(reportdict['co2_grid_per_kwh']*1000,'.0f')) + ' gram per kWh of grid energy, '+\
    str(format(reportdict['co2_diesel_per_kwh']*1000,'.0f')) + ' gram per kWh of diesel generated energy, ' +\
    str(format(reportdict['co2_pv_per_kwh']*1000,'.0f')) + ' gram per kWh of solar generated energy and '+\
    str(format(reportdict['co2_wind_per_kwh']*1000,'.0f')) + ' gram per kWh of wind generated energy. '+\
    'For the assessed microgrid the emmission is estimated as '+str(format(reportdict['co2_mg_per_kwh']*1000, '.0f')) +\
    ' gram per kWh. This results in an emission reduction of '+\
     str(format((reportdict['co2_grid_per_kwh']-reportdict['co2_mg_per_kwh'])*1000, '.0f'))+' gram per kWh. '+\
    'At the given energy consumption this results in an annual CO$_{2}$ emission reduction of '+\
    sep('%.2f' % ((reportdict['co2_grid_per_kwh']-reportdict['co2_mg_per_kwh'])*reportdict['residential_demand'])) +\
    ' kg per year.'
    return co2

def sep(s, thou=",", dec="."):
    integer, decimal = s.split(".")
    integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
    return integer
