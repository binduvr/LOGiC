import numpy as np
import json
import os
import pandas as pd
import pprint as pp

import logic.offgrid_simulator.offgridders.A_offgridders_wrapper as og
import logic.offgrid_simulator.models as models
import logic.offgrid_simulator.weather as weather

# TODO:
# MONTHLY TOTALS TIME SERIES OF ALL RESULTS AS OUTPUT TO BE USED IN GRAPH

# MAKE OUTPUT INCLUDE HOW MANY SOLAR PANELS AND TYPE ETC AND WIND TURBINES AND COSTS

# SHOW CO2 REDUCTION BY USING THIS SYSTEM


# IMPORT TAX OVER THE MACHINARY ORDERED OR SOMETHING remove tax for now

# MAKE THE FUNCTION RETURN ESTIMATED TIME OR SOMETHING


def generate_simulation_results(input_dict, session_id):
    print('starting working dir: ' + os.getcwd())
    endwd = os.getcwd()

    offgridders_input = generate_input(input_dict, session_id)

    results = og.run_simulation(offgridders_input)

    output_data = generate_webpage_output(results, session_id)

    # START WORKING ON REPORT GENERATION ROUTE
    # GET FLASK STRUCTURE ON POINT

    # if 'reportstuff' in output_dict:
    #     from C4_reportgenerator import repgen, repcompile, removejunk
    #     repgen(output_dict, input_dict, results, preprocessed_data)
    #     repcompile(input_dict, output_dict)
    #     #following lines are under construction and thus commented
    #     from C5_sendreport import mailreport
    #     mailreport(input_dict,output_dict)
    #     #send(output_dict, input_dict, results, preprocessed_data)

    #     #removejunk(input_dict, output_dict)
    # os.chdir(endwd)
    # print('ending working dir: ' + os.getcwd())
    return output_data




def generate_input(input_dict, session_id):
    """This function gets the input ready to be run through OESMOT"""

    # Set values from input dictionary
    latitude = input_dict['latitude']
    longitude = input_dict['longitude']
    country_code = input_dict['country_code']
    project_name = input_dict['project_name']
    active_components = input_dict['active_components']
    demands = input_dict['demands']
    additional_parameters = input_dict['additional_parameters']

    # Make directory for the ID of this simulation
    output_directory = 'data/outputs/'+session_id
    os.mkdir(output_directory)

    # Dump input json to the directory for analysis at later stage
    with open(output_directory + os.sep + 'input.json', 'w') as fp:
        json.dump(input_dict, fp)

    # Get optimal panel configuration for location
    # TODO: Do this in OSELC app
    optimal_slope, optimal_azimuth = weather.get_optimal_panel_config(latitude, longitude)
    panel_config = {'optimal_slope': [optimal_slope],
        'optimal_azimuth': [optimal_azimuth]}
    df = pd.DataFrame(data=panel_config)
    df.to_csv(output_directory + '/test_results.csv', index=False)

    # Create folders for OESMOT output
    folder_list = ['/lp_files', '/storage', '/electricity_mg', '/inputs', '/oemof']

    for folder in folder_list:
        os.mkdir(output_directory + folder)

    # Configure the project site
    project_site = models.ProjectSite(country_code, latitude, longitude, demands)
    project_site.plot_data(output_directory + '/inputs')

    # Create offgridders input object
    offgridders_input = models.OffgriddersInput(project_name, project_site,
        active_components, additional_parameters, output_directory)

    return offgridders_input


def generate_webpage_output(results, session_id):
    webpage_output = {
        'session_id': session_id,
        'nominal_solar_power_installed': results['capacity_pv_kWp'][0],
        'nominal_wind_power_installed': results['capacity_wind_kW'][0],
        'nominal_diesel_generator_power': results['capacity_genset_kW'][0],
        'storage_capacity': results['capacity_storage_kWh'][0],
        'renewable_energy_share': (results['res_share'][0])*100,
        'levelised_cost_of_electricity': results['lcoe'][0],
        'solar_system_cost': results['costs_pv'][0],
        'wind_system_cost': results['costs_wind'][0],
        'storage_unit_cost': results['costs_storage'][0],
        'diesel_generator_cost': results['costs_genset'][0],
        # TODO: Move to OSELC app
        'optimal_slope': results['optimal_slope'][0],
        'optimal_azimuth': results['optimal_azimuth'][0]
    }


    # plotdata = pd.read_csv('simulation_results/test/electricity_mg/'+input_dict['project_name']+'_electricity_mg.csv')
    # plotdata = plotdata.round(5)
    # from D31_plotter import plotter

    # TODO: Fix output directory plotting
    # plotter(plotdata, input_dict['outputdir'],input_dict['runtime'])

    # if 'generate_report' in input_dict:
    #     if input_dict['generate_report']:
    #         output_dict['reportstuff'] = dict()


    return webpage_output
