enter ='\r\n'
import os
from logic.report_generator.functions.L_tablemaker import centertable as table
from logic.report_generator.functions.L_tablemaker import centermoneytable as moneytable
def systemeconomics(reportdict):
    investtable = moneytable(reportdict['investtable'],'|l|r|', 'investtable','Investment cost of the system')
    opextable = moneytable(reportdict['opexinputtable'],'|l|r|r|', 'opextable','Operational expenditure of the main components of the system')
    econinputtable = table(reportdict['econinputtable'], '|l|r|r|', 'econinputtable', 'Economic input variables')
    investinputtable = moneytable(reportdict['investinputtable'],'|l|r|r|', 'investinputtable', 'Per unit investment cost of the main considered system components')
	# actual string concatenation
    econ = '\\subsection*{System economics}' + enter + \
    'In order to assess the economics of the system the following economic ' +\
    'parameters have been assumed: '+enter+\
    econinputtable+enter+\
    'The investment costs associated with the use of the different main components are assumed to be:' +enter+\
    investinputtable+enter+\
    'Based on these the investment costs of the main components of the system are estimated as:'+enter+\
    investtable+enter+\
    'The operational expenditure is estimated as:'+ enter+\
    opextable+enter
    #'\\begin{center}'+enter+\
    #'\\begin{tabular}{r|c}'+enter+\
    #'Investments                & Cost   \\\ \hline '+enter+\
    #'Solar power investment cost     & \\dEUR{'+str(webpage_dict['nominal_solar_power_installed'])+'}  \\\ ' +enter+\
    #'Wind power investment cost &\\dEUR{'+str(webpage_dict['nominal_wind_power_installed'])+'} \\\ ' +enter+\
    #'Storage facility investment cost &\\dEUR{'+str(webpage_dict['storage_capacity'])+'}  \\\ ' +enter+\
    #'\\end{tabular}' +enter+ '\\end{center}'+\
    #'\\captionof{table}{Estimated investment cost of the microgrid} \\vspace{2.5mm}'



    return econ
