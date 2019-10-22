import flask
import logic.location_data.models as models

location_data = flask.Blueprint('location_data', __name__)

@location_data.route('/offgridders_data/<country_code>', methods=['GET'])
def get_offgridders_data(country_code):
    """Get all usable data for specific country."""

    if len(country_code) == 2:
        country = models.Country(country_code.upper())
        return country.to_dict()
    else:
        flask.abort(404)