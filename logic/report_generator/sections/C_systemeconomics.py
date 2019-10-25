enter ='/r/n'
import os

def systemeconomics(reportdict):
    webpage_dict = output_dict['webpage_dict']

	# actual string concatenation
    econ = '\\section*{System economics}' + enter + \
    'In order to assess the economics of the system the following economic ' +\
    'parameters have been assumed: '+enter+\
    '\\begin{center}'+enter+\
    '\\begin{tabular}{r|c|c}'+enter+\
    'Parameter      & Value & unit     \\\ \hline '+enter+\
    'CAPEX wind energy &'+str(webpage_dict['nominal_solar_power_installed'])+'& \\euro\/kWh \\\ ' +enter+\
    'OPEX wind energy &'+str(webpage_dict['nominal_wind_power_installed'])+'& \\euro\/kWh\/year \\\ ' +enter+\
    'Variable cost wind energy &'+str(webpage_dict['storage_capacity'])+'&  \\euro/kWh \\\ ' +enter+\
    'CAPEX solar energy &'+str(webpage_dict['nominal_solar_power_installed'])+'& \\euro\/kWp  \\\ ' +enter+\
    'OPEX solar energy &'+str(webpage_dict['nominal_wind_power_installed'])+'& \\euro\/kWh\/year \\\ ' +enter+\
    'Variable cost solar energy &'+str(webpage_dict['storage_capacity'])+'& \\euro\/kWh \\\ ' +enter+\
    'CAPEX diesel generator &'+str(webpage_dict['nominal_solar_power_installed'])+'& \\euro\/kWp \\\ ' +enter+\
    'OPEX diesel generator&'+str(webpage_dict['nominal_wind_power_installed'])+'& \\euro\/kW\/year \\\ ' +enter+\
    'Variable cost backup &'+str(webpage_dict['storage_capacity'])+'& \\euro\/kWh \\\ ' +enter+\
    '\\end{tabular}'+enter+\
    '\\end{center}' +enter+\
    '\\captionof{table}{Assumed costs of the system} \\vspace{2.5mm}'+enter+\
    'With the estimated system the following costs are associated: '+ enter+\
    '\\begin{center}'+enter+\
    '\\begin{tabular}{r|c}'+enter+\
    'Investments                & Cost   \\\ \hline '+enter+\
    'Solar power investment cost     & \\dEUR{'+str(webpage_dict['nominal_solar_power_installed'])+'}  \\\ ' +enter+\
    'Wind power investment cost &\\dEUR{'+str(webpage_dict['nominal_wind_power_installed'])+'} \\\ ' +enter+\
    'Storage facility investment cost &\\dEUR{'+str(webpage_dict['storage_capacity'])+'}  \\\ ' +enter+\
    '\\end{tabular}' +enter+ '\\end{center}'+\
    '\\captionof{table}{Estimated investment cost of the microgrid} \\vspace{2.5mm}'
    '\\begin{center}\\begin{tabular}{r|c}'
    'Annual operational expenditure & Annual cost  \\\ \hline ' +enter+\
    ' &'+ '\\euro forty-two' +' \\\ ' +\
    '\\end{tabular}'+enter+\
    '\\end{center}' +enter+\
    '\\captionof{table}{Estimated investment cost for the system} \\vspace{2.5mm}'+enter


    return econ
