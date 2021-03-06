import datetime
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# TODO: Remove ending slash
# Directories and file locations
OUTPUT_DIRECTORY = "data/outputs/"
INPUT_DIRECTORY = "data/inputs/"

DEMAND_PROFILE_DIRECTORY = INPUT_DIRECTORY + "demand_profiles/"
COUNTRY_DB = INPUT_DIRECTORY + "country_db_v1.1.csv"

REPORT_NAME = "OGTC_Simulation_Results"
EMAIL_TEXT_FILE = "data/email_text.html"

ADMIN_SETTINGS_FILE = "admin_settings.ini"

# Type of day time series and hour of year they start
# FIXME: Find the right days (no weekends)
TYPICAL_DAYS = {
    'mid_summer': "2019-06-21 00:00:00",
    'mid_winter': "2019-12-21 00:00:00",
    'spring_equinox': "2019-03-21 00:00:00",
    'autumn_equinox': "2019-09-21 00:00:00"
}

CO2_DIESEL_PER_KWH = 1.05564
CO2_GRID_PER_KWH = 0.4
CO2_WIND_PER_KWH = 0.011
CO2_PV_PER_KWH = 0.025

# Relevant output from test_results.csv to be used in time series
RELEVANT_COLUMNS = ['Demand', 'PV generation', 'Wind generation',
    'Excess generation', 'Storage charge', 'Storage discharge',
    'Storage SOC', 'Genset generation',
    'Consumption from main grid', 'Feed into main grid']

FORMATTED_COLUMN_NAMES = ['demand', 'pv_generation', 'wind_generation',
    'excess_generation', 'storage_charge', 'storage_discharge',
    'storage_soc', 'genset_generation',
    'maingrid_consumption', 'feed_into_maingrid']

# Default values for the Offgridders tool
CASE_DEFINITION = {'perform_simulation': True,
    'based_on_case': True,
    'capacity_pv_kWp': 'oem',
    'capacity_wind_kW': 'oem',
    'capacity_storage_kWh': 'oem',
    'force_charge_from_maingrid': False,
    'discharge_only_when_blackout': False,
    'capacity_rectifier_ac_dc_kW': 'oem',
    'capacity_inverter_dc_ac_kW': 'oem',
    'enable_inverter_only_at_backout': False,
    'capacity_genset_kW': 'oem',
    'genset_with_minimal_loading': False,
    'number_of_equal_generators': 1,
    'capacity_pcc_consumption_kW': 'oem',
    'capacity_pcc_feedin_kW': 'oem',
    'allow_shortage': True,
    'max_shortage': 'default',
    'stability_constraint': 'share_hybrid',
    'renewable_constraint': False,
    'evaluation_perspective': 'AC_system'}

PARAMETERS_CONSTANT_VALUES = {'blackout_duration': 0,
    'blackout_duration_std_deviation': 0,
    'blackout_frequency': 0,
    'blackout_frequency_std_deviation': 0,
    'combustion_value_fuel': 9.8,
    'demand_ac_scaling_factor': 1,
    'demand_dc_scaling_factor': 1,
    'distribution_grid_cost_investment': 0,
    'distribution_grid_cost_opex': 0,
    'distribution_grid_lifetime': 40,
    'genset_batch': 0.5,
    'genset_cost_investment': 820,
    'genset_cost_opex': 0.05,
    'genset_cost_var': 0,
    'genset_efficiency': 0.33,
    'genset_lifetime': 10,
    'genset_max_loading': 1,
    'genset_min_loading': 0.1,
    'genset_oversize_factor': 1,
    'inverter_dc_ac_batch': 0.5,
    'inverter_dc_ac_cost_investment': 0,
    'inverter_dc_ac_cost_opex': 0,
    'inverter_dc_ac_cost_var': 0,
    'inverter_dc_ac_efficiency': 1,
    'inverter_dc_ac_lifetime': 15,
    'maingrid_distance': 1,
    'maingrid_electricity_price': 0.22,
    'maingrid_extension_cost_investment': 0,
    'maingrid_extension_cost_opex': 0,
    'maingrid_extension_lifetime': 40,
    'maingrid_feedin_tariff': 0.05,
    'maingrid_renewable_share': 0,
    'min_renewable_share': 0,
    'pcoupling_batch': 1,
    'pcoupling_cost_investment': 200,
    'pcoupling_cost_opex': 0,
    'pcoupling_cost_var': 0,
    'pcoupling_efficiency': 1,
    'pcoupling_lifetime': 20,
    'pcoupling_oversize_factor': 1.5,
    'fuel_price': 1.30,
    'fuel_price_change_annual': 0.05,
    'project_cost_investment': 200,
    'project_cost_opex': 0,
    'project_lifetime': 20,
    'pv_batch': 0.5,
    'pv_cost_investment': 1200,
    'pv_cost_opex': 25,
    'pv_cost_var': 0,
    'pv_lifetime': 25,
    'rectifier_ac_dc_batch': 0.5,
    'rectifier_ac_dc_cost_investment': 0,
    'rectifier_ac_dc_cost_opex': 0,
    'rectifier_ac_dc_cost_var': 0,
    'rectifier_ac_dc_efficiency': 1,
    'rectifier_ac_dc_lifetime': 15,
    'shortage_max_allowed': 0,
    'shortage_max_timestep': 1,
    'shortage_penalty_costs': 0.5,
    'stability_limit': 0.2,
    'storage_batch_capacity': 1,
    'storage_batch_power': 1,
    'storage_capacity_cost_investment': 20,
    'storage_capacity_cost_opex': 6.75,
    'storage_capacity_lifetime': 13.5,
    'storage_cost_var': 0,
    'storage_Crate_charge': 1,
    'storage_Crate_discharge': 0.5,
    'storage_efficiency_charge': 0.97,
    'storage_efficiency_discharge': 0.97,
    'storage_loss_timestep': 0,
    'storage_power_cost_investment': 500,
    'storage_power_cost_opex': 0,
    'storage_power_lifetime': 13.5,
    'storage_soc_initial': 'None',
    'storage_soc_max': 1,
    'storage_soc_min': 0.2,
    'tax': 0,
    'wacc': 0.02,
    'white_noise_demand': 0,
    'white_noise_pv': 0,
    'white_noise_wind': 0,
    'wind_batch': 0.5,
    'wind_cost_investment': 2500,
    'wind_cost_opex': 50,
    'wind_cost_var': 0,
    'wind_lifetime': 20}

PARAMETERS_SENSITIVITY = {}

PROJECT_SITE = {'timeseries_file': 'test_site.csv',
    'title_time': 'None',
    'title_demand_ac': 'Demand',
    'title_demand_dc': 'None',
    'title_pv': 'SolarGen',
    'title_wind': 'Wind',
    'title_grid_availability': 'None',
    'seperator': ';',
    'file_index': None}

OFFGRIDDERS_SETTINGS = {'restore_oemof_if_existant': False,
    'restore_blackouts_if_existant': False,
    'include_shortage_penalty_costs_in_lcoe': False,
    'allow_shortage': True,
    'time_start': datetime.datetime(2019, 1, 1, 0, 0),
    'time_frequency': 'H',
    'sensitivity_all_combinations': False,
    'solver': 'cbc',
    'solver_verbose': False,
    'cmdline_option': 'ratioGap',
    'cmdline_option_value': 0.03,
    'input_folder_timeseries': './inputs/timeseries',
    'output_folder': 'simulation_results/test',
    'output_file': 'test_results',
    'save_lp_file': False,
    'lp_file_for_only_3_timesteps': False,
    'save_oemofresults': False,
    'save_to_csv_flows_storage': True,
    'save_to_csv_flows_electricity_mg': True,
    'save_to_png_flows_storage': True,
    'save_to_png_flows_electricity_mg': True,
    'display_meta': False,
    'display_main': False,
    'display_experiment': False,
    'results_demand_characteristics': True,
    'results_blackout_characteristics': True,
    'results_annuities': True,
    'results_costs': True,
    'necessity_for_blackout_timeseries_generation': True,
    'evaluated_days': 365}
