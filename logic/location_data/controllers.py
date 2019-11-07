import flask
import simplejson

import logic.settings as settings
import logic.location_data.models as models

location_data = flask.Blueprint('location_data', __name__)

@location_data.route('/offgridders_data/<country_code>', methods=['GET'])
def get_offgridders_data(country_code):
    """Get all usable data for specific country."""

    if len(country_code) == 2:
        country = models.Country(country_code.upper())
        country_data = country.get_simulation_input()

        # TODO: Replaces NaN's with defaults in settings, do another way
        # TODO: Check which defaults were change by checking if they equal

        # Overwrite unknowns with defaults
        # for key in country_data.keys():
        #     if country_data[key] == '':
        #         country_data[key] = settings.PARAMETERS_CONSTANT_VALUES[key]
        # return simplejson.dumps(country_data, ignore_nan=True)

        # Only send known values
        # result_data = {}
        # for key in country_data.keys():
        #     if country_data[key] != '':
        #         result_data[key] = country_data[key]
        # return simplejson.dumps(result_data, ignore_nan=True)

        return simplejson.dumps(country_data, ignore_nan=True)

    else:
        flask.abort(404)