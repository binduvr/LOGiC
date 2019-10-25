
enter = '/r/n'
import os
from L_tablemaker import centertable
def systemlayout(reportdict):
    layouttable = centertable(reportdict['systemtable'],'|l|r|c|', 'systemlayout','Sizing of the main components of the system')
    sys = '\\section*{System sizing}' + enter + \
    'The calculation described above has resulted in the following system:' + enter +\
    layouttable+enter+\
    'The system defined by the parameters above realises a levelised cost of electricity ' +\
    'of \\texteuro '+ str(round(reportdict['lcoe'],2))+' per kWh. the system does ' +\
    'this at a renewable energy share of '+ str(round(reportdict['res_share'],2)) + ' \%. '
	#maybe some comparison to a full diesel mg and buying fro the grid, including blackout numbers and res share comparison?


    return sys
