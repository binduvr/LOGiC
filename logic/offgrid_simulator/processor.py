import numpy as np
import json
import os
import pandas as pd
import pprint as pp
import time

import logic.offgrid_simulator.offgridders.A_offgridders_wrapper as og
import logic.offgrid_simulator.models as models
import logic.offgrid_simulator.weather as weather
import logic.settings as settings

# TODO:

# MAKE OUTPUT INCLUDE HOW MANY SOLAR PANELS AND TYPE ETC AND WIND TURBINES AND COSTS
# MAKE THE FUNCTION RETURN ESTIMATED TIME OR SOMETHING

# PUT PICTURE OF LOCATION IN REPORT
# IMPORT TAX OVER THE MACHINARY ORDERED OR SOMETHING remove tax for now

def generate_simulation_results(input_dict, session_id):

    offgridders_input = generate_input(input_dict, session_id)

    results = og.run_simulation(offgridders_input)

    # TODO: Find better way for lat lon
    latitude = input_dict['latitude']
    longitude = input_dict['longitude']
    # session_id = '20191114100723'
    append_additional_results(session_id, latitude, longitude)

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
    output_directory = settings.OUTPUT_DIRECTORY + session_id
    os.mkdir(output_directory)

    # Get optimal panel configuration for location
    # TODO: Do this in OSELC app
    # optimal_slope, optimal_azimuth = \
    #     weather.get_optimal_panel_config(latitude, longitude)
    # panel_config = {'optimal_slope': [optimal_slope],
    #     'optimal_azimuth': [optimal_azimuth]}

    # df = pd.DataFrame(data=panel_config)
    # df.to_csv(output_directory + '/test_results.csv', index=False)

    # Create folders for OESMOT output
    folder_list = ['/lp_files', '/storage', '/electricity_mg',
        '/inputs', '/oemof','/report']

    for folder in folder_list:
        os.mkdir(output_directory + folder)

    # Dump input json to the directory for analysis at later stage
    with open(output_directory + '/inputs/input.json', 'w') as fp:
        json.dump(input_dict, fp)

    # TODO: Implement surface roughness functionality
    # Configure the project site
    project_site = models.ProjectSite(country_code, latitude, longitude, demands)
    project_site.plot_data(output_directory + '/inputs')

    # Create offgridders input object
    offgridders_input = models.OffgriddersInput(project_name, project_site,
        active_components, additional_parameters, output_directory)

    return offgridders_input

# TODO: Add sums and C02 reductions
def get_average_C02(session_id):

    variable_tuples = [
        ('Wind generation', settings.CO2_WIND_PER_KWH),
        ('PV generation', settings.CO2_PV_PER_KWH),
        ('Genset generation', settings.CO2_DIESEL_PER_KWH),
        ('Consumption from main grid', settings.CO2_GRID_PER_KWH)
    ]

    time_series = pd.read_csv(settings.OUTPUT_DIRECTORY + session_id \
        + '/electricity_mg/electricity_mg.csv')

    for var_set in variable_tuples:
        if var_set[0] not in time_series.columns:
            time_series[var_set[0]] = [0] * len(time_series)

    average_CO2 = 0
    for variable_set in variable_tuples:
        variable_type = variable_set[0]
        co2_type = variable_set[1]

        CO2_production = time_series[variable_type].sum() \
                / (time_series['Wind generation'].sum() \
                    + time_series['PV generation'].sum() \
                    + time_series['Genset generation'].sum() \
                    + time_series['Consumption from main grid'].sum()) \
                * co2_type

        average_CO2 += CO2_production

    return average_CO2


def append_additional_results(session_id, latitude, longitude):
    output_file = settings.OUTPUT_DIRECTORY + session_id + '/test_results.csv'
    output_df = pd.read_csv(output_file)

    average_CO2_production = get_average_C02(session_id)

    optimal_slope, optimal_azimuth = \
        weather.get_optimal_panel_config(latitude, longitude)

    additional_data = {
        'optimal_slope': [optimal_slope],
        'optimal_azimuth': [optimal_azimuth],
        'CO2_mg_per_kWh': [average_CO2_production]}

    additional_data_df = pd.DataFrame.from_dict(additional_data)

    final_results = output_df.join(additional_data_df, how='outer')
    final_results.to_csv(output_file)