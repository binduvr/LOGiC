import D41_symbolfunctions as sym
enter = sym.enterkey()
import os
def method(output_dict, input_dict, results, preprocessed_data):
	meth = '\\section*{Method}' + \
	enter + \
	'The LOGiC Off-Grid sizing tool utilizes the Open Energy MOdelling Framework (OEMOF0 [REF!] ' +\
	'to make a first estimation of the (economical) optimal size of the generation and storage ' +\
	'components in an (off-grid) microgrid. This estimation is made by ' +\
	'[insert method explanation]' +enter+\
	'The total electricity demand has been been specified as ' +\
	dom + ' and has been converted to a demand time series using historic load data ' +\
	'collected bij ENTSO-E [REF!].' +enter+\
	'The expected energy production by solar panels and wind turbines has '+\
	'been estimated based on weather data made available by the PVGIS project [REF!]. ' +\
	'This weather data (solar radiation and windspeed) has been used to calculate '+\
	'the expected generated power per installed kW of wind power and kWp of solar power, respectively. '
	#some method description?
	return meth
