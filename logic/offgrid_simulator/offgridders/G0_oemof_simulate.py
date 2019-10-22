'''
Overlying script for tool for the analysis of possible
operational modes of micro grids interconnecting with an unreliable national grid

General settings, simulation-specific input data taken from dictionary experiment

Utilizing the bus/component library oemof_generatemodel and the process oemof library oemof_general
new cases can easily be added.
'''

# to check for files and paths
import os.path
import timeit

# NOTE: This ensures the "multithreading" is possible
import pyutilib.subprocess.GlobalData
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

# Logging of info
import logging
import oemof.outputlib as outputlib

# For speeding up lp_files and bus/component definition in oemof as well as processing
from G1_oemof_create_model import oemof_model
from G2b_constraints_custom import stability_criterion, renewable_criterion, battery_management, ac_dc_bus
from G3_oemof_evaluate import timeseries
from G3a_economic_evaluation import economic_evaluation
from G3b_plausability_tests import plausability_tests
from G4_output_functions import output

# This is not really a necessary class, as the whole experiement could be given to the function, but it ensures, that
# only correct input data is included

class oemof_simulate:

    def run(experiment, case_dict):
        '''
        Funktion to generate oemof-lp file, simulate and extract simulation results from oemof-results,
        including extraction of time series, accumulated values, optimized capacities.
        Simulation results are extracted based on their case definitions in case_dict,
        thus the only part where changes are neccesary to modify cases is not here but
        in the case definitions directly (oemof_cases). If the computation of the extracted
        results itself should change (eg. in the future allowing a finer timestep resulution),
        this is the right place.
        '''
        start = timeit.default_timer()

        file_name = case_dict['filename']

        # For restoring .oemof results if that is possible (speeding up computation time)
        if os.path.isfile(experiment['output_folder'] + "/oemof/" + file_name + ".oemof") and experiment['restore_oemof_if_existant'] == True:
            logging.info("Previous results of " + case_dict['case_name'] + " restored.")

        # If .oemof results do not already exist, start oemof-process
        else:
            # generate model
            micro_grid_system, model = oemof_model.build(experiment, case_dict)
            # perform simulation
            micro_grid_system        = oemof_model.simulate(experiment, micro_grid_system, model, file_name)
            # store simulation results to .oemof
            oemof_model.store_results(micro_grid_system, file_name, experiment['output_folder'])

        # it actually is not really necessary to restore just simulated results... but for consistency and to make sure that calling results is easy, this is used nevertheless
        # load oemof results from previous or just finished simulation
        micro_grid_system = oemof_model.load_oemof_results(experiment['output_folder'], file_name)

        #output.save_network_graph(micro_grid_system, case_dict['case_name'])
        ######################
        # Processing
        ######################
        results = micro_grid_system.results['main']
        meta = micro_grid_system.results['meta']

        oemof_results = {
            'case': case_dict['case_name'],
            'filename': 'results_' + case_dict['case_name'] + experiment['filename'],
            'objective_value': meta['objective'],
            'simulation_time': meta['solver']['Time'],
            'comments': experiment['comments']
        }

        electricity_bus_ac = outputlib.views.node(results, 'bus_electricity_ac')

        electricity_bus_dc = outputlib.views.node(results, 'bus_electricity_dc')

        try:

            e_flows_df = timeseries.get_demand(case_dict, oemof_results, electricity_bus_ac, electricity_bus_dc, experiment)
            e_flows_df = timeseries.get_shortage(case_dict, oemof_results, electricity_bus_ac, electricity_bus_dc, experiment, e_flows_df)

            oemof_results.update({'supply_reliability_kWh':
                                      oemof_results['total_demand_supplied_annual_kWh'] / oemof_results[
                                          'total_demand_annual_kWh']})

            e_flows_df = timeseries.get_excess(case_dict, oemof_results, electricity_bus_ac, electricity_bus_dc, e_flows_df)

            timeseries.get_fuel(case_dict, oemof_results, results)
            e_flows_df = timeseries.get_genset(case_dict, oemof_results, electricity_bus_ac, e_flows_df)

            e_flows_df = timeseries.get_national_grid(case_dict, oemof_results, results, e_flows_df,
                                                      experiment['grid_availability'])

            e_flows_df = timeseries.get_wind(case_dict, oemof_results, electricity_bus_ac, e_flows_df,
                                             experiment['peak_wind_generation_per_kW'])

            e_flows_df = timeseries.get_pv(case_dict, oemof_results, electricity_bus_dc, experiment, e_flows_df,
                                           experiment['peak_pv_generation_per_kWp'])

            e_flows_df = timeseries.get_storage(case_dict, oemof_results, experiment, results, e_flows_df)

            e_flows_df = timeseries.get_rectifier(case_dict, oemof_results, electricity_bus_ac, electricity_bus_dc, e_flows_df)

            e_flows_df = timeseries.get_inverter(case_dict, oemof_results, electricity_bus_ac, electricity_bus_dc, e_flows_df)

            # determine renewable share of system - not of demand, but of total generation + consumption.
            timeseries.get_res_share(case_dict, oemof_results, experiment)

        except (KeyError):
            logging.error('Optimized values for a component could not be found in simulation results. \n'
                          'Did you use restore_oemof_if_existant=True? Than you probably reload an out-dated model and its results.')

        # Run plausability test on energy flows
        plausability_tests.run(oemof_results, e_flows_df)

        # Run test on oemof constraints
        if case_dict['stability_constraint']==False:
            pass
        elif case_dict['stability_constraint'] == 'share_backup':
            stability_criterion.backup_test(case_dict, oemof_results, experiment, e_flows_df)
        elif case_dict['stability_constraint'] == 'share_usage':
            stability_criterion.usage_test(case_dict, oemof_results, experiment, e_flows_df)
        elif case_dict['stability_constraint'] == 'share_hybrid':
            stability_criterion.hybrid_test(case_dict, oemof_results, experiment, e_flows_df)

        renewable_criterion.share_test(case_dict, oemof_results, experiment)
        battery_management.forced_charge_test(case_dict, oemof_results, experiment, e_flows_df)
        battery_management.discharge_only_at_blackout_test(case_dict, oemof_results, e_flows_df)
        ac_dc_bus.inverter_only_at_blackout_test(case_dict, oemof_results, e_flows_df)

        # Generate output (csv, png) for energy/storage flows
        output.save_mg_flows(experiment, case_dict, e_flows_df, experiment['filename'])
        output.save_storage(experiment, case_dict, e_flows_df, experiment['filename'])

        # print meta/main results in command window
        if electricity_bus_ac != None:
            output.print_oemof_meta_main_invest(experiment, meta, electricity_bus_ac, case_dict['case_name'])
        if electricity_bus_dc != None:
            output.print_oemof_meta_main_invest(experiment, meta, electricity_bus_dc, case_dict['case_name'])

        # Evaluate simulated systems regarding costs
        economic_evaluation.project_annuities(case_dict, oemof_results, experiment)

        duration = timeit.default_timer() - start
        oemof_results.update({'evaluation_time': round(duration, 5)})

        # Infos on simulation
        logging.info('Simulation of case "' + case_dict['case_name'] + '" resulted in : \n'
                     + '    ' + '  ' + '    ' + '    ' + '    '
                     + str(round(oemof_results['lcoe'], 3)) + ' currency/kWh, '
                     + 'at a renewable share of '
                     + str(round(oemof_results['res_share'] * 100, 2)) + ' percent'
                     + ' with a reliability of '
                     + str(round(oemof_results['supply_reliability_kWh'] * 100, 2)) + ' percent')
        logging.info('    Initial simulation time (s): ' + str(round(oemof_results['simulation_time'], 2)) + ' / Actual evaluation time (s): '  + str(round(duration, 2)))

        # Debug messages
        logging.debug('    Exact OEM results of case "' + case_dict['case_name'] + '" : \n'
                     + '    ' + '  ' + '    ' + '    ' + '    ' + str(
            round(oemof_results['capacity_storage_kWh'], 3)) + ' kWh battery, '
                     + str(round(oemof_results['capacity_pv_kWp'], 3)) + ' kWp PV, '
                    + str(round(oemof_results['capacity_wind_kW'], 3)) + ' kW wind, '
                     + str(round(oemof_results['capacity_genset_kW'], 3)) + ' kW genset '
                     + 'at a renewable share of ' + str(round(oemof_results['res_share'] * 100, 2)) + ' percent'
                     + ' with a reliability of ' + str(
            round(oemof_results['supply_reliability_kWh'] * 100, 2)) + ' percent')
        logging.debug('    Simulation of case ' + case_dict['case_name'] + ' complete.')
        logging.debug('\n')

        if experiment['save_oemofresults'] == False:
            os.remove(experiment['output_folder']+'/oemof/'+file_name + ".oemof")

        return oemof_results