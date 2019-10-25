from logic.report_generator.functions.L_figuremaker import multicolfigure as figure
enter = '/r/n'
import os
def appendix(reportdict):
	impath = '/outputs/'+str(output_dict['session_id'])+'/'
	pvyield = str(int(preprocessed_data['totalperkwpPV']))
	windyield = str(int(preprocessed_data['totalperkwwind']))
	dom = str(reportdict['domestic_demand'])
	com = str(reportdict['commercial_demand'])
	indus = str(reportdict['industrial_demand'])

	app = '\\appendix'+enter+\
	'\\section*{Used data and time series}'+enter+\
	'The timeseries used in and resulting from the calculations are '+\
	'listed on this page.'+enter+\
	figure('per_unit_pv_generation.png', 'Time series of the solar '+\
	'energy production in kW per kWp of installed solar power','perunitpv')+\
	enter+enter+\
	figure('per_unit_wind_generation.png', 'Time series of the wind '+\
	'energy production in kW per kW of installed wind power','perunitwind')+\
	enter+enter+\
	''+\
	''+\
	''+\
	''

	return app
