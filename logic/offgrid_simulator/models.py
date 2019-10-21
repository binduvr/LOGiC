import datetime
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pprint as pp

import logic.offgrid_simulator.profiles as profiles
import logic.offgrid_simulator.weather as weather

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

PARAMETERS_CONSTANT_VALUES = {'blackout_duration': 2.5,
    'blackout_duration_std_deviation': 0.5,
    'blackout_frequency': 4,
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
    'maingrid_electricity_price': 0.248,
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
    'pv_cost_investment': 2800,
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
    'wacc': 0.16,
    'white_noise_demand': 0,
    'white_noise_pv': 0,
    'white_noise_wind': 0,
    'wind_batch': 0.5,
    'wind_cost_investment': 2500,
    'wind_cost_opex': 0,
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

SETTINGS = {'restore_oemof_if_existant': False,
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
    'evaluated_days': 14}


class ProjectSite:
    """A project site to be used in Offgridders.

    Objects of this class are used as an attribute in OESMOTInput
    objects and determine the demand profiles and per unit power
    generation of wind and solar generators

    Parameters
    ----------
    country_code: str
        ISO 3166-1 alpha-2 country code of location.
    latitude: float
        Latitude coordinate of location.
    longitude: float
        Longitude coordinate of location.
    demands: dictionary
        Type of demand key (residential, commercial, industrial) and
        yearly demand value in kWh/year.

    Attributes
    ----------
    country_code: str
        ISO 3166-1 alpha-2 country code.
    plot_data:

    demand_ac: pandas Series
        Hourly time series with AC power demand for each hour of year
    demand_ac: pandas Series
        Hourly time series with DC power demand for each hour of year
    wind_generation_per_kW: pandas Series
        Hourly time series with wind generation in kW/kW for each hour
        of the year based on hourly wind speed typical year
    pv_generation_per_kWp: pandas Series
        Hourly time series with solar generation in kW/kWp for each
        hour of the year based on hourly solar irradiance typical year
    """

    def __init__(self, country_code, latitude, longitude, demands):
        self.country_code = country_code

        self.residential_demand = profiles.get_demand(country_code,
            demands['residential_demand'], type='residential')

        self.commercial_demand = profiles.get_demand(country_code,
            demands['commercial_demand'])

        self.industrial_demand = profiles.get_demand(country_code,
            demands['industrial_demand'])

        self.demand_ac = self.residential_demand \
            + self.commercial_demand + self.industrial_demand
        # TODO: Finish DC demand assignment (now on 0)
        self.demand_dc = self.demand_ac - self.demand_ac

        self.wind_generation_per_kW = self.set_wind_generation(latitude,
            longitude, SETTINGS['evaluated_days'])
        self.pv_generation_per_kWp = self.set_pv_generation(latitude,
            longitude, SETTINGS['evaluated_days'])


    def set_wind_generation(self, latitude, longitude, evaluated_days):
        wind_speed = weather.get_wind_standard_year(latitude, longitude,
            evaluated_days)
        # NOTE: Rough estimate
        wind_generation = wind_speed / 24

        return wind_generation

    def set_pv_generation(self, latitude, longitude, evaluated_days):
        typicalpv = weather.get_solar_standard_year(latitude, longitude, evaluated_days)
        # NOTE: This is a rough estimate and is not accurate
        solar_generation = typicalpv['pvaverage']/1000

        return solar_generation

    def plot_data(self, directory):
        """Plots a figure of the variable to the given file"""

        plot_name_list = [(self.pv_generation_per_kWp, 'per_unit_pv_generation'),
            (self.wind_generation_per_kW, 'per_unit_wind_generation'),
            (self.residential_demand, 'residential_demand'),
            (self.commercial_demand, 'commercial_demand'),
            (self.industrial_demand, 'industrial_demand')]

        for variable_tuple in plot_name_list:
            plot_variable = variable_tuple[0]
            plot_name = variable_tuple[1]
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(plot_variable)
            plt.savefig(directory + '/' + plot_name)
            plt.close(fig)

    def to_dict(self):

        default_data = PROJECT_SITE

        additional_parameters = {
            'demand_ac': self.demand_ac,
            'wind_generation_per_kW': self.wind_generation_per_kW,
            'pv_generation_per_kWp': self.pv_generation_per_kWp,
            'demand_dc': self.demand_dc
        }
        return {'test_site': {**default_data, **additional_parameters}}


class OffgriddersInput:
    """Input for Offgridders.

    Objects of this class are used as an input or the OESMOT tool.

    Parameters
    ----------
    country_code: str
        ISO 3166-1 alpha-2 country code.
    latitude: float
        Latitude coordinate of location.
    longitude: float
        Longitude coordinate of location.
    project_name: str
        The name of the test case.
    active_components: dictionary
        Component keys and boolean values stating whether active.
    demands: dictionary
        Type of demand key (residential, commercial, industrial) and
        yearly demand value in kWh/year.
    additional_parameters: dictionary
        Additional parameters to be used instead of default values.
    settings: dictionary
        Additional settings to be used instead of defaults.

    Attributes
    ----------
    project_name: str
        Name of the simulation case.
    case_definitions: dictionary
    parameters_constant_values:
    settings:
    input_excel_file:
    parameters_sensitivity:
    project_site_s:
    blackouts:
    """

    def __init__(self, project_name, project_site, active_components,
        additional_parameters, output_folder):
        self.project_name = project_name
        self.case_definition = \
            self.set_case_definition(self.project_name, active_components)
        self.parameters_constant_values = \
            {**PARAMETERS_CONSTANT_VALUES, **additional_parameters}
        self.settings = SETTINGS
        self.settings['output_folder'] = output_folder
        self.parameters_sensitivity = PARAMETERS_SENSITIVITY
        self.project_site = project_site

    def set_case_definition(self, project_name, active_components):

        case_definition = CASE_DEFINITION

        case_definition['case_name'] = project_name

        if not active_components['wind']:
            case_definition['capacity_wind_kW'] = 'None'
        if not active_components['solar']:
            case_definition['capacity_pv_kWp'] = 'None'
        if not active_components['storage']:
            case_definition['capacity_storage_kWh'] = 'None'
        if not active_components['grid_connection']:
            case_definition['capacity_pcc_consumption_kW'] = 'None'
            case_definition['capacity_pcc_feedin_kW'] = 'None'

        return case_definition


    def to_dict(self):
        offgridders_data = {
           # 'totalperkwpPV' = sum(self.solargen),
           # 'totalperkwwind' = sum(self.windgen),
           # 'blackoutdf': self.blackouts,
           'case_definition': self.case_definition,
           'parameters_constant_values': self.parameters_constant_values,
           'parameters_sensitivity': self.parameters_sensitivity,
           'project_site_s': self.project_site.to_dict(),
           'settings': self.settings
        }

        return offgridders_data