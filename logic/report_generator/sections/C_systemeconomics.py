enter ='/r/n'
import os
from logic.report_generator.functions.L_tablemaker import centertable as table
def systemeconomics(reportdict):
    investtable = table(reportdict['investtable'],'|l|r|c|', 'investtable','Investment cost of the system')
    opextable = table(reportdict['opextable'],'|l|r|c|', 'opextable','Operational expenditure of the main components of the system')
    econinputtable = table(reportdict['econinputtable'], '|l|r|c|', 'econinputtable', 'Economic input variables')

	# actual string concatenation
    econ = '\\section*{System economics}' + enter + \
    'In order to assess the economics of the system the following economic ' +\
    'parameters have been assumed: '+enter+\
    econinputtable+enter+\
    'Based on these the investment costs of the main components of the system are estimated as:'+enter+\
    investtable+enter+\
    'The operational expenditure is estimated as:'+ enter+\
    opextable+enter+\
    #'\\begin{center}'+enter+\
    #'\\begin{tabular}{r|c}'+enter+\
    #'Investments                & Cost   \\\ \hline '+enter+\
    #'Solar power investment cost     & \\dEUR{'+str(webpage_dict['nominal_solar_power_installed'])+'}  \\\ ' +enter+\
    #'Wind power investment cost &\\dEUR{'+str(webpage_dict['nominal_wind_power_installed'])+'} \\\ ' +enter+\
    #'Storage facility investment cost &\\dEUR{'+str(webpage_dict['storage_capacity'])+'}  \\\ ' +enter+\
    #'\\end{tabular}' +enter+ '\\end{center}'+\
    #'\\captionof{table}{Estimated investment cost of the microgrid} \\vspace{2.5mm}'



    return econ
