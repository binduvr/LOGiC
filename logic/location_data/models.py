import pandas as pd
import requests as req
import threading
import io

import logic.settings as settings

class Country:
    """A country to be used as input for OESMOT.

    Attributes:
        country_code: The country code of the country
        blackout_frequency: Average number of blackouts per month
        blackout_duration: Average duration of a blackout
        electricity_price: Cost of electricity in EURO/kWh
        renewable_share: Fraction energy consumption from renewable sources
        tax: Import tax (VAT) as a fraction
        diesel_price: Current cost of diesel in EURO/L
    """

    # TODO: Make diesel price fuel price

    def __init__(self, country_code):
        self.country_code = country_code
        self.set_local_attributes()

        # TODO: Update live diesel price
        # self.diesel_price = self.get_diesel_price()

    def set_local_attributes(self):
        """Sets all attributes which are stored locally in the csv"""

        # Read country database csv file
        df = pd.read_csv(settings.COUNTRY_DB)
        # Retrieve series of values for country code
        result_series = df.query('country_code == @self.country_code')
        # Assign attributes
        self.blackout_frequency = result_series['blackout_frequency'].values[0]
        self.blackout_duration = result_series['blackout_duration'].values[0]
        self.electricity_price = result_series['electricity_price'].values[0]
        # TODO: To be updated live
        self.diesel_price = result_series['diesel_price'].values[0]
        self.renewable_share = result_series['renewable_share'].values[0]
        self.tax = result_series['tax'].values[0]

    def get_diesel_price(self):
        """Return current diesel price in country."""
        return None

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'blackout_frequency': self.blackout_frequency,
            'blackout_duration': self.blackout_duration,
            'electricity_price': self.electricity_price,
            'renewable_share': self.renewable_share,
            'tax': self.tax,
            'diesel_price': self.diesel_price,
        }
