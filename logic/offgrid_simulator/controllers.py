import flask
import threading
import pandas as pd
import time
import pprint as pp

import logic.settings as settings
import logic.offgrid_simulator.processor as processor

offgrid_simulator = flask.Blueprint('offgrid_simulator', __name__)

def process_request(input_dict, session_id):
    """Run the simulation with the given data."""

    x = threading.Thread(target=processor.generate_simulation_results,
       args=(input_dict, session_id))
    x.start()

# @offgrid_simulator.route('/simulate', methods=['POST'])
@offgrid_simulator.route('/simulate')
def handle_request():
    """Runs a simulation using supplied values."""

    # Testing #######################
    input_dict = {
        'project_name': 'hoevelaken',
        'country_code': 'NL',
        'address': "some random address",
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
            'dieselgen': True,
            'grid_connection': False
        },
        'additional_parameters': {'blackout_frequency': 0}
    }
    #######################




    session_id = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    # input_dict = request.get_json(force=True)

    process_request(input_dict, session_id)
    return session_id


@offgrid_simulator.route('/get_result/<session_id>', methods=['GET'])
def get_result(session_id=None):
    """Retrieves simulation results using session ID."""

    file_path = settings.OUTPUT_DIRECTORY + session_id + '/test_results.csv'
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
        flask.abort(500)


@offgrid_simulator.route('/daily_time_series/<session_id>/<series_type>', methods=['GET'])
def get_daily_time_series(session_id, series_type):
    """Retrieves a certain time series for 1 day."""

    typical_days = settings.TYPICAL_DAYS

    # TODO: Use same method as monthly time series
    if series_type in typical_days.keys():
        time_series = pd.read_csv(settings.OUTPUT_DIRECTORY + session_id \
            + '/electricity_mg/electricity_mg.csv')

        start_index = time_series.loc[time_series['timestep'] == \
            typical_days[series_type]].index[0]

        relevant_data = time_series[settings.RELEVANT_COLUMNS].copy()

        day_series = relevant_data[start_index:start_index + 24]

        response = flask.make_response(day_series.reset_index().to_json())
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

    for i in range(1, 13):
        month_series = time_series.loc[(time_series['timestep'].dt.month == i)]
        month_list.append(month_series.sum())

    # Dope one liner ayy lmao
    # month_list = [time_series.loc[(time_series['timestep'].dt.month == i)].sum() for i in range(1, 13)]

    monthly_dataframe = pd.DataFrame(month_list, columns=settings.RELEVANT_COLUMNS)

    response = flask.make_response(monthly_dataframe.reset_index().to_json())
    return flask.jsonify(response.get_json(force=True))


@offgrid_simulator.route('/demand_series/<session_id>', methods=['GET'])
def get_input_series(session_id=None, file=None):
    """Retrieves demand and generation profiles from a specific simulation."""

    file_path = settings.OUTPUT_DIRECTORY + session_id \
        + '/inputs/demands.csv'

    demand_dataframe = pd.read_csv(file_path)

    response = flask.make_response(demand_dataframe.to_json())
    return flask.jsonify(response.get_json(force=True))
