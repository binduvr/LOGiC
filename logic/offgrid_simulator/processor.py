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

import logic.report_generator.importer as importer
import logic.report_generator.generator as generator
import logic.report_generator.compiler as compiler
# TODO:

# MAKE OUTPUT INCLUDE HOW MANY SOLAR PANELS AND TYPE ETC AND WIND TURBINES AND COSTS
# MAKE THE FUNCTION RETURN ESTIMATED TIME OR SOMETHING

# PUT PICTURE OF LOCATION IN REPORT
# IMPORT TAX OVER THE MACHINARY ORDERED OR SOMETHING remove tax for now

def generate_simulation_results(input_dict, session_id):

    offgridders_input = generate_input(input_dict, session_id)

    results = og.run_simulation(offgridders_input)

    # Create report
    # FIXME: Find better threading solution, this is horrible
    # while True:
    #     try:
    #         reportdict = importer.import_data(session_id)
    #         generator.generate_report(session_id, reportdict)
    #         compiler.compile(session_id, reportdict)
    #     except:
    #         time.sleep(5)
    #         continue
    #     break
    reportdict = importer.import_data(session_id)
    generator.generate_report(session_id, reportdict)
    compiler.compile(session_id, reportdict)

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
    optimal_slope, optimal_azimuth = \
        weather.get_optimal_panel_config(latitude, longitude)
    panel_config = {'optimal_slope': [optimal_slope],
        'optimal_azimuth': [optimal_azimuth]}

    df = pd.DataFrame(data=panel_config)
    df.to_csv(output_directory + '/test_results.csv', index=False)

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
