import flask
import threading
import pandas as pd
import time
import pprint as pp
import simplejson
import json
import numpy as np

import logic.settings as settings
import logic.offgrid_simulator.processor as processor

offgrid_simulator = flask.Blueprint('offgrid_simulator', __name__)

def process_request(input_dict, session_id):
    """Run the simulation with the given data."""

    x = threading.Thread(target=processor.generate_simulation_results,
       args=(input_dict, session_id))
    x.start()

@offgrid_simulator.route('/simulate', methods=['POST'])
# @offgrid_simulator.route('/simulate')
def handle_request():
    """Runs a simulation using supplied values."""

    session_id = time.strftime("%Y%m%d%H%M%S", time.gmtime())

    input_dict = flask.request.get_json(force=True)

    processor.generate_simulation_results(input_dict, session_id)

    # # THIS IS THE ORKNEY ISLANDS ID TO USE IF PANIC BUTTON, NO GRID
    # session_id = "20191115083605"
    # time.sleep(60)

    return session_id


@offgrid_simulator.route('/get_result/<session_id>', methods=['GET'])
def get_result(session_id=None):
    """Retrieves simulation results using session ID."""

    file_path = settings.OUTPUT_DIRECTORY + session_id + '/test_results.csv'
    try:
        results = pd.read_csv(file_path)

        with open(settings.OUTPUT_DIRECTORY + session_id \
                + "/inputs/input.json", encoding='utf-8') as f:
            inputs = json.loads(f.read())

        annual_demand = float(results['total_demand_annual_kWh'][0])
        CO2_mg_per_kWh = float(results['CO2_mg_per_kWh'][0])

        # If grid not active use diesel co2 production
        if inputs['active_components']['grid_connection']:
            baseline_CO2 = settings.CO2_GRID_PER_KWH
        else:
            baseline_CO2 = settings.CO2_DIESEL_PER_KWH

        kg_CO2_saved = (baseline_CO2 - CO2_mg_per_kWh) * annual_demand

        webpage_output = {
            'session_id': session_id,
            'nominal_solar_power_installed': float(results['capacity_pv_kWp'][0]),
            'nominal_wind_power_installed': float(results['capacity_wind_kW'][0]),
            'nominal_diesel_generator_power': float(results['capacity_genset_kW'][0]),
            'storage_capacity': float(results['capacity_storage_kWh'][0]),
            'renewable_energy_share': float((results['res_share'][0])*100),
            'levelised_cost_of_electricity': float(results['lcoe'][0]),
            'solar_system_cost': float(results['costs_pv'][0]),
            'wind_system_cost': float(results['costs_wind'][0]),
            'storage_unit_cost': float(results['costs_storage'][0]),
            'diesel_generator_cost': float(results['costs_genset'][0]),
            'annuity_pv': float(results['annuity_pv'][0]),
            'annuity_wind': float(results['annuity_wind'][0]),
            'annuity_genset': float(results['annuity_genset'][0]),

            # TODO: Change 0 to O
            'kg_C02_saved': float(kg_CO2_saved),
            'optimal_slope': float(results['optimal_slope'][0]),
            'optimal_azimuth': float(results['optimal_azimuth'][0])
        }
        return simplejson.dumps(webpage_output, ignore_nan=True)
    except Exception as e:
        print(e)
        flask.abort(404)


@offgrid_simulator.route('/daily_time_series/<session_id>/<series_type>', methods=['GET'])
def get_daily_time_series(session_id, series_type):
    """Retrieves a certain time series for 1 day."""

    typical_days = settings.TYPICAL_DAYS.copy()

    # TODO: Use same method as monthly time series
    if series_type in typical_days.keys():
        time_series = pd.read_csv(settings.OUTPUT_DIRECTORY + session_id \
            + '/electricity_mg/electricity_mg.csv')

        start_index = time_series.loc[time_series['timestep'] == \
            typical_days[series_type]].index[0]

        # relevant_data = time_series[settings.RELEVANT_COLUMNS].copy()
        relevant_data = pd.DataFrame(time_series)

        relevant_column_dict = dict(zip(settings.RELEVANT_COLUMNS.copy(), settings.FORMATTED_COLUMN_NAMES.copy()))

        # Make empty arrays
        for key in relevant_column_dict.keys():
            if key not in relevant_data.columns:
                relevant_data[key] = [0] * len(time_series)

        relevant_data.rename(columns=relevant_column_dict, inplace=True)

        day_series = relevant_data[start_index:start_index + 24]
        new = day_series.filter(relevant_column_dict.values(), axis=1)

        response = flask.make_response(new.reset_index().to_json())
        return flask.jsonify(response.get_json(force=True))

    else:
        flask.abort(404)


@offgrid_simulator.route('/monthly_time_series/<session_id>', methods=['GET'])
def get_monthly_time_series(session_id):
    """Retrieves monthly totals time series' for 12 months."""

    time_series = pd.read_csv(settings.OUTPUT_DIRECTORY + session_id \
        + '/electricity_mg/electricity_mg.csv')

    time_series['timestep'] = pd.to_datetime(time_series['timestep'],
        errors='coerce')

    month_list = []
    # columns = time_series.columns

    for i in range(1, 13):
        month_series = time_series.loc[(time_series['timestep'].dt.month == i)]
        month_list.append(month_series.sum())

    # Dope one liner ayy lmao
    # month_list = [time_series.loc[(time_series['timestep'].dt.month == i)].sum() for i in range(1, 13)]

    # monthly_dataframe = pd.DataFrame(month_list, columns=settings.RELEVANT_COLUMNS)
    monthly_dataframe = pd.DataFrame(month_list)
    relevant_column_dict = dict(zip(settings.RELEVANT_COLUMNS.copy(), settings.FORMATTED_COLUMN_NAMES.copy()))

    # TODO: Make sure everything works
    # Make empty arrays
    for key in relevant_column_dict.keys():
        if key not in monthly_dataframe.columns:
            monthly_dataframe[key] = [0] * len(month_list)

    monthly_dataframe.rename(columns=relevant_column_dict, inplace=True)

    new = monthly_dataframe.filter(relevant_column_dict.values(), axis=1)

    response = flask.make_response(new.reset_index().to_json())
    return flask.jsonify(response.get_json(force=True))


@offgrid_simulator.route('/demand_series/<session_id>', methods=['GET'])
def get_input_series(session_id=None, file=None):
    """Retrieves demand and generation profiles from a specific simulation."""

    file_path = settings.OUTPUT_DIRECTORY + session_id \
        + '/inputs/demands.csv'

    demand_dataframe = pd.read_csv(file_path)

    response = flask.make_response(demand_dataframe.to_json())
    return flask.jsonify(response.get_json(force=True))
