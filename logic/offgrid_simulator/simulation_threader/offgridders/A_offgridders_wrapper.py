import sys
import os
import shutil
from oemof.tools import logger
import logging
import numpy as np
import pandas as pd
import pprint as pp
import pyomo
import time
import datetime

# sys.path.insert(0, './offgridders')
sys.path.insert(0, './logic/offgrid_simulator/simulation_threader/offgridders')

import C_sensitivity_experiments as sens

def run_simulation(offgridders_input):
	# preprocessed_data = offgridders_input.to_dict()
	preprocessed_data = offgridders_input

	case_definition = preprocessed_data['case_definition']
	parameters_constant_values = preprocessed_data['parameters_constant_values']
	parameters_sensitivity = preprocessed_data['parameters_sensitivity']
	project_site_s = preprocessed_data['project_site_s']
	settings = preprocessed_data['settings']
	# NOTE: Added time afterwards
	settings['time_start'] = datetime.datetime(2019, 1, 1, 0, 0)

	logger.define_logging(logpath=settings['output_folder'],
        logfile='micro_grid_design_logfile.log',
        screen_level=logging.INFO,
        #screen_level=logging.DEBUG,
        file_level=logging.DEBUG)

	#---- Define all sensitivity_experiment_s, define result parameters ----------#
	sensitivity_experiment_s, blackout_experiment_s, overall_results, names_sensitivities = \
		sens.generate_sensitvitiy_experiments.get(settings, parameters_constant_values,
			parameters_sensitivity, project_site_s)

	###############################################################################
	# Process and initialize                                                      #
	###############################################################################

	#----------------- Extend sensitivity_experiment_s----------------------------#
	# with demand, pv_generation_per_kWp, wind_generation_per_kW                  #
	#-----------------------------------------------------------------------------#
	from D0_process_input import noise, process_input_parameters
	# Adapt timeseries of experiments according to evaluated days
	max_date_time_index, max_evaluated_days = \
		process_input_parameters.add_timeseries(sensitivity_experiment_s)
	settings.update({'max_date_time_index': max_date_time_index})
	settings.update({'max_evaluated_days': max_evaluated_days})

	# -----------Apply noise to timeseries of each experiment --------------------#
	# This results in unique timeseries for each experiment! For comparability    #
	# it would be better to apply noise to each project site. However, if noise   #
	# is subject to sensitivity analysis, this is not possible. To have the same  #
	# noisy timeseries at a project site, noise has to be included in csv data!   #
	#-----------------------------------------------------------------------------#
	noise.apply(sensitivity_experiment_s)

	# Calculation of grid_availability with randomized blackouts
	from E_blackouts_central_grid import central_grid
	if settings['necessity_for_blackout_timeseries_generation']==True:
		sensitivity_grid_availability, blackout_results = central_grid.get_blackouts(settings, blackout_experiment_s)

	#---------------------------- Base case OEM ----------------------------------#
	# Based on demand, pv generation and subjected to sensitivity analysis SOEM   #
	#-----------------------------------------------------------------------------#
	# import all scripts necessary for loop
	from A1_general_functions import helpers
	from F_case_definitions import cases
	from G0_oemof_simulate import oemof_simulate

	experiment_count = 0
	# total_number_of_simulations = settings['total_number_of_experiments'] * len(case_list)

	for experiment in sensitivity_experiment_s:

		capacities_oem = {}

		if 'grid_availability' not in sensitivity_experiment_s[experiment].keys():
			# extend experiment with blackout timeseries according to blackout parameters
			logging.debug('Using grid availability timeseries that was randomly generated.')
			blackout_experiment_name = sens.get_names.blackout_experiment_name(sensitivity_experiment_s[experiment])
			sensitivity_experiment_s[experiment].update({'grid_availability':
															 sensitivity_grid_availability[blackout_experiment_name]})


		# --------get case definition for specific loop------------------------------#
		experiment_case_dict = cases.update_dict(capacities_oem,
			case_definition, sensitivity_experiment_s[experiment])

		###############################################################################
		# Creating, simulating and storing micro grid energy systems with oemof       #
		# According to parameters set beforehand                                      #
		###############################################################################
		experiment_count = experiment_count + 1
		logging.info('Starting simulation, ' + 'project site ' \
			+ sensitivity_experiment_s[experiment]['project_site_name'] + '.')

		oemof_results = oemof_simulate.run(sensitivity_experiment_s[experiment], experiment_case_dict)

		# Extend base capacities for cases utilizing these values, only valid for specific experiment
		if case_definition['based_on_case'] == False:
			capacities_oem.update({experiment_case_dict['case_name']: helpers.define_base_capacities(oemof_results)})

		# Extend oemof_results by blackout characteristics
		if 'grid_availability' in sensitivity_experiment_s[experiment].keys():
			blackout_result = central_grid.oemof_extension_for_blackouts(sensitivity_experiment_s[experiment]['grid_availability'])
			oemof_results   = central_grid.extend_oemof_results(oemof_results, blackout_result)
		else: # one might check for settings['necessity_for_blackout_timeseries_generation']==True here, but I think its unnecessary
			oemof_results   = central_grid.extend_oemof_results(oemof_results, blackout_results[blackout_experiment_name])

		# Extend overall results dataframe with simulation results
		overall_results = helpers.store_result_matrix(overall_results, sensitivity_experiment_s[experiment], oemof_results)

		# TODO: This will later be fixed
		# Appending results to output file
		output_file = sensitivity_experiment_s[experiment]['output_folder'] + '/test_results.csv'
		# output_df = pd.read_csv(output_file)

		# final_results = output_df.join(overall_results, how='outer')
		# final_results.to_csv(output_file)
		overall_results.to_csv(output_file, index=False)

		if settings['display_experiment'] == True:
			logging.info('The experiment with following parameters has been analysed:')
			pp.pprint(sensitivity_experiment_s[experiment])

	# display all results
	output_names = ['case']
	output_names.extend(names_sensitivities)
	output_names.extend(['lcoe', 'res_share'])
	logging.info('Simulation complete.')
	logging.shutdown()

	# return final_results
	return overall_results
