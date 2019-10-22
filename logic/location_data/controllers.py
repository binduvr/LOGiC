# from flask import Flask, request, Blueprint, abort, jsonify
import flask
import logic.location_data.models as models

location_data = flask.Blueprint('location_data', __name__)

@location_data.route('/oesmot_data/<country_code>', methods=['GET'])
def get_oesmot_data(country_code):
    """Get all data for specific country.

    Most of this data is currently the data which can be used in OESMOT.
    Currently no extra social data implemented.
    """

    # try:
    #     country = models.Country(country_code.upper())
    #     return country.to_dict()
    # except:
    #     abort(400)

    # country_code = country_code.upper()

    if len(country_code) == 2:
        country = models.Country(country_code.upper())
        return country.to_dict()
    else:
        flask.abort(404)


