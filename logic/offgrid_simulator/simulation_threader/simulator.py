import numpy as np
import json
import sys
import pandas as pd
import time
import requests as req
import re
import traceback

import offgridders.A_offgridders_wrapper as og
import output_settings as settings

sim_input_json_file = str(sys.argv[1])
output_folder = str(sys.argv[2])

def generate_simulation_results(sim_input_json_file):

    with open(sim_input_json_file) as f:
        data = json.load(f)

    offgridders_input = data['offgridders_input']

    test_site = offgridders_input['project_site_s']['test_site']
    test_site['demand_ac'] = pd.Series(test_site['demand_ac'])
    test_site['wind_generation_per_kW'] = pd.Series(test_site['wind_generation_per_kW'])
    test_site['pv_generation_per_kWp'] = pd.Series(test_site['pv_generation_per_kWp'])
    test_site['demand_dc'] = pd.Series(test_site['demand_dc'])

    offgridders_input['project_site_s']['test_site'] = test_site


    results = og.run_simulation(offgridders_input)

    # TODO: Find better way for lat lon
    latitude = data['latitude']
    longitude = data['longitude']
    session_id = data['session_id']


    append_additional_results(session_id, latitude, longitude)


def get_average_C02(session_id):

    variable_tuples = [
        ('Wind generation', settings.CO2_WIND_PER_KWH),
        ('PV generation', settings.CO2_PV_PER_KWH),
        ('Genset generation', settings.CO2_DIESEL_PER_KWH),
        ('Consumption from main grid', settings.CO2_GRID_PER_KWH)
    ]

    time_series = pd.read_csv(output_folder + '/electricity_mg/electricity_mg.csv')

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

# TODO: Move to main app
def get_optimal_panel_config(lat, lon):

    try:
        base_url = "http://re.jrc.ec.europa.eu/pvgis5/PVcalc.php?lat={}&lon={}\
            &loss=14&peakpower=1&outputformatchoice=basic&optimalinclination=1\
            &optimalangles=1&inclined_optimum=1&vertical_optimum=1"

        url = base_url.format(lat, lon)
        r = req.get(url)

        slope = [int(k) for k in re.findall(r'\b\d+\b', r.text.splitlines()[5])][0]
        azimuth = [int(k) for k in re.findall(r'\b\d+\b', r.text.splitlines()[6])][0]

        return slope, azimuth
    except Exception:
        traceback.print_exc()
        return 0, 0

def append_additional_results(session_id, latitude, longitude):
    output_file = output_folder + '/test_results.csv'
    output_df = pd.read_csv(output_file)

    average_CO2_production = get_average_C02(session_id)

    optimal_slope, optimal_azimuth = \
        get_optimal_panel_config(latitude, longitude)

    additional_data = {
        'optimal_slope': [optimal_slope],
        'optimal_azimuth': [optimal_azimuth],
        'CO2_mg_per_kWh': [average_CO2_production]}

    additional_data_df = pd.DataFrame.from_dict(additional_data)

    final_results = output_df.join(additional_data_df, how='outer')
    final_results.to_csv(output_file)



# Run simulation
generate_simulation_results(sim_input_json_file)