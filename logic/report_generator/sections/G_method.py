enter = '\r\n'
import os
def method(reportdict):
	dom = str(reportdict['residential_demand'])
	meth = '\\end{multicols}\\section*{Method and development}\\begin{multicols}{2}\\setlength{\\parindent}{0pt}' + \
	enter + '\\subsection*{Method}'+enter+\
	'The OGTC Microgrid Assessment Tool utilizes the Open Energy MOdelling Framework (OEMOF) ' +\
	'to make a first estimation of the (economical) optimal size of the generation and storage ' +\
	'components in an (off-grid) microgrid. This estimation is made by ' +\
	'deriving an equation that describes the cost of energy of a microgrid with the chosen components and solving for the lowest system cost. ' +enter+\
	'The expected energy production by solar panels and wind turbines has '+\
	'been estimated based on weather data made available by the PVGIS project. ' +\
	'This weather data (solar radiation and windspeed) has been used to calculate '+\
	'the expected generated power per installed kW of wind power and kWp of solar power, respectively. \\vfill\\null\\columnbreak'
	#some method description?
	return meth
