import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import logic.offgrid_simulator.profiles as profiles
import logic.offgrid_simulator.weather as weather
import logic.settings as settings
from logic.offgrid_simulator import windconverters as windconverters
class ProjectSite:
    """A project site to be used in Offgridders.

    Objects of this class are used as an attribute in OffgriddersInput
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
            longitude, settings.OFFGRIDDERS_SETTINGS['evaluated_days'], demands) # NOTE: added demands as argument for use in turbine selection
        self.pv_generation_per_kWp = self.set_pv_generation(latitude,
            longitude, settings.OFFGRIDDERS_SETTINGS['evaluated_days'])


    def set_wind_generation(self, latitude, longitude, evaluated_days, demands): # NOTE: added demands as argument for use in turbine selection
        wind_speed = weather.get_wind_standard_year(latitude, longitude,
            evaluated_days)
        wind_generation, turbine_type = windconverters.chosen_turbine(wind_speed,demands)
        return wind_generation

    def set_pv_generation(self, latitude, longitude, evaluated_days):
        typicalpv = weather.get_solar_standard_year(latitude, longitude, evaluated_days)
        # NOTE: This is a rough estimate and is not accurate
        solar_generation = typicalpv['pvaverage']/1000
        return solar_generation

    def plot_data(self, directory):
        """Generates csv of the variables to the given directory and plots"""

        df = pd.DataFrame({'per_unit_pv_generation': list(self.pv_generation_per_kWp),
                'per_unit_wind_generation': list(self.wind_generation_per_kW),
                'residential_demand': list(self.residential_demand),
                'commercial_demand': list(self.commercial_demand),
                'industrial_demand': list(self.industrial_demand)
            })

        df.to_csv(directory + '/demands.csv')

        # TODO: Add actual time to axis instead of index
        for column in df:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(df[column])
            plt.savefig(directory + '/' + column)
            plt.close(fig)


    def to_dict(self):

        default_data = settings.PROJECT_SITE

        demand_parameters = {
            'demand_ac': self.demand_ac,
            'wind_generation_per_kW': self.wind_generation_per_kW,
            'pv_generation_per_kWp': self.pv_generation_per_kWp,
            'demand_dc': self.demand_dc
        }
        return {'test_site': {**default_data, **demand_parameters}}


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
    case_definition: dictionary
        A dictionary defining the test case
    parameters_constant_values: dictionary
        Addictional variables to be used in simulation
    settings: dictionary
        Simulation settings
    parameters_sensitivity: dictionary
        Additional parameters for the sensitivity experiment
    project_site: ProjectSite
        Object containing various demand and generation data

    """

    def __init__(self, project_name, project_site, active_components,
        additional_parameters, output_folder):
        self.project_name = project_name
        self.case_definition = \
            self.set_case_definition(self.project_name, active_components)
        # TODO: Ensure null values are excluded
        self.parameters_constant_values = \
            self.set_parameters_constant_values(additional_parameters)
        self.settings = settings.OFFGRIDDERS_SETTINGS
        self.settings['output_folder'] = output_folder
        self.parameters_sensitivity = settings.PARAMETERS_SENSITIVITY
        self.project_site = project_site

    def set_case_definition(self, project_name, active_components):

        case_definition = settings.CASE_DEFINITION

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

    def set_parameters_constant_values(self, additional_parameters):
        result_params = {}
        for key in additional_parameters.keys():
            if additional_parameters[key] != '':
                result_params[key] = additional_parameters[key]
        return {**settings.PARAMETERS_CONSTANT_VALUES, **result_params}

    def to_dict(self):
        offgridders_data = {
           'case_definition': self.case_definition,
           'parameters_constant_values': self.parameters_constant_values,
           'parameters_sensitivity': self.parameters_sensitivity,
           'project_site_s': self.project_site.to_dict(),
           'settings': self.settings
        }
        return offgridders_data
