import numpy as np
import json
import os
import pandas as pd
import pprint as pp
import time
import subprocess

# import logic.offgrid_simulator.offgridders.A_offgridders_wrapper as og
import logic.offgrid_simulator.models as models
import logic.offgrid_simulator.weather as weather
import logic.settings as settings


def start_simulation_thread(input_dict, session_id):

    offgridders_input = generate_input(input_dict, session_id).to_dict()

    sim_input_json = {
        'offgridders_input': offgridders_input,
        'session_id': session_id,
        'latitude': input_dict['latitude'],
        'longitude': input_dict['longitude']
    }

    sim_input_file = os.path.abspath(settings.OUTPUT_DIRECTORY + session_id + '/inputs/sim_input.json')
    output_folder = offgridders_input['settings']['output_folder']
    simulator_script = "logic/offgrid_simulator/simulation_threader/simulator.py"

    # Dump offgridders json to the directory for use as input in simulator script
    with open(sim_input_file, 'w') as fp:
        json.dump(sim_input_json, fp)


    # Run system simulator scrpt whatever
    subprocess.Popen("python " + simulator_script + " " \
        + sim_input_file + " " + output_folder, shell=True)

    return session_id


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
    output_directory = os.path.abspath(settings.OUTPUT_DIRECTORY + session_id)
    os.mkdir(output_directory)

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