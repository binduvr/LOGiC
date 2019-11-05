
enter = '\r\n'
import os
from logic.report_generator.functions.L_tablemaker import centertable as table
def systemlayout(reportdict):
    layouttable = table(reportdict['systemtable'],'|l|r|r|', 'systemlayout','Sizing of the main components of the system')

    yourmg = '\\end{multicols}\\section*{Your microgrid}\\begin{multicols}{2}\\setlength{\\parindent}{0pt}'+enter+\
    'The assessed situation results in the mircogrid configuration and associated economics described below.'

    sys = '\\subsection*{System sizing}' + enter + \
    'The calculation described above has resulted in the following system:' + enter +\
    layouttable+enter+\
    'The system defined by the parameters above realises a levelised cost of electricity ' +\
    'of \\texteuro '+ str(reportdict['lcoe'])+' per kWh. the system does ' +\
    'this at a renewable energy share of '+ str(reportdict['res_share']) + ' \%. '
	#maybe some comparison to a full diesel mg and buying fro the grid, including blackout numbers and res share comparison?


    return yourmg, sys
