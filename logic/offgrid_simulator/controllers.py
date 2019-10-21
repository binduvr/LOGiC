from flask import Flask, request, Blueprint, abort, jsonify, make_response, Response, send_from_directory
import threading
import pandas as pd
import time
import pprint as pp

import logic.offgrid_simulator.processor as processor

offgrid_simulator = Blueprint('offgrid_simulator', __name__)

# TODO: Store file names and directories in config file or smth
def process_request(input_dict, session_id):
    """Run the simulation with the given data."""

    # TODO: Fix solver multithreading problem
    # x = threading.Thread(target=processor.generate_simulation_results,
    #    args=(input_dict, session_id))
    # x.start()
    processor.generate_simulation_results(input_dict, session_id)

@offgrid_simulator.route('/')
def handle_request():
    """Runs a simulation using supplied values."""

    # Testing #######################
    input_dict = {
        'project_name': 'hoevelaken',
        'country_code': 'NL',
        # NOTE: Make sure they are sent as floats.
        'latitude': 51,
        'longitude': 5,
        'demands': {
            'residential_demand': 35000,
            'commercial_demand': 0,
            'industrial_demand': 0
        },
        'active_components': {
            'wind': True,
            'solar': True,
            'storage': True,
            'dieselgen': False,
            'grid_connection': False
        },
        'additional_parameters': {'blackout_frequency': 0}
    }
    #######################




    session_id = time.strftime("%Y%m%d%H%M%S", time.gmtime())

    # input_dict = request.args.to_dict()

    process_request(input_dict, session_id)
    return session_id


@offgrid_simulator.route('/get_result/<session_id>')
def get_result(session_id=None):
    """Retrieves simulation results using session ID."""

    file_path = 'data/outputs/' + session_id + '/test_results.csv'
    results = pd.read_csv(file_path)
    try:
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

            'optimal_slope': float(results['optimal_slope'][0]),
            'optimal_azimuth': float(results['optimal_azimuth'][0])
        }
        return webpage_output
    except:
        abort(500)


@offgrid_simulator.route('/get_time_series/<session_id>/<series_type>')
def get_daily_time_series(session_id, series_type):
    """Retrives a certain time series for 1 day."""

    # Type of day time series and hour of year they start
    time_series_types = {
        # FIXME: Find the right values
        'mid_summer': 4105, # 21 June
        'mid_winter': 8497, # 21 December
        'spring_equinox': 1898, # 21 March
        'autumn_equinox': 6313 # 21 March
    }

    relevant_columns = ['Demand', 'PV generation', 'Wind generation',
        'Excess generation', 'Storage charge', 'Storage discharge',
        'Genset generation']

    if series_type in time_series_types.keys():
        time_series = pd.read_csv('data/outputs/' + session_id \
            + '/electricity_mg/electricity_mg.csv', usecols=relevant_columns)

        day_series = time_series[time_series_types[series_type]:\
            time_series_types[series_type] + 24]

        response = make_response(day_series.to_json())
        return jsonify(response.get_json(force=True))

# @offgrid_simulator.route('/get_time_series/<session_id>/<series_type>')
# def


# FIXME:
@offgrid_simulator.route('/get_image/<session_id>/<file>')
def get_image(session_id=None, file=None):
    """Retrieves a specific image from a specific simulation."""

    file_path = 'data/outputs/'+session_id+'/inputs'

    try:
        return send_from_directory(file_path, filename=file, as_attachment=True)
    except FileNotFoundError:
        abort(404)
