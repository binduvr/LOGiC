
enter = '/r/n'
import os
from logic.report_generator.functions.L_tablemaker import centertable as table
def systemlayout(reportdict):
    layouttable = table(reportdict['systemtable'],'|l|r|c|', 'systemlayout','Sizing of the main components of the system')
    sys = '\\section*{System sizing}' + enter + \
    'The calculation described above has resulted in the following system:' + enter +\
    layouttable+enter+\
    'The system defined by the parameters above realises a levelised cost of electricity ' +\
    'of \\texteuro '+ str(reportdict['lcoe'])+' per kWh. the system does ' +\
    'this at a renewable energy share of '+ str(reportdict['res_share']) + ' \%. '
	#maybe some comparison to a full diesel mg and buying fro the grid, including blackout numbers and res share comparison?


    return sys
