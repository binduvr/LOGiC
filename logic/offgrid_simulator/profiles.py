
import pandas as pd
import os

import logic.settings as settings

def get_demand(country_code, yearly_demand, type='residential'):
    """Generate hourly demand from demand profile and yearly demand"""

    directory = settings.DEMAND_PROFILE_DIRECTORY + type + '/'

    file_list = os.listdir(directory)
    countries = [x.split('.')[0] for x in file_list]

    country_code = country_code.upper()

    if country_code in countries:
        profile = pd.read_csv(directory + country_code + '.csv')
    else:
        profile = pd.read_csv(directory + 'NL.csv')

    return yearly_demand * profile['demand']