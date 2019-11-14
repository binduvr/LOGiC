
enter = '\r\n'
import os
import re
from logic.report_generator.functions.L_tablemaker import centertable as table
def systemlayout(reportdict):
    layouttable = table(reportdict['systemtable'],'|l|r|r|', 'systemlayout','Sizing of the main components of the system')
    s = '%.2f' % reportdict['residential_demand']
    dom = sep(s)

    yourmg = '\\end{multicols}\\section*{Your microgrid}\\begin{multicols}{2}\\setlength{\\parindent}{0pt}'+enter+\
    'The assessed situation results in the mircogrid configuration and associated economics described below.'
    demand = '\\subsection*{Electricity demand}' + enter + \
    'The annual electricity demand has been specified as ' +\
	dom + ' kWh per year and has been converted to a demand time series using historic load data ' +\
	'collected by ENTSO-E.'
    sys = '\\subsection*{System sizing}' + enter + \
    'The calculation described above has resulted in the following system:' + enter +\
    layouttable+enter+\
    'The system defined by the parameters above realises a levelised cost of electricity ' +\
    'of \\texteuro '+ str(format(reportdict['lcoe'],'.2f'))+' per kWh. The system does ' +\
    'this at a renewable energy share of '+ str(format(reportdict['res_share'],'.2f')) + ' \%. '
	#maybe some comparison to a full diesel mg and buying fro the grid, including blackout numbers and res share comparison?


    return yourmg, sys, demand

def sep(s, thou=",", dec="."):
    integer, decimal = s.split(".")
    integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
    return integer
