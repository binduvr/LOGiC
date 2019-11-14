import requests
import time
import json

BASE_URL = 'http://localhost:5000'
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

# Request location based additional factors
def test_location_data(country_code):
    location_data_url = BASE_URL + "/location_data/offgridders_data/" + country_code
    r = requests.get(location_data_url)
    additional_parameters = {'additional_parameters': json.loads(r.text)}
    #additional_parameters['fuel_price'] = 2.00
    return additional_parameters

# # Create user input and overwrite additional factors
def test_simulation(additional_parameters):
    user_input = {
        'project_name': 'koog',
        'country_code': 'NL',
        'address': "some random address",
        # NOTE: Make ure they are sent as floats.
        'latitude': 53.094,
        'longitude': 4.752,
        'demands': {
            'residential_demand': 365250,
            'commercial_demand': 0,
            'industrial_demand': 0
        },
        'active_components': {
            'wind': False,
            'solar': False,
            'storage': False,
            'dieselgen': True,
            # NOTE: Making grid active gives errors during report gen
            'grid_connection': True
        },
        'additional_parameters': {}
    }
    payload = {**user_input, **additional_parameters}

    # Run simulation using provided input and get session id
    simulation_url = BASE_URL + "/offgrid_simulator/simulate"
    r = requests.post(simulation_url, data=json.dumps(payload), headers=headers)
    session_id = r.text
    return session_id

# Attempt to retrieve results
def test_get_results(session_id):
    static_result_url = "/offgrid_simulator/get_result/" + session_id
    trying = True
    static_results = ''
    while trying:
        request_json = requests.get(BASE_URL + static_result_url)
        if request_json:
            static_results = request_json.text
            trying = False
        else:
            time.sleep(1)
    return static_results

# Retrieve daily time series for typical day
def test_daily_series(session_id):
    daily_series_types = ['mid_summer', 'mid_winter', 'spring_equinox', 'autumn_equinox']

    daily_time_series_url = "/offgrid_simulator/daily_time_series/" + session_id + "/mid_summer"
    daily_time_series = requests.get(BASE_URL + daily_time_series_url).text
    return daily_time_series


# Retrieve monthly totals time series
def test_monthly_series(session_id):
    monthly_time_series_url = "/offgrid_simulator/monthly_time_series/" + session_id
    monthly_time_series = requests.get(BASE_URL + monthly_time_series_url).text
    return monthly_time_series

# Retrieve input demands time series'
def test_demand_series(session_id):
    demand_time_series_url = "/offgrid_simulator/demand_series/" + session_id
    demand_time_series = requests.get(BASE_URL + demand_time_series_url).text
    return demand_time_series

# Send report to email address
def test_email_report(session_id, email):
    report_payload = {
        'session_id': session_id,
        'email': email
    }
    report_email_url = "/report/email"
    status = requests.post(BASE_URL + report_email_url, data=json.dumps(report_payload), headers=headers).text
    return status

# Download report
def test_download_report(session_id):
    report_download_url = "/report/download/" + session_id
    r = requests.get(BASE_URL + report_download_url)

    # Write contents of request to pdf file
    with open("OGTC_Simulation_Results.pdf", "wb") as file:
        file.write(r.content)


def test_application():
    additional_parameters = test_location_data("NL")
    print(additional_parameters)

    session_id = test_simulation(additional_parameters)
    # session_id = "20191029133752"
    print(session_id)

    static_results = test_get_results(session_id)
    print(static_results)

    daily_time_series = test_daily_series(session_id)

    monthly_time_series = test_monthly_series(session_id)

    demand_time_series = test_demand_series(session_id)

    # ENTER EMAIL HERE
    email = "test@gmail.com"
    email_status = test_email_report(session_id, email)
    print(email_status)

    test_download_report(session_id)

test_application()
